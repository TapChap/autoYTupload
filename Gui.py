import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QLineEdit,
    QFrame,
    QMessageBox,
    QHBoxLayout,
)
from PyQt5.QtCore import QTimer
from uploadYTvideo import uploadVideo  # Ensure this is available

class FileBrowserApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the variables
        self.selected_directory = r"C:\Users\Shai grossman\Desktop\exported"
        self.entered_file_name = ""
        self.file_extension = ".mp4"  # Default file extension
        self.timer = None  # Timer to check for the file
        self.stable_check_count = 0
        self.stability_checks = 3
        self.last_size = 0

        # Create the UI components
        self.init_ui()

    def init_ui(self):
        # Set the layout
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.setWindowIcon(QIcon('youtube.ico'))  # Add this line to set the icon

        # Warning Label at the top
        warning_label = QLabel("Warning! Using this tool will close all open Chrome tabs, use with caution.", self)
        warning_label.setStyleSheet("color: red; font-weight: bold; font-size: 12px;")

        # Create a frame for better visual separation
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")

        # Create buttons, labels, and input fields
        self.dir_label = QLabel(f"Selected Directory: {self.selected_directory}", self)
        self.file_label = QLabel("", self)

        select_dir_button = QPushButton("Choose Directory", self)
        select_dir_button.setStyleSheet("background-color: #4CAF50; color: white;")

        # File Name Section
        self.file_name_title = QLabel("File Name:")
        self.file_name_input = QLineEdit(self)
        self.file_name_input.setPlaceholderText("Enter file name here...")

        # File Extension Section
        self.file_extension_title = QLabel("File Extension:")
        self.file_extension_input = QLineEdit(self)
        self.file_extension_input.setText("mp4")  # Default value for file extension
        self.file_extension_input.setPlaceholderText("Enter file extension (without dot)")

        save_button = QPushButton("Start", self)
        save_button.setStyleSheet("background-color: #008CBA; color: white;")

        # Connect buttons to functions
        select_dir_button.clicked.connect(self.browse_directory)
        save_button.clicked.connect(self.start_process)

        self.file_name_input.returnPressed.connect(self.start_process)       # Trigger on Enter key for file name
        self.file_extension_input.returnPressed.connect(self.start_process)  # Trigger on Enter key for file extension

        # Layout for File Name
        file_name_layout = QHBoxLayout()
        file_name_layout.addWidget(self.file_name_title)
        file_name_layout.addWidget(self.file_name_input)

        # Layout for File Extension
        file_extension_layout = QHBoxLayout()
        file_extension_layout.addWidget(self.file_extension_title)
        file_extension_layout.addWidget(self.file_extension_input)

        # Add widgets to layout
        layout.addWidget(warning_label)  # Add the warning label to the top
        layout.addWidget(self.dir_label)
        layout.addWidget(select_dir_button)
        layout.addLayout(file_name_layout)  # File Name Layout
        layout.addLayout(file_extension_layout)  # File Extension Layout
        layout.addWidget(save_button)
        layout.addWidget(self.file_label)

        # Set the layout to the frame and then to the window
        frame.setLayout(layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        # Window settings
        self.setWindowTitle("YT Upload")
        self.setGeometry(300, 300, 400, 250)

    def browse_directory(self):
        # Open a directory picker dialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selected_directory = directory
            self.dir_label.setText(f"Selected Directory: {directory}")

    def start_process(self):
        # Get the text from the QLineEdit fields and initiate file waiting
        file_name = self.file_name_input.text()
        file_extension = self.file_extension_input.text().strip()

        # Set the file extension with the dot prefix

        if file_extension:
            self.file_extension = f".{file_extension}"
        else:
            self.file_extension = ".mp4"  # Default to mp4 if empty

        if file_name and self.selected_directory:
            self.entered_file_name = file_name
            self.file_label.setText(f"Waiting for: {self.selected_directory}/{self.file_name_input.text()}{self.file_extension} to finish exporting")

        arr = os.listdir(self.selected_directory)
        if (self.entered_file_name + self.file_extension) not in arr:
            self.show_error_message("the specified file wasn't found")

        self.start_timer()

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_file_size)
        self.timer.start(1000)  # Check every second

    def check_for_file_size(self):
        filePath = self.selected_directory + "/" + self.file_name_input.text() + self.file_extension

        current_size = os.path.getsize(filePath)

        # Check if size is the same as last time
        if current_size == self.last_size:
            self.stable_check_count += 1
        else:
            self.stable_check_count = 0  # Reset if file size changed

        # Update last known size
        self.last_size = current_size

        # Check if file has been stable for enough checks
        if self.stable_check_count >= self.stability_checks:
            print("Export complete!")
            self.timer.stop()  # Stop checking further
            self.uploadVideo()

    def uploadVideo(self):
        # Call the function from the other file to process the found file
        self.close()
        uploadVideo(self.selected_directory + "\\", self.entered_file_name, self.file_extension)

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

def launchGUI():
    app = QApplication(sys.argv)
    file_browser = FileBrowserApp()
    file_browser.show()
    sys.exit(app.exec_())  # Ensure this exits cleanly

# Call launchGUI to start the application
if __name__ == "__main__":
    launchGUI()
