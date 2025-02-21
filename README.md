# RidiculousRenamer

This was really just an experiment conducted with ChatGPT to test how good it is at assembling a moderately complex UI. It was HORRIBLE at Kivy (it could never get working one) but terrific at PySide which is good enough I suppose.

That said, it's a pretty decent renamer that lets you preview images you're renaming, edit destination filenames before they actually get made, and it has a decent progress tracker.

It supports undo which is pretty cool for a commandline tool.

Improvements could be made, and if you do something interesting feel free to send a pull request and I'll probably accept it.

## **The Creed of a Python Renaming Tool**

1. **This is my renaming tool. There are many like it, but this one is mine.**  

2. **My renaming tool is my best friend. It is my workflow. I must master it as I must master my craft.**  

3. **My renaming tool, without me, is useless. Without my renaming tool, I am slow. I must execute my scripts cleanly. I must rename more efficiently than chaos threatens to disorganize me. I must structure my files before confusion spreads. I will...**  

4. **My renaming tool and I know that what counts in this battle is not the number of lines of code, nor the verbosity of output, nor the complexity of syntax. We know that only precision matters. We will rename with precision…**  

5. **My renaming tool is an extension of myself, even as I am of it. Thus, I will learn it as a brother. I will know its weaknesses, its strengths, its functions, its arguments, its regex patterns, and its logging behavior. I will guard it against poor error handling and unnecessary inefficiencies, just as I guard my system against corruption and failure. I will keep it optimized and robust. We will become part of each other. We will…**  

6. **Before logic and order, I swear this creed. My renaming tool and I are the guardians of organization. We are the masters of disorder. We are the saviors of structure.**  

7. **So be it, until all filenames are clean, every directory is in order, and there is no chaos—only clarity!**


---
# RidiculousRenamer

**RidiculousRenamer** is a Python-based **batch file renaming tool** with a **graphical user interface (GUI)** built using **PySide6 (Qt for Python)**. It allows users to preview, modify, and confirm file renaming before execution. It also supports **undoing renames**, copying files to a new location with modified names, and displaying an **image preview** for selected image files.

## 🚀 Features

✅ **Batch rename files** using prefixes, suffixes, and sequential numbering  
✅ **Graphical UI (PySide6)** for previewing and modifying filenames before renaming  
✅ **Live image preview** when selecting an image file in the UI  
✅ **Undo renaming** using a saved JSON mapping file (automatically stored)  
✅ **Copy files to a new directory** instead of renaming in place  
✅ **Progress bar & pie chart visualization** during renaming  
✅ **Estimated time to completion** for large file operations  

---

## 📥 Installation

### **1️⃣ Install Python (if not installed)**
- Python **3.8+** is required.

Download from [python.org](https://www.python.org/) if needed.

### **2️⃣ Install Required Packages**
Run the following command to install dependencies:
```sh
pip install -r requirements.txt
```
If `requirements.txt` isn't available, install manually:
```sh
pip install PySide6 matplotlib
```

---

## 🛠️ Usage

The script provides a **command-line interface (CLI)** to rename or copy files, and an interactive **GUI for confirming renames**.

### **Basic Syntax**
```sh
python rename_files.py [DIRECTORY] [OPTIONS]
```

### **Renaming Files**
```sh
python rename_files.py my_folder -p "*.jpg" -s newfile --suffix "_edited"
```
✅ Renames all `.jpg` files in `my_folder` to:
```
image1.jpg  →  newfile_0001_edited.jpg
image2.jpg  →  newfile_0002_edited.jpg
```
📌 **Before renaming**, the GUI will show a preview where filenames can be edited.

---

### **Undo Last Rename**
```sh
python rename_files.py --undo
```
✅ **Restores files to their original names** using the last saved JSON mapping.

#### **Undo with a Specific JSON File**
```sh
python rename_files.py --undo 2de8102e-ecc5-4ad8-b588-7bcf377350a9.json
```
✅ **Uses the provided mapping file** instead of the last recorded one.

---

### **Copy Files Instead of Renaming**
```sh
python rename_files.py my_folder -p "*.png" -s copy_test -c backup_folder
```
✅ **Copies files to `backup_folder` with renamed versions.**  
✅ **Original files remain unchanged.**

---

## 🖥️ GUI Features

When renaming files, a **PySide6-based GUI** appears, showing:

### **1️⃣ Editable Filename Table**
- View old & new filenames before renaming
- Click to edit new filenames

### **2️⃣ Image Preview Pane**
- Clicking a filename shows **image preview** (if it's an image file)

### **3️⃣ Progress Bar & Pie Chart**
- Shows renaming progress
- If copying, displays **estimated time to completion**

---

## ⚙️ Command-Line Options

| Option           | Description |
|-----------------|-------------|
| `DIRECTORY`     | The folder containing files to rename |
| `-p, --pattern` | Wildcard pattern (e.g., `*.txt`, `*.jpg`) |
| `--prefix`      | Prefix to add to filenames |
| `--suffix`      | Suffix to add to filenames |
| `-s, --sequence` | Sequential renaming pattern (e.g., `file_0001`) |
| `-c, --copy`    | Copy files to a new folder instead of renaming |
| `-u, --undo`    | Undo last renaming operation |

---
## 📝 Notes
- The **undo feature** relies on JSON mapping files that are **automatically saved** in the same directory as the renamed files.
- If renaming involves **copying**, the **estimated time to completion** is displayed.
- **Image previews** work for `.jpg`, `.png`, `.gif`, `.bmp` formats.

---

## 🏗️ Future Enhancements
- Drag-and-drop file selection
- More renaming rules (e.g., regex-based renames)

---

## 🔥 Contributing
Pull requests and feature suggestions are welcome! Open an issue if you encounter bugs.

---

## 📜 License
**MIT License** – Free to use and modify.

---

## 🎉 Credits
Developed by **Eddie Engineer**.
