from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QLineEdit, QMessageBox, QFrame, QSlider, QGridLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
import base64
import os
from groq import Groq


# Main application class for Llamafy Vision, a tool that uses an LLM to analyze images
class LlamafyVisionApp(QWidget):
    def __init__(self):
        super().__init__()
        # Set up the main window
        self.setWindowTitle("Visionari - AI Image Analysis Tool")
        self.setGeometry(100, 100, 800, 1000)  # Adjusted window size
        self.setStyleSheet("background-color: #EAEAEA;")
        self.setWindowIcon(QIcon("vision.png"))

        # Main layout for the application
        self.main_layout = QGridLayout()

        # Title Label
        self.title_label = QLabel("Visionari - AI Image Analysis Tool")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "background-color: #B0BEC5; padding: 15px; font-size: 24px; font-weight: bold; color: #FFFFFF; border-radius: 10px;")
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 2)

        # GROQ Key Input Section
        self.groq_key_frame = QFrame()  # Frame to hold GROQ key input elements
        self.groq_key_layout = QHBoxLayout()
        self.groq_key_frame.setLayout(self.groq_key_layout)
        self.groq_key_label = QLabel("GROQ Key:")  # Label for GROQ Key input
        self.groq_key_label.setFont(QFont("Arial", 12))  # Set font for the label
        self.groq_key_input = QLineEdit()  # Input field for GROQ Key
        self.groq_key_input.setPlaceholderText("Enter your GROQ API Key here")  # Placeholder text
        self.groq_key_input.setMinimumHeight(30)  # Set minimum height for input field
        self.groq_key_layout.addWidget(self.groq_key_label)  # Add label to layout
        self.groq_key_layout.addWidget(self.groq_key_input)  # Add input field to layout
        self.main_layout.addWidget(self.groq_key_frame, 1, 0, 1, 2)  # Add GROQ key frame to main layout

        # Image Upload Section
        self.image_upload_frame = QFrame()  # Frame to hold image upload elements
        self.image_layout = QHBoxLayout()
        self.image_upload_frame.setLayout(self.image_layout)
        self.image_label = QLabel("Image Upload:")  # Label for image upload
        self.image_label.setFont(QFont("Arial", 12))  # Set font for the label
        self.open_button = QPushButton("Upload Image")  # Button to upload image
        self.open_button.setStyleSheet(
            "padding: 10px; background-color: #90A4AE; color: #FFFFFF; font-weight: bold; border-radius: 5px;")
        self.open_button.clicked.connect(self.open_image)  # Connect button to function to open image
        self.image_layout.addWidget(self.image_label)  # Add label to layout
        self.image_layout.addWidget(self.open_button)  # Add button to layout
        self.main_layout.addWidget(self.image_upload_frame, 2, 0, 1, 2)  # Add image upload frame to main layout

        # Image Preview Area
        self.image_preview_label = QLabel("Image Preview Here")  # Label to show image preview
        self.image_preview_label.setAlignment(Qt.AlignCenter)  # Center-align the image preview
        self.image_preview_label.setStyleSheet(
            "border: 2px solid #B0BEC5; min-height: 200px; min-width: 400px; background-color: #FFFFFF; border-radius: 10px;")
        self.main_layout.addWidget(self.image_preview_label, 3, 0, 1, 2)  # Add image preview label to the layout

        # Image Query Section
        self.image_query_label = QLabel("Image Query:")  # Label for image query
        self.image_query_label.setFont(QFont("Arial", 12))  # Set font for the label
        self.image_query_input = QLineEdit()  # Input field for the image query
        self.image_query_input.setPlaceholderText("Enter your Image Query here")  # Placeholder text
        self.image_query_input.setMinimumHeight(50)  # Set minimum height for input field
        self.main_layout.addWidget(self.image_query_label, 4, 0, 1, 2)  # Add label to the layout
        self.main_layout.addWidget(self.image_query_input, 5, 0, 1, 2)  # Add input field to the layout

        # LLM Parameters Section (New sliders for Max Tokens, Temperature, Top P)
        self.llm_parameters_frame = QFrame()  # Frame to hold LLM parameters sliders
        self.llm_parameters_frame.setStyleSheet(
            "background-color: #F5F5F5; border: 1px solid #B0BEC5; padding: 10px; border-radius: 10px;")
        self.llm_parameters_layout = QVBoxLayout()
        self.llm_parameters_frame.setLayout(self.llm_parameters_layout)
        self.llm_parameters_label = QLabel("LLM Parameters:")
        self.llm_parameters_label.setFont(QFont("Arial", 11))
        self.llm_parameters_layout.addWidget(self.llm_parameters_label)

        # Max New Tokens Slider
        self.max_tokens_label = QLabel("Max New Tokens: 512")
        self.max_tokens_label.setFont(QFont("Arial", 9))
        self.llm_parameters_layout.addWidget(self.max_tokens_label)
        self.max_tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_slider.setSingleStep(5)
        self.max_tokens_slider.setMinimum(1)
        self.max_tokens_slider.setMaximum(1000)
        self.max_tokens_slider.setValue(512)
        self.max_tokens_slider.setToolTip(
            "Maximum length of the newly generated text. If explicitly set to None it will be the model's max context length minus input length. (Default: 512, 1 ≤ max_new_tokens ≤ 1000000)")
        self.max_tokens_slider.setStyleSheet(
            "QSlider::handle:horizontal { background-color: #78909C; border: 1px solid #5C6BC0; width: 20px; height: 20px; border-radius: 10px; box-shadow: 1px 1px 5px #555; }"
            "QSlider::groove:horizontal { height: 8px; background: #CFD8DC; border-radius: 4px; }"
            "QSlider::sub-page:horizontal { background: #5C6BC0; border-radius: 4px; }"
            "QSlider::handle:horizontal:hover { background-color: #5C6BC0; }"
        )
        self.max_tokens_slider.valueChanged.connect(
            lambda: self.max_tokens_label.setText(f"Max New Tokens: {self.max_tokens_slider.value()}"))
        self.llm_parameters_layout.addWidget(self.max_tokens_slider)

        # Temperature Slider
        self.temperature_label = QLabel("Temperature: 0.7")
        self.temperature_label.setFont(QFont("Arial", 9))
        self.llm_parameters_layout.addWidget(self.temperature_label)
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setSingleStep(1)
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(100)
        self.temperature_slider.setValue(70)
        self.temperature_slider.setToolTip(
            "Temperature to use for sampling. 0 means the output is deterministic. Values greater than 1 encourage more diversity (Default: 0.7, 0 ≤ temperature ≤ 1)")
        self.temperature_slider.setStyleSheet(
            "QSlider::handle:horizontal { background-color: #78909C; border: 1px solid #5C6BC0; width: 20px; height: 20px; border-radius: 10px; box-shadow: 1px 1px 5px #555; }"
            "QSlider::groove:horizontal { height: 8px; background: #CFD8DC; border-radius: 4px; }"
            "QSlider::sub-page:horizontal { background: #5C6BC0; border-radius: 4px; }"
            "QSlider::handle:horizontal:hover { background-color: #5C6BC0; }"
        )
        self.temperature_slider.valueChanged.connect(
            lambda: self.temperature_label.setText(f"Temperature: {self.temperature_slider.value() / 100}"))
        self.llm_parameters_layout.addWidget(self.temperature_slider)

        # Top P Slider
        self.top_p_label = QLabel("Top P: 0.9")
        self.top_p_label.setFont(QFont("Arial", 9))
        self.llm_parameters_layout.addWidget(self.top_p_label)
        self.top_p_slider = QSlider(Qt.Horizontal)
        self.top_p_slider.setSingleStep(1)
        self.top_p_slider.setMinimum(0)
        self.top_p_slider.setMaximum(100)
        self.top_p_slider.setValue(90)
        self.top_p_slider.setToolTip(
            "Sample from the set of tokens with highest probability such that sum of probabilities is higher than p. Lower values focus on the most probable tokens. Higher values sample more low-probability tokens (Default: 0.9, 0 < top_p ≤ 1)")
        self.top_p_slider.setStyleSheet(
            "QSlider::handle:horizontal { background-color: #78909C; border: 1px solid #5C6BC0; width: 20px; height: 20px; border-radius: 10px; box-shadow: 1px 1px 5px #555; }"
            "QSlider::groove:horizontal { height: 8px; background: #CFD8DC; border-radius: 4px; }"
            "QSlider::sub-page:horizontal { background: #5C6BC0; border-radius: 4px; }"
            "QSlider::handle:horizontal:hover { background-color: #5C6BC0; }"
        )
        self.top_p_slider.valueChanged.connect(
            lambda: self.top_p_label.setText(f"Top P: {self.top_p_slider.value() / 100}"))
        self.llm_parameters_layout.addWidget(self.top_p_slider)

        self.main_layout.addWidget(self.llm_parameters_frame, 0, 2, 6, 1)  # Place LLM Parameters to the right section

        # Submit and Clear Buttons Section
        self.button_layout = QHBoxLayout()  # Layout to hold buttons
        self.submit_button = QPushButton("Submit Query")  # Button to submit query
        self.submit_button.setStyleSheet(
            "padding: 10px; background-color: #78909C; color: #FFFFFF; font-weight: bold; border-radius: 5px;")
        self.submit_button.clicked.connect(self.submit_query)  # Connect button to function to submit query
        self.clear_button = QPushButton("Clear")  # Button to clear fields
        self.clear_button.setStyleSheet(
            "padding: 10px; background-color: #CFD8DC; color: #000000; font-weight: bold; border-radius: 5px;")
        self.clear_button.clicked.connect(self.clear_fields)  # Connect button to function to clear fields
        self.button_layout.addWidget(self.submit_button)  # Add submit button to layout
        self.button_layout.addWidget(self.clear_button)  # Add clear button to layout
        self.main_layout.addLayout(self.button_layout, 6, 0, 1, 2)  # Add button layout to the main layout

        self.output_text = QTextEdit()  # Text edit area for displaying LLM output
        self.output_text.setReadOnly(True)  # Set to read-only
        self.output_text.setMinimumHeight(150)  # Set minimum height
        self.output_text.setStyleSheet(
            "background-color: #FFFFFF; border: 2px solid #B0BEC5; border-radius: 10px; padding: 10px;")
        self.main_layout.addWidget(self.output_text, 7, 0, 1, 3)  # Add text edit to the layout

        self.setLayout(self.main_layout)

    # Function to handle image upload
    def open_image(self):
        options = QFileDialog.Options()  # Options for the file dialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.jpeg *.jpg);;All Files (*)", options=options)

        if file_path:
            try:
                # Load and display image in the preview label
                pixmap = QPixmap(file_path)
                self.image_preview_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.image_path = file_path  # Store the path of the uploaded image
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     f"Failed to load image: {str(e)}")  # Show error if image loading fails

    # Function to handle submitting the query to the LLM API
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
            with open(self.image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                # Get the values from the sliders
                max_tokens = self.max_tokens_slider.value()
                temperature = self.temperature_slider.value() / 100
                top_p = self.top_p_slider.value() / 100

                # Call LLM API and get the response
                output = self.call_llm_api(groq_key, base64_image, image_query, max_tokens, temperature, top_p)
                self.output_text.setPlainText(output)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process the image: {str(e)}")

    # Function to call the LLM API with the provided GROQ key, image, and query
    def call_llm_api(self, groq_key, base64_image, image_query, max_tokens, temperature, top_p):
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
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=False,
                stop=None,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            QMessageBox.critical(self, "API Error", f"Failed to get response from LLM API: {str(e)}")
            return ""

    # Function to clear all input fields and reset the UI
    def clear_fields(self):
        self.image_query_input.clear()  # Clear the image query input
        self.output_text.clear()  # Clear the LLM output text
        self.image_preview_label.clear()  # Clear the image preview label
        self.image_preview_label.setText("Image Preview Here")  # Reset the text in the image preview label
        if hasattr(self, 'image_path'):
            del self.image_path  # Delete the stored image path

        # Reset sliders to default values
        self.max_tokens_slider.setValue(512)
        self.temperature_slider.setValue(70)
        self.top_p_slider.setValue(90)


# Entry point for the application
if __name__ == "__main__":
    app = QApplication([])  # Create a new QApplication
    window = LlamafyVisionApp()  # Create an instance of the application
    window.show()  # Show the main window
    app.exec_()  # Execute the application