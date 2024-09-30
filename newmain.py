import spacy
import pandas as pd
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
import nltk
from difflib import get_close_matches
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ttkthemes import ThemedStyle

nltk.download('punkt')

# Load a pre-trained spaCy model
nlp = spacy.load("en_core_web_md")

# Load your dataset from a CSV file (replace 'crime_data.csv' with your dataset path)
df = pd.read_csv("E:/VIT/TY/SEM5/EDI/Dataset/crime_dataset_new (1).csv")

# Define a dictionary for specific crimes and their corresponding penal codes
specific_crimes = {
    'rape': '376D',
    'dacoity': '400',
    'theft': '401',
}

# Initialize matched information list
matched_info = []

# Tokenize input words
input_words = []

# Global variables for user input
age_asked = False
group_crime = None

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
    global input_words, age_asked, group_crime, specific_crimes, matched_info

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
        weapon_similarity = fuzz.partial_ratio(weapon.lower(), corrected_input_text.lower()) if not pd.isna(
            weapon) else 0

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
                    matched_info.append(
                        (crime, weapon, penal_code, cognizable_status if cognizable_status else cognizable))
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
    result_text = ""

    if unique_matched_info or detected_crimes:
        result_text += "Matches found:\n\n"

        if unique_matched_info:
            result_text += "Fuzzy Matches:\n"
            for info in unique_matched_info:
                crime, weapon, penal_code, cognizable = info
                if weapon:
                    result_text += f"For Crime: {crime}, Weapon: {weapon}, Penal Code: {penal_code}, Cognizable: {cognizable}\n"
                else:
                    result_text += f"For Crime: {crime}, Penal Code: {penal_code}, Cognizable: {cognizable}\n"

        if detected_crimes:
            result_text += "\nSemantic Matches:\n"
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
    else:
        result_text = "No matching crimes found for the given description."

    # Update the result label
    result_label.config(text=result_text)

# Create a Tkinter window
root = tk.Tk()
root.title("Crime Detection App")

# Apply a themed style for a modern look
style = ThemedStyle(root)
style.set_theme("plastik")  # Choose the theme (you can explore other themes)

# Create and style widgets
frame = ttk.Frame(root, padding="20", style="My.TFrame")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

title_label = ttk.Label(frame, text="Crime Detection App", font=("Arial", 16), style="My.TLabel")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Input Text Entry
input_text_entry = tk.Text(frame, height=5, width=50, wrap=tk.WORD)
input_text_entry.grid(row=1, column=0, columnspan=2, pady=(10, 20))

# Get User Input Button
get_input_button = ttk.Button(frame, text="Get User Input", command=get_user_input, style="My.TButton")
get_input_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))

# Crime Text Entry
crime_text_entry = tk.Text(frame, height=5, width=50, wrap=tk.WORD)
crime_text_entry.grid(row=3, column=0, columnspan=2, pady=(10, 20))

# Get Crime Input Button
get_crime_input_button = ttk.Button(frame, text="Get Crime Input", command=get_crime_input, style="My.TButton")
get_crime_input_button.grid(row=4, column=0, columnspan=2, pady=(10, 20))

# Result Label
result_label = ttk.Label(frame, text="", font=("Arial", 12), wraplength=400, justify=tk.LEFT, style="My.TLabel")
result_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

# Define custom styles
style.configure("My.TFrame", background="#4CAF50")
style.configure("My.TLabel", background="#4CAF50", foreground="#FFFFFF")
style.configure("My.TButton", background="#FF5722", foreground="#FFFFFF")

# Start the Tkinter event loop
root.mainloop()