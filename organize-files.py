import os
import openai
import logging
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import io
import base64

# Set your OpenAI API key
openai.api_key = "YOUR OPEN API KEY HERE"

# Base directory where files are located
base_dir = r"C:\Users\DwainBrowne\OneDrive - comtech.repair\Documents\_MANUALS"

# Base directory where categorized folders will be created
output_base_dir = r"C:\Users\DwainBrowne\OneDrive - comtech.repair\Documents\_MANUALS"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Categories and folder paths
categories = {
    "CRANES": "_CRANES",
    "EXCAVATORS (ABOVE 135)": "_EXCAVATORS_ABOVE_135",
    "BULLDOZERS": "_BULLDOZERS",
    "GRADERS": "_GRADERS",
    "WHEEL LOADERS": "_WHEEL_LOADERS",
    "TRACK LOADERS": "_TRACK_LOADERS",
    "BIG ROLLERS": "_BIG_ROLLERS",
    "PILE DRIVERS": "_PILE_DRIVERS",
    "ASPHALT PAVERS": "_ASPHALT_PAVERS",
    "WHEEL EXCAVATORS": "_WHEEL_EXCAVATORS",
    "BACKHOES": "_BACKHOES",
    "SKID STEERS": "_SKID_STEERS",
    "EXCAVATORS (UP TO 95)": "_EXCAVATORS_UP_TO_95",
    "MANLIFTS (80FT)": "_MANLIFTS_80FT",
    "TELEHANDLERS (FORKLIFT)": "_TELEHANDLERS_FORKLIFT",
    "COMPACT TRACK LOADERS": "_COMPACT_TRACK_LOADERS",
    "ROUGH TERRAIN FORKLIFTS": "_ROUGH_TERRAIN_FORKLIFTS",
    "FORKLIFT": "_FORKLIFT",
    "MANLIFTS (BELOW 80FT)": "_MANLIFTS_BELOW_80FT",
    "SCISSOR LIFTS": "_SCISSOR_LIFTS",
    "TRUCKS": "_TRUCKS",
    "SMALL ROLLERS": "_SMALL_ROLLERS",
    "BOOM LIFTS": "_BOOM_LIFTS",
    "TOWABLE LIFTS": "_TOWABLE_LIFTS",
    "UTILITY VEHICLES": "_UTILITY_VEHICLES",
    "SMALL DUMPERS": "_SMALL_DUMPERS",
    "COMPACT WHEEL LOADERS": "_COMPACT_WHEEL_LOADERS",
    "LIGHT TOWERS": "_LIGHT_TOWERS",
    "UNKNOWN_CATEGORY": "_UNKNOWN_CATEGORY"
}

def categorize_file(file_name):
    """Categorize based on the file name."""
    file_name_lower = file_name.lower()
    if "excavator" in file_name_lower:
        if "180lc" in file_name_lower or "135" in file_name_lower:
            return "EXCAVATORS (ABOVE 135)"
        return "EXCAVATORS (UP TO 95)"
    if "wheel loader" in file_name_lower:
        return "WHEEL LOADERS"
    if "truck" in file_name_lower or "mack" in file_name_lower or "cummins" in file_name_lower:
        return "TRUCKS"
    if "bulldozer" in file_name_lower:
        return "BULLDOZERS"
    if "grader" in file_name_lower:
        return "GRADERS"
    if "roller" in file_name_lower:
        if "big" in file_name_lower:
            return "BIG ROLLERS"
        return "SMALL ROLLERS"
    if "pile driver" in file_name_lower:
        return "PILE DRIVERS"
    if "paver" in file_name_lower:
        return "ASPHALT PAVERS"
    if "backhoe" in file_name_lower:
        return "BACKHOES"
    if "skid steer" in file_name_lower:
        return "SKID STEERS"
    if "manlift" in file_name_lower:
        if "80ft" in file_name_lower:
            return "MANLIFTS (80FT)"
        return "MANLIFTS (BELOW 80FT)"
    if "telehandler" in file_name_lower or "forklift" in file_name_lower:
        return "TELEHANDLERS (FORKLIFT)"
    if "compact track loader" in file_name_lower:
        return "COMPACT TRACK LOADERS"
    if "rough terrain forklift" in file_name_lower:
        return "ROUGH TERRAIN FORKLIFTS"
    if "scissor lift" in file_name_lower:
        return "SCISSOR LIFTS"
    if "boom lift" in file_name_lower:
        return "BOOM LIFTS"
    if "towable lift" in file_name_lower:
        return "TOWABLE LIFTS"
    if "utility vehicle" in file_name_lower:
        return "UTILITY VEHICLES"
    if "small dumper" in file_name_lower:
        return "SMALL DUMPERS"
    if "compact wheel loader" in file_name_lower:
        return "COMPACT WHEEL LOADERS"
    if "light tower" in file_name_lower:
        return "LIGHT TOWERS"
    return None

def get_text_from_pdf(pdf_path):
    """Extract text from the first 20 pages of a PDF file."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            text = ""
            for page_num in range(min(20, len(reader.pages))):  # Read up to 20 pages
                page = reader.pages[page_num]
                text += page.extract_text() or ""
            return text
    except Exception as e:
        logging.error(f"Failed to read PDF file {pdf_path}: {e}")
        return ""

def convert_pdf_to_image(pdf_path):
    """Convert the first page of a PDF to an image and return as bytes."""
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            img_byte_arr = io.BytesIO()
            images[0].save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            return img_byte_arr
        return None
    except Exception as e:
        logging.error(f"Failed to convert PDF to image {pdf_path}: {e}")
        return None

def get_category_from_content(content):
    """Use OpenAI to categorize the content of a PDF file."""
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"Categorize the following text into one of the given categories: {list(categories.keys())}."
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response.choices[0].message.content.strip().upper()
    except Exception as e:
        logging.error(f"Failed to get category from content: {e}")
        return None

def get_category_from_image(image_bytes):
    """Use OpenAI to categorize the content of an image of a PDF."""
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Categorize the following image into one of the given categories."
                },
                {
                    "role": "user",
                    "content": f"Categories: {list(categories.keys())}"
                }
            ],
            functions=[{
                "name": "image",
                "arguments": {"image": base64.b64encode(image_bytes).decode('utf-8')}
            }]
        )
        return response.choices[0].message.content.strip().upper()
    except Exception as e:
        logging.error(f"Failed to get category from image: {e}")
        return None

def move_files():
    """Move files to categorized folders based on their names or content."""
    for root, dirs, files in os.walk(base_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            category = categorize_file(file_name)
            if not category and file_name.endswith(".pdf"):
                content = get_text_from_pdf(file_path)
                category = get_category_from_content(content)
                if not category:
                    image_bytes = convert_pdf_to_image(file_path)
                    if image_bytes:
                        category = get_category_from_image(image_bytes)
            if not category:
                category = "UNKNOWN_CATEGORY"
            category = category.replace("'", "").strip()  # Ensure no extra quotes or whitespace
            if category not in categories:
                category = "UNKNOWN_CATEGORY"
            category_dir = os.path.join(output_base_dir, categories[category])
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            try:
                os.rename(file_path, os.path.join(category_dir, file_name))
                logging.info(f"Moved {file_name} to {category_dir}")
            except Exception as e:
                logging.error(f"Failed to move file {file_name}: {e}")

if __name__ == "__main__":
    move_files()
