import pandas as pd
import random

# Crime data
crimes = [
    "Uttering words with deliberate intent to wound religious feelings",
    "Murder",
    "Causing of death by negligence",
    "Dowry death",
    "Thug ",
    "Causing Miscarriage",
    "Voluntarily causing grievous hurt by use of acid",
    "Causing hurt by act endangering life or personal safety of other",
    "Sexual harassment",
    "Stalking",
    "Kidnapping",
    "Rape",
    "Sexual intercourse by husband upon his wife during separation",
    "Theft",
    "Extortion",
    "Robbery",
    "Dacoity",
    "Dacoity,Murder",
    "Stolen property",
    "Cheating",
    "Mischief",
    "House-trespass",
    "House-breaking",
    "Forgery",
    "Making a false document",
    "Adultery",
    "Misconduct in public by a drunken person"
]

# Weapon data
weapons = [
    "",
    "knife",
    "gun",
    "ropes",
    "acid"
]

# Penal code data
penal_codes = [
    "298",
    "300",
    "304A",
    "304B",
    "310",
    "312",
    "326A",
    "337",
    "354A",
    "354D",
    "359",
    "375",
    "376B",
    "378",
    "383",
    "390",
    "391",
    "396",
    "410",
    "415",
    "425",
    "442",
    "445",
    "463",
    "464",
    "497",
    "510"
]

# FIR Launched by data for specific crimes
female_names = [
    "Priya", "Neha", "Sneha", "Anita", "Riya", "Sonia", "Pooja", "Meena", "Jyoti",
    "Shweta", "Kavita", "Kiran", "Suman", "Rani", "Smita", "Aarti", "Kajal", "Mona",
    "Divya", "Sapna","Poonam", "Tina","Rashmi"
]

# Random names for FIR Launched by (gender: Male or Transgender)
random_names = [
    "Ramesh", "Suresh", "Ajay", "Kailash", "Prem", "Sameer",
    "Anand", "Milind", "Abhay", "Lakshay", "Vaibhav", "Arijit", "Atif", "Aslam",
    "Mustufa", "Atharva", "Parag", "Neeraj", "Dheeraj", "Sujoy", "Ajit", "Rohit",
    "Virat", "Sachin", "Mahendra", "Sunil", "Amar", "Prasad", "Vineet", "Shantanu",  "Debashish",
    "Navjot", "Parthiv", "Riyan","Abdul","Sujal","Arya","Soham","Om","Atharva"
]

# Weapon data for specific crimes
weapons_for_murder = ["knife", "gun", "ropes"]
weapons_for_thug = ["knife", "gun", "ropes"]
weapons_home = [
    "hammer","stones","rod","hockey stick",
]
locations = ["Katraj", "Chintamani I","Chintamani II","Chintamani III","Dolphin Chowk","Bibwewadi Gavthan",
             "Mahesh Society","Swargate","City Pride","Sukhsagar Nagar","KK Market","Shani Mandir","Khau Gali"]


# Generate dataset
data = []
for _ in range(5000):
    penal_code = random.choice(penal_codes)
    crime = crimes[penal_codes.index(penal_code)]

    # Randomly assign weapon for murder and thug crimes
    if "Murder" in crime:
        weapon = random.choice(weapons_for_murder)
        cognizable = True
    elif "Thug" in crime:
        weapon = random.choice(weapons_for_thug)
        cognizable = True
    elif "Extortion" in crime:
        weapon = random.choice(weapons[1:4])
        cognizable = True
    elif "Kidnapping" in crime:
        weapon = random.choice(weapons[1:4])
        cognizable = True
    elif "Dacoity + Murder" in crime:
        weapon = random.choice(weapons[1:4]) 
        cognizable = True   
    elif "Robbery" in crime:
        weapon = random.choice(weapons[1:4])
        cognizable = True
    elif "House-breaking" in crime:
        weapon = random.choice(weapons_home[0:4])
        cognizable = True
    elif penal_code == "326A":
        weapon = "acid"
    elif penal_code == "337":
        weapon = random.choice(weapons[1:4])
        cognizable = True
    else:
        weapon = ""
        cognizable = crime in ["Theft", "Rape", "Kidnapping", "Dowry death", "Murder"]

    # Random age and gender
    age = random.randint(16, 75)
    gender = ""

    # Random time and date
    time = f"{random.randint(0, 23)}:{random.randint(0, 59)}"
    date = f"{random.randint(1, 31)}/{random.randint(1, 12)}/{random.randint(2020, 2023)}"

    # FIR Launched by for specific crimes
    if age <= 18:
        fir_launched_by = ""
    elif any(c in crime for c in ["Dowry", "Causing Miscarriage", "Sexual harassment", "Stalking", "Rape"]):
        fir_launched_by = random.choice(female_names)
        gender = "Female"
    else:
        fir_launched_by = random.choice(random_names)
        gender = "Male" if random.choice([True, False]) else "Male"

    location = random.choice(locations)
    
    data.append([penal_code, crime, weapon, age, gender, cognizable, time, date, location, fir_launched_by])

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=["Penal Code", "Crime", "Weapon Used", "Age", "Gender", "Cognizable", "Time", "Date", "Location", "FIR Launched by"])
df