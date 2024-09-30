# AI-Based-Police-Penal-Code-Detection-using-keywords-in-FIR-reports

## Overview
This Crime Detection App is an intelligent system designed to assist in identifying and categorizing criminal offenses based on user-provided descriptions. It utilizes natural language processing and machine learning techniques to match input descriptions with relevant crimes, their corresponding Indian Penal Code (IPC) sections, and other pertinent details.

## Features
- User-friendly GUI built with Tkinter
- Fuzzy matching for crime detection
- Semantic similarity analysis using spaCy
- Handling of specific crimes with additional constraints (e.g., group crimes, age-based classifications)
- Integration with a comprehensive crime dataset

## Dataset
The project includes a custom-built dataset (`crime_dataset_new.csv`) containing information about various crimes, including:
- Crime descriptions
- Corresponding IPC sections
- Weapons used (if applicable)
- Cognizable status

This dataset serves as the foundation for the app's crime detection capabilities.

## How It Works
1. Users input a description of an incident through the GUI.
2. The app processes the input using natural language processing techniques.
3. It performs both fuzzy matching and semantic similarity analysis to identify potential crimes.
4. For specific crimes (e.g., rape, dacoity, theft), the app may prompt for additional information.
5. The results, including matched crimes, IPC sections, and other relevant details, are displayed to the user.

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/rituraj1314/AI-Based-Police-Penal-Code-Detection-using-keywords-in-FIR-reports.git
   ```
2. Download the spaCy English model:
   ```
   python -m spacy download en_core_web_md
   ```

## Usage
Run the main script to start the application:
```
python newmain.py
```

## Legal Approval
This project has been reviewed and approved by a professional lawyer to ensure its compliance with legal standards and ethical considerations in the context of criminal law and data privacy.

## Disclaimer
This app is intended for informational purposes only and should not be considered as legal advice. Always consult with a qualified legal professional for specific legal matters.

## Contributing
Contributions to improve the app or expand the dataset are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.


## Contact
Rituraj Vijay Sharma
VIT Pune
