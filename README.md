# File Organizer for Manuals

This repository contains a Python script designed to organize PDF manuals into categorized folders based on their content. It utilizes the OpenAI API to analyze and categorize PDF documents, ensuring that each manual is placed in the correct directory for easy access and management.

## Features

- **PDF Analysis**: Leverages the OpenAI API to understand and categorize PDF content.
- **Automatic Categorization**: Organizes PDF files into predefined categories such as Cranes, Excavators, Bulldozers, and more.
- **Logging**: Includes logging functionality to track the process and outcomes of the file organization.

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.x
- OpenAI Python package
- PyPDF2
- pdf2image

Additionally, you will need an OpenAI API key to use the OpenAI services.

## Installation

1. Clone the repository to your local machine.
2. Install the required Python packages using pip:

```bash
pip install openai PyPDF2 pdf2image
