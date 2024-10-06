from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QLineEdit, QMessageBox, QFrame
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
        self.setGeometry(100, 100, 700, 900)  # Set window position and size
        self.setStyleSheet("background-color: #EAEAEA;")  # Set neutral background color
        self.setWindowIcon(QIcon("vision.png"))  # Set the window icon

        # Main layout for the application
        self.layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Visionari - AI Image Analysis Tool")
        self.title_label.setAlignment(Qt.AlignCenter)  # Center-align the title label
        self.title_label.setStyleSheet(
            "background-color: #B0BEC5; padding: 15px; font-size: 24px; font-weight: bold; color: #FFFFFF; border-radius: 10px;")
        self.layout.addWidget(self.title_label)  # Add title label to the layout

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
        self.layout.addWidget(self.groq_key_frame)  # Add GROQ key frame to main layout

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
        self.layout.addWidget(self.image_upload_frame)  # Add image upload frame to main layout

        # Image Preview Area
        self.image_preview_label = QLabel("Image Preview Here")  # Label to show image preview
        self.image_preview_label.setAlignment(Qt.AlignCenter)  # Center-align the image preview
        self.image_preview_label.setStyleSheet(
            "border: 2px solid #B0BEC5; min-height: 200px; min-width: 400px; background-color: #FFFFFF; border-radius: 10px;")
        self.layout.addWidget(self.image_preview_label)  # Add image preview label to the layout

        # Image Query Section
        self.image_query_label = QLabel("Image Query:")  # Label for image query
        self.image_query_label.setFont(QFont("Arial", 12))  # Set font for the label
        self.image_query_input = QLineEdit()  # Input field for the image query
        self.image_query_input.setPlaceholderText("Enter your Image Query here")  # Placeholder text
        self.image_query_input.setMinimumHeight(50)  # Set minimum height for input field
        self.layout.addWidget(self.image_query_label)  # Add label to the layout
        self.layout.addWidget(self.image_query_input)  # Add input field to the layout

        # LLM Output Section
        self.output_label = QLabel("LLM Output:")  # Label for LLM output
        self.output_label.setFont(QFont("Arial", 12))  # Set font for the label
        self.output_label.setStyleSheet(
            "background-color: #B0BEC5; padding: 5px; color: #FFFFFF; font-weight: bold; border-radius: 5px;")
        self.layout.addWidget(self.output_label)  # Add label to the layout
        self.output_text = QTextEdit()  # Text edit area for displaying LLM output
        self.output_text.setReadOnly(True)  # Set to read-only
        self.output_text.setMinimumHeight(300)  # Set minimum height
        self.output_text.setStyleSheet(
            "background-color: #FFFFFF; border: 2px solid #B0BEC5; border-radius: 10px; padding: 10px;")
        self.layout.addWidget(self.output_text)  # Add text edit to the layout

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
        self.layout.addLayout(self.button_layout)  # Add button layout to the main layout

        self.setLayout(self.layout)  # Set the main layout

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
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")  # Show error if image loading fails

    # Function to handle submitting the query to the LLM API
    def submit_query(self):
        groq_key = self.groq_key_input.text()  # Get GROQ API key from input field
        image_query = self.image_query_input.text()  # Get image query from input field

        # Check if GROQ key is provided
        if not groq_key:
            QMessageBox.warning(self, "Input Error", "Please enter a valid GROQ Key.")
            return

        # Check if image is uploaded
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "Input Error", "Please upload an image.")
            return

        # Check if image query is provided
        if not image_query or image_query == "Enter your Image Query here":
            QMessageBox.warning(self, "Input Error", "Please enter a valid image query.")
            return

        try:
            # Encode image to base64 for API submission
            with open(self.image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                # Call LLM API and get the response
                output = self.call_llm_api(groq_key, base64_image, image_query)
                self.output_text.setPlainText(output)  # Display the output in the text area
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process the image: {str(e)}")  # Show error if processing fails

    # Function to call the LLM API with the provided GROQ key, image, and query
    def call_llm_api(self, groq_key, base64_image, image_query):
        try:
            client = Groq(api_key=groq_key)  # Initialize Groq client with the provided API key
            # Make a request to the LLM API
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
            return chat_completion.choices[0].message.content  # Return the content from the API response
        except Exception as e:
            QMessageBox.critical(self, "API Error", f"Failed to get response from LLM API: {str(e)}")  # Show error if API call fails
            return ""

    # Function to clear all input fields and reset the UI
    def clear_fields(self):
        self.image_query_input.clear()  # Clear the image query input
        self.output_text.clear()  # Clear the LLM output text
        self.image_preview_label.clear()  # Clear the image preview label
        self.image_preview_label.setText("Image Preview Here")  # Reset the text in the image preview label
        if hasattr(self, 'image_path'):
            del self.image_path  # Delete the stored image path

# Entry point for the application
if __name__ == "__main__":
    app = QApplication([])  # Create a new QApplication
    window = LlamafyVisionApp()  # Create an instance of the application
    window.show()  # Show the main window
    app.exec_()  # Execute the application