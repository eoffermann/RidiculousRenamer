import os
import sys
import glob
import json
import logging
import uuid
from pathlib import Path
from typing import Optional, Dict
import time
import argparse
import shutil
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QDialog, QProgressBar, 
    QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

MAPPING_FILE_STORAGE = "last_mapping.json"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class RenameFilesUI(QDialog):
    def __init__(self, file_mappings, copy_mode=False, copy_dest=None):
        super().__init__()
        self.file_mappings = file_mappings
        self.copy_mode = copy_mode
        self.copy_dest = Path(copy_dest) if copy_dest else None
        self.progress = 0
        self.total_files = len(file_mappings)
        self.start_time = None
        self.timer = QTimer()

        self.setWindowTitle("File Rename Preview")
        self.setGeometry(100, 100, 800, 500)
        
        # Main layout (Horizontal split: Left = Table, Right = Image Preview)
        main_layout = QHBoxLayout(self)

        # Left side: File Table
        left_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(len(file_mappings))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Old Filename", "New Filename"])
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 250)
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, (old, new) in enumerate(file_mappings.items()):
            self.table.setItem(i, 0, QTableWidgetItem(Path(old).name))
            self.table.setItem(i, 1, QTableWidgetItem(Path(new).name))

        self.table.itemSelectionChanged.connect(self.show_image_preview)

        left_layout.addWidget(QLabel("Preview of file renaming:"))
        left_layout.addWidget(self.table)

        # Buttons
        button_layout = QVBoxLayout()
        self.start_button = QPushButton("Confirm Rename")
        self.cancel_button = QPushButton("Cancel")
        self.start_button.clicked.connect(self.start_rename)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)

        left_layout.addLayout(button_layout)

        main_layout.addLayout(left_layout)

        # Right side: Image Preview
        right_layout = QVBoxLayout()
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(300, 300)
        self.image_label.setScaledContents(True)
        right_layout.addWidget(self.image_label)
        main_layout.addLayout(right_layout)

        # Progress UI (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)

        self.eta_label = QLabel("Estimated time remaining: --")
        self.eta_label.setVisible(False)
        left_layout.addWidget(self.eta_label)

        self.pie_chart_label = QLabel()
        self.pie_chart_label.setVisible(False)
        right_layout.addWidget(self.pie_chart_label)

    def show_image_preview(self):
        """Displays an image preview when a file is selected."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        filename = selected_items[0].text()
        full_path = next((key for key in self.file_mappings.keys() if Path(key).name == filename), None)

        if full_path and Path(full_path).suffix.lower() in [".jpg", ".png", ".gif", ".bmp"]:
            pixmap = QPixmap(full_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.setText("Invalid Image")
        else:
            self.image_label.setText("No image selected")

    def start_rename(self):
        """Begins renaming/copying files and updates the UI."""
        self.start_time = time.time()
        
        # Update mappings based on user edits
        for i in range(self.table.rowCount()):
            old_name = self.table.item(i, 0).text()
            new_name = self.table.item(i, 1).text()
            old_path = next((k for k in self.file_mappings.keys() if Path(k).name == old_name), None)
            if old_path:
                self.file_mappings[old_path] = str(Path(old_path).parent / new_name)

        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.eta_label.setVisible(self.copy_mode)
        self.pie_chart_label.setVisible(True)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(500)

    def update_progress(self):
        """Performs renaming/copying in steps and updates progress UI."""
        if self.progress < self.total_files:
            old_path, new_path = list(self.file_mappings.items())[self.progress]

            if self.copy_mode:
                shutil.copy(old_path, self.copy_dest / Path(new_path).name)
            else:
                os.rename(old_path, new_path)

            self.progress += 1
            self.progress_bar.setValue(int((self.progress / self.total_files) * 100))
            self.update_pie_chart()

            elapsed_time = time.time() - self.start_time
            if self.progress > 0:
                estimated_time = (elapsed_time / self.progress) * (self.total_files - self.progress)
                self.eta_label.setText(f"Estimated time remaining: {int(estimated_time)}s")

        else:
            self.timer.stop()
            self.accept()

    def update_pie_chart(self):
        """Creates and updates a properly scaled pie chart showing progress."""
        completed = self.progress
        remaining = self.total_files - completed

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie([completed, remaining], labels=["Completed", "Remaining"],
               autopct='%1.1f%%', startangle=90, colors=["green", "lightgrey"])
        ax.axis("equal")

        fig.canvas.draw()
        img_path = "progress_pie.png"
        fig.savefig(img_path, bbox_inches='tight', dpi=100)
        plt.close(fig)

        pixmap = QPixmap(img_path)
        self.pie_chart_label.setPixmap(pixmap)
        self.pie_chart_label.setScaledContents(True)

def save_last_mapping(mapping_file):
    """Stores the last used JSON mapping filename."""
    with open(MAPPING_FILE_STORAGE, "w", encoding="utf-8") as f:
        json.dump({"last_mapping": mapping_file}, f)

def load_last_mapping():
    """Retrieves the last stored JSON mapping file, if available."""
    if not os.path.exists(MAPPING_FILE_STORAGE):
        return None
    with open(MAPPING_FILE_STORAGE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("last_mapping")

def rename_files(directory: str, pattern: str, prefix: Optional[str] = None, suffix: Optional[str] = None, 
                 sequence: Optional[str] = None, copy_dest: Optional[str] = None) -> None:
    """
    Prepares a mapping of new filenames and launches the UI for confirmation.

    Args:
        directory (str): Path to the directory containing files to rename.
        pattern (str): File pattern to match (e.g., "*.jpg").
        prefix (Optional[str]): Prefix to add to filenames.
        suffix (Optional[str]): Suffix to add to filenames.
        sequence (Optional[str]): Sequence identifier for numbering files.
        copy_dest (Optional[str]): Destination directory if copying instead of renaming.

    Raises:
        FileNotFoundError: If no matching files are found.
        FileExistsError: If renaming would overwrite existing files.
    """
    directory = Path(directory).resolve()
    files = sorted(directory.glob(pattern))  # Using Path.glob instead of `glob.glob`

    if not files:
        logging.error("No matching files found.")
        raise FileNotFoundError("No matching files found in the specified directory.")

    # Prepare mapping file
    mapping: Dict[str, str] = {}
    uuid_str = str(uuid.uuid4())
    mapping_file = directory / f"{uuid_str}.json"

    # Create copy destination directory if needed
    if copy_dest:
        copy_dest = Path(copy_dest).resolve()
        copy_dest.mkdir(parents=True, exist_ok=True)

    for idx, old_path in enumerate(files, start=1):
        old_path = Path(old_path)  # Ensure it's a Path object
        ext = old_path.suffix
        stem = old_path.stem

        # Construct new filename
        new_name = f"{sequence}_{idx:04d}{ext}" if sequence else f"{stem}{ext}"
        if prefix:
            new_name = f"{prefix}{new_name}"
        if suffix:
            new_name = f"{Path(new_name).stem}{suffix}{ext}"

        # Determine the new path
        new_path = (copy_dest / new_name) if copy_dest else (directory / new_name)

        # Prevent overwriting existing files
        if new_path.exists():
            logging.error(f"File conflict: {new_path} already exists. Rename aborted.")
            raise FileExistsError(f"Renaming would overwrite existing file: {new_path}")

        if old_path != new_path:
            mapping[str(old_path)] = str(new_path)

    # Write mapping file
    with mapping_file.open("w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4)

    logging.info(f"Mapping file saved: {mapping_file}")

    # Save the last mapping for reference
    save_last_mapping(str(mapping_file))

    # Launch UI
    app = QApplication.instance() or QApplication(sys.argv)  # Avoid multiple instances
    ui = RenameFilesUI(mapping, copy_mode=bool(copy_dest), copy_dest=copy_dest)
    if ui.exec():
        logging.info(f"Renaming complete. Mapping file saved: {mapping_file}")

def undo_rename(mapping_file=None):
    """Restores files to their original names using a JSON mapping file."""
    if not mapping_file:
        mapping_file = load_last_mapping()
        if not mapping_file:
            print("Error: No previous mapping file found. Please specify a file.")
            sys.exit(1)

    mapping_path = Path(mapping_file).resolve()

    if not mapping_path.exists():
        print(f"Error: Mapping file '{mapping_path}' not found.")
        sys.exit(1)

    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    for old_name, new_name in mapping.items():
        new_path = Path(new_name)
        old_path = Path(old_name)

        if new_path.exists():
            os.rename(new_path, old_path)
        else:
            print(f"Path {new_path} does not exist.")

    print(f"Undo completed. Files restored based on {mapping_path}")

def main():
    parser = argparse.ArgumentParser(description="Rename or copy files with UI confirmation.")
    parser.add_argument("directory", type=str, nargs="?", help="Directory containing files (not required for undo).")
    parser.add_argument("-p", "--pattern", type=str, default="*", help="File pattern (e.g., *.txt).")
    parser.add_argument("--prefix", type=str, help="Prefix for filenames.")
    parser.add_argument("--suffix", type=str, help="Suffix for filenames.")
    parser.add_argument("-s", "--sequence", type=str, help="Sequential renaming pattern.")
    parser.add_argument("-c", "--copy", type=str, help="Copy files to this directory instead of renaming in place.")
    parser.add_argument("-u", "--undo", nargs="?", const=True, help="Undo the last renaming operation or use a specified JSON mapping file.")

    args = parser.parse_args()

    if args.undo:
        undo_rename(args.undo if args.undo is not True else None)
    elif args.directory:
        rename_files(args.directory, args.pattern, args.prefix, args.suffix, args.sequence, args.copy)
    else:
        print("Error: You must specify a directory unless using --undo.")
        sys.exit(1)

if __name__ == "__main__":
    main()