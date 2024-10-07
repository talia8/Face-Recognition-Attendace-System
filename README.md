# Facial Recognition Attendance System

<img src="Screenshot.png">

## Overview

The **Facial Recognition Attendance System** is a Python-based application that uses computer vision techniques to recognize faces and mark attendance in real-time. The application can enroll new faces into a database and detect previously registered users to log their attendance. Unknown faces are also detected and logged with their image captured for later review.

This system is built using:
- **OpenCV** for video capture and image processing
- **Face Recognition** for facial detection and recognition
- **Tkinter** for the graphical user interface (GUI)
- **PIL** (Pillow) for image handling

The project is ideal for use in environments such as classrooms, offices, or events where attendance needs to be automatically tracked.


## Features

- **Real-time Face Detection**: Detect faces from a live video feed.
- **Mark Attendance**: Automatically logs attendance for recognized faces and prevents duplicate logging for the same day.
- **Enroll New Users**: Add new faces to the database with a simple UI for registering individuals.
- **Handle Unknown Faces**: Detect and store unknown faces in a separate directory for future review.
- **View Attendance Log**: Open the attendance log, which tracks the names and timestamps of attendees.
- **Graphical User Interface**: A simple and intuitive GUI that allows users to interact with the system easily.


## Requirements

### Software Requirements:
- **Python 3.x**
- **Operating System**: Works on Windows, Linux, or macOS

### Python Dependencies:
You can install the necessary dependencies using the following command:

```bash
pip install -r requirements.txt
```
If you're a Windows user make sure you have Visual Studio build tools installed. Linux and Mac OS users don't need to install cmake and dlib. 

## Installation & Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/facial-recognition-attendance-system.git
cd facial-recognition-attendance-system
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the application

```bash
python main.py
```


## Folder Structure

- **/database**: This folder holds the known and unknown face images and the log file.
  - **/known_faces**: Stores the images of enrolled users.
  - **/unknown_faces**: Stores the images of unknown faces detected by the system.
  - **log.csv**: Attendance log where recognized users and their timestamps are stored.

- **/util.py**: Utility functions used for creating UI elements.
- **main.py**: The main script to run the facial recognition system.
- **requirements.txt**: A list of Python dependencies required by the project.


## How to Use

### 1. Enroll a New User
- Launch the application.
- Click the **"Add New Face"** button.
- Enter the name of the person and ensure only one face is in the frame. Press **"Accept"** to save the face to the known database.

### 2. Mark Attendance
- Click the **"Mark Attendance"** button.
- The system will begin recognizing faces in real-time and log their attendance if they are recognized.
- If a person has already been logged for the day, they won’t be re-logged.

### 3. View Attendance Log
- Click the **"View Attendance Log"** button to open the log in a default text editor.
  
### 4. Detect Unknown Faces
- If the system detects an unknown face, it will save the face in the **/unknown_faces** directory. These images can be reviewed later for registration.


## Contributing

Contributions are welcome! Feel free to submit a pull request or report issues to improve the functionality or performance of the project.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Credits

This project uses the following open-source libraries:
- [OpenCV](https://opencv.org/)
- [Face Recognition](https://github.com/ageitgey/face_recognition)
- [Pillow (PIL)](https://python-pillow.org/)

