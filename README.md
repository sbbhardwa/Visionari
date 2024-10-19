# Visionari

****Visionari - Simple tool based on llama vision ****


![image](https://github.com/user-attachments/assets/de5e5b36-6624-49eb-b809-073a346b98d5)


Visionari is an AI-powered desktop application designed to analyze images and generate insightful responses based on user queries. Built using PyQt5 for the GUI, this application interacts with the Groq API for LLM (Large Language Model) capabilities, providing users with intuitive and interactive image analysis features.
Features

•	Image Upload and Preview: Upload images directly through the application and preview them in the GUI.
•	AI-Powered Analysis: Submit questions about uploaded images and receive detailed responses from a language model.
•	User-Friendly Interface: Modern, intuitive interface built with PyQt5, including professional touches and customization.
•	Open Source: Licensed under GPLv3, Visionari is open for contribution and enhancement by the community.


**New Features: Enhanced LLM Parameters UI**

Max New Tokens Slider: Allows users to set the maximum length of the generated text. This is now equipped with a detailed tooltip explaining its functionality and a 3D visual effect for better interaction.

Tooltip: "Maximum length of the newly generated text. If explicitly set to None, it will be the model's max context length minus input length. (Default: 512, 1 ≤ max_new_tokens ≤ 1000000)"

Temperature Slider: Controls the randomness of the output. A tooltip has been added for a better understanding of this parameter, and the slider has a smooth movement with an improved visual style.

Tooltip: "Temperature to use for sampling. 0 means the output is deterministic. Values greater than 1 encourage more diversity. (Default: 0.7, 0 ≤ temperature ≤ 1)"

Top P Slider: Provides control over the sampling strategy by choosing from the highest probability tokens. This slider also includes a tooltip and improved visuals for a more intuitive user experience.

Tooltip: "Sample from the set of tokens with the highest probability such that the sum of probabilities is higher than p. Lower values focus on the most probable tokens. Higher values sample more low-probability tokens. (Default: 0.9, 0 < top_p ≤ 1)"

**Installation**
To get started with Visionari, clone the repository and install the required dependencies.
Prerequisites

•	Python 3.7 or higher
•	Groq Python SDK (for interacting with the Groq API)
•	PyQt5 for GUI elements

**Installation Steps**
1.	Clone the repository:
2.	Install dependencies: Install the necessary Python libraries using pip:
Example requirements.txt:
3.	Run the application:

**Usage**
1.	GROQ API Key: Enter your GROQ API key to allow the app to interact with the AI model.
2.	Image Upload: Use the "Upload Image" button to select an image from your local device.
3.	Submit Query: Enter your query about the image and press "Submit Query". The AI will analyze the image and respond accordingly.
4.	Clear Fields: Use the "Clear" button to reset the image, output, and query fields.
Development

If you want to contribute to Visionari, feel free to fork the repository and make your improvements. You can submit pull requests for new features, bug fixes, or other enhancements.
Contribution Guidelines
•	Fork the repository.
•	Create a feature branch.
•	Commit your changes.
•	Open a pull request for review.
Please ensure that your changes follow

