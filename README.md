# 📂 File Organizer Bot

Welcome to the File Organizer Bot! This bot helps you organize your files by sorting them into appropriate folders based on their extensions, creation dates, and more. 🚀

## Features

- 📅 **Date-Based Sorting**: Organizes files by year, month (short form), and week.
- 📄 **Document Organization**: Further categorizes documents into Word, Excel, PDF, Text, and PPT.
- 🗃️ **Installer and Setup Files**: Separates installer and setup files into dedicated folders.
- 🔄 **Duplicate Handling**: Detects and handles duplicate files accurately.
- 📊 **Progress Bar**: Displays a progress bar during the organization process.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/t3hj/file-organiser.git
   cd file-organiser
   ```

2. **Create a virtual environment** (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the script**:
   ```sh
   python main.py
   ```

2. **Organize your files**:
   The script will organize files in your Downloads directory by default. You can modify the path in the script if needed.

## Configuration

- **Python Interpreter**: Ensure VS Code is using the correct Python interpreter. You can set this in `.vscode/settings.json`:
  ```json
  {
      "python.pythonPath": "C:\\Python312\\python.exe"
  }
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request. 🛠️

## License

This project is licensed under the MIT License. 📜

## Contact

For any questions or suggestions, feel free to reach out. 📧

Happy organizing! 🎉
