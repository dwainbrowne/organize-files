import os

def delete_word_documents(folder_path):
    # Define the file extensions for Word documents
    word_extensions = ['.doc', '.docx']
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if the file is a Word document
            if os.path.isfile(file_path) and os.path.splitext(filename)[1] in word_extensions:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    # Replace with the path to your folder
    folder_path = r'C:\Users\DwainBrowne\OneDrive - SnapSuite\2024\snapsuite\data-backup\storage\main\ss-p'
    
    # Call the function to delete Word documents
    delete_word_documents(folder_path)
