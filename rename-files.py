import os
import re
import random
import string

# Specify the directory containing the files
directory = r'C:\Users\DwainBrowne\OneDrive - comtech.repair\Documents\_MANUALS'

# List of valid and invalid words
valid_words = [
    'Excavator', 'Excavators', 'Service', 'Repair', 'Factory', 'Truck', 'Trucks', 'Heavy', 'Duty', 'Equipment', 'Crawler'
]
invalid_words = [
    'download', 'raw', 'instant', 'phpapp','downloads','unknown'
]

def clean_file_name(file_name):
    # Remove special characters
    cleaned_name = re.sub(r'[^A-Za-z0-9_\-\.]', '', file_name)
    # Replace underscores with hyphens
    cleaned_name = cleaned_name.replace('_', '-')
    # Split the name and extension
    name, ext = os.path.splitext(cleaned_name)
    # Split the name into words
    words = name.split('-')
    # Filter the words to keep only valid words and remove invalid ones
    filtered_words = [
        word.title() for word in words
        if (any(vw.lower() == word.lower() for vw in valid_words) or not any(iw.lower() == word.lower() for iw in invalid_words))
    ]
    # Reconstruct the name with filtered words
    cleaned_name = '-'.join(filtered_words)
    # Ensure the extension is lower case
    ext = ext.lower()
    # Remove leading hyphens
    cleaned_name = re.sub(r'^-+', '', cleaned_name)
    # Remove multiple consecutive hyphens
    cleaned_name = re.sub(r'-+', '-', cleaned_name)
    # Ensure there is no extra "Manual" or "Pdf"
    cleaned_name = re.sub(r'Manual', '', cleaned_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r'Pdf', '', cleaned_name, flags=re.IGNORECASE)
    # Combine the cleaned name and extension with "-Manual.pdf"
    cleaned_name = f'{cleaned_name.strip("-")}-Manual.pdf'
    return cleaned_name

def generate_random_suffix(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def rename_files_in_directory(directory):
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            new_name = clean_file_name(file_name)
            old_file = os.path.join(directory, file_name)
            new_file = os.path.join(directory, new_name)
            # If the new file name already exists, append a random suffix
            while os.path.exists(new_file):
                suffix = generate_random_suffix()
                name, ext = os.path.splitext(new_name)
                new_file = os.path.join(directory, f'{name}-{suffix}{ext}')
            os.rename(old_file, new_file)
            print(f'Renamed: {file_name} to {new_file}')

# Call the function to rename files
rename_files_in_directory(directory)
