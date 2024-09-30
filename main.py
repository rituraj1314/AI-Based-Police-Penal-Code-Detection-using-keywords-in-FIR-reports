import spacy
import pandas as pd
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
import nltk
from difflib import get_close_matches
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from ttkthemes import ThemedStyle

nltk.download('punkt')

# Load a pre-trained spaCy model
nlp = spacy.load("en_core_web_md")
# Load your dataset from a CSV file (replace 'crime_data.csv' with your dataset path)
df = pd.read_csv("E:/VIT/TY/SEM5/EDI/Dataset/crime_dataset_new (1).csv")

# Initialize matched information list
matched_info = []

# Tokenize input words
input_words = []

# Define a dictionary for specific crimes and their corresponding penal codes
specific_crimes = {
    'rape': '376D',
    'dacoity': '400',
    'theft': '401',
}

# Function to get user input
def get_user_input():
    global input_words, age_asked, group_crime

    # Get user input for the description
    input_text = simpledialog.askstring("Input", "Enter the description of the incident:")

    # Reset variables for a new input
    input_words = []
    age_asked = False
    group_crime = None

    # Process the input
    process_input(input_text, df["Crime"].str.lower().unique())

# Function to handle specific crimes with additional constraints
def handle_specific_crime(crime, group_crime, age=None):
    if crime.lower() == 'rape':
        if group_crime == 'yes':
            if age is not None:
                if age < 12:
                    return '376DB', 'TRUE'
                elif age < 16:
                    return '376DA', 'TRUE'
                else:
                    return '376D', 'TRUE'
            else:
                return None, None  # Age not provided, return None
        else:
            return '376D', 'TRUE'  # Default if not a group crime

    elif crime.lower() == 'dacoity':
        if group_crime == 'yes':
            return '400', 'TRUE'
        else:
            return None, None  # Return None if not a group crime

    elif crime.lower() == 'theft':
        if group_crime == 'yes':
            return '401', 'TRUE'
        else:
            return None, None  # Return None if not a group crime

# Function to process user input
def process_input(input_text, crime_dataset):
    global input_words, age_asked, group_crime, specific_crimes

    # Correct spelling mistakes using get_close_matches
    corrected_input_words = []
    for word in word_tokenize(input_text.lower()):
        closest_match = get_close_matches(word, df['Crime'].str.lower(), n=1)
        corrected_input_words.append(closest_match[0] if closest_match else word)

    corrected_input_text = ' '.join(corrected_input_words)
    input_words = word_tokenize(corrected_input_text)

    # Initialize group_crime
    group_crime = None

    # Iterate over the dataset
    for index, row in df.iterrows():
        crime = row['Crime']
        weapon = row['Weapon Used']
        cognizable = row['Cognizable']  # Add Cognizable column

        # Calculate fuzzy partial ratio similarity for crime and weapon
        crime_similarity = fuzz.partial_ratio(crime.lower(), corrected_input_text.lower())
        weapon_similarity = fuzz.partial_ratio(weapon.lower(), corrected_input_text.lower()) if not pd.isna(weapon) else 0

        # Define a threshold for matching
        matching_threshold = 97  # Adjust this threshold as needed

        # Check if similarity meets the threshold
        if crime_similarity >= matching_threshold or weapon_similarity >= matching_threshold:
            penal_code = row['Penal Code']

            # Check if the crime is a specific crime with additional constraints
            if crime.lower() in specific_crimes:
                if crime.lower() == 'rape' and not age_asked:
                    if group_crime is None:
                        group_crime = simpledialog.askstring("Input", "Is this a group crime? (yes/no): ").lower()
                    age = None
                    if group_crime == 'yes':
                        age = int(simpledialog.askstring("Input", "What was the age of the victim? "))
                    age_asked = True
                    penal_code, cognizable_status = handle_specific_crime(crime, group_crime, age)
                elif crime.lower() != 'rape':
                    if group_crime is None:
                        group_crime = simpledialog.askstring("Input", "Is this a group crime? (yes/no): ").lower()
                    penal_code, cognizable_status = handle_specific_crime(crime, group_crime)

                if penal_code:
                    matched_info.append((crime, weapon, penal_code, cognizable_status if cognizable_status else cognizable))
            else:
                matched_info.append((crime, weapon, penal_code, cognizable))

    # Remove duplicates from matched_info
    unique_matched_info = []
    seen_penal_codes = set()

    for info in matched_info:
        crime, weapon, penal_code, cognizable = info
        if penal_code not in seen_penal_codes:
            unique_matched_info.append(info)
            seen_penal_codes.add(penal_code)

    # Detect Crimes using semantic similarity
    detected_crimes = []

    # Process user input with spaCy
    doc = nlp(corrected_input_text)

    # Detect Crimes
    for token in doc:
        if token.text in crime_dataset:
            detected_crimes.append(token.text)

    # Find similar words using spaCy's semantic similarity
    for token in doc:
        for word in crime_dataset:
            similarity = nlp(token.text).similarity(nlp(word))
            if similarity >= 0.90:  # Adjust the threshold as needed
                detected_crimes.append(word)

    # Combine fuzzy matched crimes and semantically similar crimes
    detected_crimes = list(set(detected_crimes))

    # Display matched crimes
    if unique_matched_info:
        result_text = "Fuzzy Matches found:\n"
        for info in unique_matched_info:
            crime, weapon, penal_code, cognizable = info
            if weapon:
                result_text += f"For Crime: {crime}, Weapon: {weapon}, Penal Code: {penal_code}, Cognizable: {cognizable}\n"
            else:
                result_text += f"For Crime: {crime}, Penal Code: {penal_code}, Cognizable: {cognizable}\n"

    if detected_crimes:
        result_text += "\nSemantic Matches found:\n"
        for crime in detected_crimes:
            # Check if the detected crime is in the dataset
            if crime in crime_dataset:
                # Look up the penal code, weapon, and cognizable status in the dataset
                row = df[df["Crime"].str.lower() == crime].iloc[0]
                penal_code = row["Penal Code"]
                weapon = row["Weapon Used"]
                cognizable = row["Cognizable"]
                result_text += f"For Crime: {crime}, Weapon: {weapon}, Penal Code: {penal_code}, Cognizable: {cognizable}\n"
            # Handle specific crimes not in the dataset
            elif crime.lower() in specific_crimes:
                specific_penal_code, cognizable_status = handle_specific_crime(crime, group_crime, age)
                if specific_penal_code:
                    result_text += f"For Crime: {crime}, Penal Code: {specific_penal_code}, Cognizable: {cognizable_status}\n"
            else:
                result_text += f"For Crime: {crime}, Penal Code: Not Found, Weapon: Not Found, Cognizable: Not Found\n"

    if not unique_matched_info and not detected_crimes:
        result_text = "No matching crimes found for the given description."

    # Display the result in a message box
    messagebox.showinfo("Result", result_text)

# Create a Tkinter window
root = tk.Tk()
root.title("Crime Detection App")

# Button to trigger user input
input_button = tk.Button(root, text="Get User Input", command=get_user_input)
input_button.pack()

# Start the Tkinter event loop
root.mainloop()
