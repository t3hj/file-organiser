import os
import shutil
from datetime import datetime
from tqdm import tqdm
import re

def organize_files(directory):
    # Define the folder names for each file type
    folders = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'documents': {
            'word': ['.doc', '.docx'],
            'excel': ['.xls', '.xlsx'],
            'pdf': ['.pdf'],
            'text': ['.txt'],
            'ppt': ['.ppt', '.pptx']
        },
        'audio': ['.mp3', '.wav', '.aac'],
        'video': ['.mp4', '.mov', '.avi'],
        'archives': ['.zip', '.rar', '.tar', '.gz'],
        'scripts': ['.py', '.js', '.sh'],
        'installers': ['.exe', '.msi', '.dmg'],
        'setups': ['setup.exe', 'setup.msi']
    }

    # Create folders if they do not exist
    for folder in folders:
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Create 'duplicates' folder if it does not exist
    duplicates_folder = os.path.join(directory, 'duplicates')
    if not os.path.exists(duplicates_folder):
        os.makedirs(duplicates_folder)

    # Create 'others' folder if it does not exist
    others_folder = os.path.join(directory, 'others')
    if not os.path.exists(others_folder):
        os.makedirs(others_folder)

    def is_duplicate(file1, file2):
        # Remove common duplicate suffixes like (1), (2), etc.
        base1 = re.sub(r'\(\d+\)', '', file1)
        base2 = re.sub(r'\(\d+\)', '', file2)
        return base1.strip() == base2.strip()

    # Month names in short form
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Iterate over files in the directory with a progress bar
    for filename in tqdm(os.listdir(directory), desc="Organizing files"):
        file_path = os.path.join(directory, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Get file modification date
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        year_folder = mod_time.strftime('%Y')
        month_folder = month_names[int(mod_time.strftime('%m')) - 1]
        week_folder = f"Week-{mod_time.strftime('%U')}"
        
        date_folder_path = os.path.join(directory, year_folder, month_folder, week_folder)
        
        # Create date-based folders if they do not exist
        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)
        
        # Move files to appropriate folders based on extension
        moved = False
        for folder, extensions in folders.items():
            if isinstance(extensions, dict):  # Handle nested dictionaries for documents
                for subfolder, subextensions in extensions.items():
                    if any(filename.lower().endswith(ext) for ext in subextensions):
                        target_folder = os.path.join(date_folder_path, folder, subfolder)
                        if not os.path.exists(target_folder):
                            os.makedirs(target_folder)
                        target_path = os.path.join(target_folder, filename)
                        
                        # Handle duplicate files
                        if any(is_duplicate(filename, f) for f in os.listdir(target_folder)):
                            shutil.move(file_path, os.path.join(duplicates_folder, filename))
                        else:
                            shutil.move(file_path, target_path)
                        moved = True
                        break
                if moved:
                    break
            else:
                if any(filename.lower().endswith(ext) or filename.lower() == ext for ext in extensions):
                    target_folder = os.path.join(date_folder_path, folder)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    target_path = os.path.join(target_folder, filename)
                    
                    # Handle duplicate files
                    if any(is_duplicate(filename, f) for f in os.listdir(target_folder)):
                        shutil.move(file_path, os.path.join(duplicates_folder, filename))
                    else:
                        shutil.move(file_path, target_path)
                    moved = True
                    break
        
        # If file type is not recognized, move to 'others' folder
        if not moved:
            target_path = os.path.join(date_folder_path, 'others', filename)
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(os.path.dirname(target_path))
            
            # Handle duplicate files
            if any(is_duplicate(filename, f) for f in os.listdir(os.path.dirname(target_path))):
                shutil.move(file_path, os.path.join(duplicates_folder, filename))
            else:
                shutil.move(file_path, target_path)

# Example usage
organize_files(os.path.expanduser('~/Downloads'))
