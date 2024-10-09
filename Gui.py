import os
import sys
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
        self.timeout_seconds = 1800  # Timeout after 30 minutes
        self.timeout = 0  # Timeout counter

        # Create the UI components
        self.init_ui()

    def init_ui(self):
        # Set the layout
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Create a frame for better visual separation
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")

        # Create buttons, labels, and input fields
        self.dir_label = QLabel(self.selected_directory, self)
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

        # Layout for File Name
        file_name_layout = QHBoxLayout()
        file_name_layout.addWidget(self.file_name_title)
        file_name_layout.addWidget(self.file_name_input)

        # Layout for File Extension
        file_extension_layout = QHBoxLayout()
        file_extension_layout.addWidget(self.file_extension_title)
        file_extension_layout.addWidget(self.file_extension_input)

        # Add widgets to layout
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
            self.file_label.setText(f"Waiting for: {self.selected_directory}/{self.file_name_input.text()}{self.file_extension}")

            # Reset timeout and start the timer to check for file existence
            self.timeout = 0
            self.start_timer()
        else:
            self.file_label.setText("Please enter a file name and choose a directory.")

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_file)
        self.timer.start(1000)  # Check every second

    def check_for_file(self):
        # Check if the file exists in the selected directory
        arr = os.listdir(self.selected_directory)
        if (self.entered_file_name + self.file_extension) in arr:
            self.timer.stop()  # Stop the timer if the file is found
            self.passResults()
        else:
            self.timeout += 1
            print("Waiting for file...")  # For debugging purposes

            if self.timeout >= self.timeout_seconds:
                self.timer.stop()
                self.show_error_message("Program timed out.")
                print("Program timed out.")

    def passResults(self):
        # Call the function from the other file to process the found file
        self.close()
        uploadVideo(self.selected_directory + '\\', self.entered_file_name, self.file_extension)
        sys.exit(self)

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