from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QLineEdit, QMessageBox, QFrame
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
import base64
import os
from groq import Groq


class LlamafyVisionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visionari - AI Image Analysis Tool")
        self.setGeometry(100, 100, 700, 900)
        self.setStyleSheet("background-color: #F0F0F0;")
        self.setWindowIcon(QIcon("vision.png"))

        self.layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Visionari - AI Image Analysis Tool")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "background-color: #FFA726; padding: 15px; font-size: 24px; font-weight: bold; color: white; border-radius: 10px;")
        self.layout.addWidget(self.title_label)

        # GROQ Key Input
        self.groq_key_frame = QFrame()
        self.groq_key_layout = QHBoxLayout()
        self.groq_key_frame.setLayout(self.groq_key_layout)
        self.groq_key_label = QLabel("GROQ Key:")
        self.groq_key_label.setFont(QFont("Arial", 12))
        self.groq_key_input = QLineEdit()
        self.groq_key_input.setPlaceholderText("Enter your GROQ API Key here")
        self.groq_key_input.setMinimumHeight(30)
        self.groq_key_layout.addWidget(self.groq_key_label)
        self.groq_key_layout.addWidget(self.groq_key_input)
        self.layout.addWidget(self.groq_key_frame)

        # Image Upload Section
        self.image_upload_frame = QFrame()
        self.image_layout = QHBoxLayout()
        self.image_upload_frame.setLayout(self.image_layout)
        self.image_label = QLabel("Image Upload:")
        self.image_label.setFont(QFont("Arial", 12))
        self.open_button = QPushButton("Upload Image")
        self.open_button.setStyleSheet(
            "padding: 10px; background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px;")
        self.open_button.clicked.connect(self.open_image)
        self.image_layout.addWidget(self.image_label)
        self.image_layout.addWidget(self.open_button)
        self.layout.addWidget(self.image_upload_frame)

        # Image Preview Area
        self.image_preview_label = QLabel("Image Preview Here")
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setStyleSheet(
            "border: 2px solid #BDBDBD; min-height: 200px; min-width: 400px; background-color: white; border-radius: 10px;")
        self.layout.addWidget(self.image_preview_label)

        # Image Query Section
        self.image_query_label = QLabel("Image Query:")
        self.image_query_label.setFont(QFont("Arial", 12))
        self.image_query_input = QLineEdit()
        self.image_query_input.setPlaceholderText("Enter your Image Query here")
        self.image_query_input.setMinimumHeight(50)
        self.layout.addWidget(self.image_query_label)
        self.layout.addWidget(self.image_query_input)

        # LLM Output Section
        self.output_label = QLabel("LLM Output:")
        self.output_label.setFont(QFont("Arial", 12))
        self.output_label.setStyleSheet(
            "background-color: #FFA726; padding: 5px; color: white; font-weight: bold; border-radius: 5px;")
        self.layout.addWidget(self.output_label)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(300)
        self.output_text.setStyleSheet(
            "background-color: #FFFFFF; border: 2px solid #BDBDBD; border-radius: 10px; padding: 10px;")
        self.layout.addWidget(self.output_text)

        # Submit and Clear Buttons
        self.button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit Query")
        self.submit_button.setStyleSheet(
            "padding: 10px; background-color: #2196F3; color: white; font-weight: bold; border-radius: 5px;")
        self.submit_button.clicked.connect(self.submit_query)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(
            "padding: 10px; background-color: #F44336; color: white; font-weight: bold; border-radius: 5px;")
        self.clear_button.clicked.connect(self.clear_fields)
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.clear_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.jpeg *.jpg);;All Files (*)", options=options)

        if file_path:
            try:
                # Load and display image
                pixmap = QPixmap(file_path)
                self.image_preview_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.image_path = file_path
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def submit_query(self):
        groq_key = self.groq_key_input.text()
        image_query = self.image_query_input.text()

        if not groq_key:
            QMessageBox.warning(self, "Input Error", "Please enter a valid GROQ Key.")
            return

        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "Input Error", "Please upload an image.")
            return

        if not image_query or image_query == "Enter your Image Query here":
            QMessageBox.warning(self, "Input Error", "Please enter a valid image query.")
            return

        try:
            # Encode image to base64 for API
            with open(self.image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                # Call API
                output = self.call_llm_api(groq_key, base64_image, image_query)
                self.output_text.setPlainText(output)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process the image: {str(e)}")

    def call_llm_api(self, groq_key, base64_image, image_query):
        try:
            client = Groq(api_key=groq_key)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": image_query},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                model="llava-v1.5-7b-4096-preview",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            QMessageBox.critical(self, "API Error", f"Failed to get response from LLM API: {str(e)}")
            return ""

    def clear_fields(self):
        self.image_query_input.clear()
        self.output_text.clear()
        self.image_preview_label.clear()
        self.image_preview_label.setText("Image Preview Here")
        if hasattr(self, 'image_path'):
            del self.image_path


if __name__ == "__main__":
    app = QApplication([])
    window = LlamafyVisionApp()
    window.show()
    app.exec_()