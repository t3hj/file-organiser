import os
import shutil
from datetime import datetime
from tqdm import tqdm
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def organize_files(directory, delete_empty_folders=False, progress_callback=None):
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

    # Month names in short form with numeric prefix
    month_names = ["01 - Jan", "02 - Feb", "03 - Mar", "04 - Apr", "05 - May", "06 - Jun", "07 - Jul", "08 - Aug", "09 - Sep", "10 - Oct", "11 - Nov", "12 - Dec"]

    def organize_directory(current_directory):
        # Iterate over files and directories in the current directory with a progress bar
        for filename in tqdm(os.listdir(current_directory), desc=f"Organizing files in {current_directory}"):
            file_path = os.path.join(current_directory, filename)
            
            # Recursively organize subdirectories
            if os.path.isdir(file_path):
                organize_directory(file_path)
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

            # Update progress bar
            if progress_callback:
                progress_callback()

        # Delete empty folders if the option is enabled
        if delete_empty_folders:
            for root, dirs, files in os.walk(current_directory, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)

    organize_directory(directory)

# GUI setup
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        delete_empty_folders = messagebox.askyesno("Delete Empty Folders", "Do you want to delete empty folders after organizing?")
        organize_files(directory, delete_empty_folders, update_progress)
        messagebox.showinfo("Success", "Files organized successfully!")

def update_progress():
    progress_bar.step(1)
    root.update_idletasks()

def create_gui():
    global root, progress_bar
    root = tk.Tk()
    root.title("File Organizer")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Select a directory to organize:")
    label.pack(pady=5)

    select_button = tk.Button(frame, text="Select Directory", command=select_directory)
    select_button.pack(pady=5)

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
