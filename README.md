# 🎥 YouTube Video Export and Upload Automation

This project automates the process of uploading videos to YouTube once they are finished exporting from DaVinci Resolve. It allows you to set up the upload script and leave your computer, so you can edit the video details later from any device without having to wait for the export to complete.

## ✨ Features

- 📂 Monitors a specified directory for video files being exported.
- 🚀 Automatically uploads the completed video to YouTube while keeping it private.
- 🐍 Uses Selenium for browser automation to interact with the YouTube Studio interface.

## 🛠️ Prerequisites

To run this project, you'll need to have the following installed:

- Python 3.x
- Pip (Python package manager)

## 📥 Installation

1. Clone this repository or download the files.
2. Navigate to the project directory.
3. Install the required Python packages by running the command to install `psutil` and `selenium`.
4. Download the ChromeDriver and ensure it matches your Chrome version. Set the path to the ChromeDriver in the `uploadVideo` script.
5. Configure the `uploadVideo` function with your YouTube channel ID and other settings.

## 🚦 Usage

1. Run the GUI application to set the directory and file name for the video you are exporting.
2. Once the video is exported, the application will automatically detect it and trigger the upload to YouTube.
3. The uploaded video will be set to private, allowing you to edit its details from your phone or another PC at your convenience.

## 🔍 How It Works

1. The GUI allows you to select a directory and enter the file name of the video.
2. The script waits for the specified video file to appear in the directory after the export is complete.
3. Upon detection of the completed file, the upload script will initiate, using Selenium to automate the upload process.
4. The video will be uploaded privately, allowing you to make further edits at your leisure.

## ⚠️ Important Notes

- Ensure that you are logged into your YouTube account in Chrome and that the correct user data path is specified in the upload script.
- The script will close any existing Chrome instances to avoid conflicts.
- Adjust the file path and browser settings in the script as necessary for your system.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
