import os.path
from datetime import datetime

import tkinter as tk
from tkinter import messagebox
from tkinter import font

import cv2
from PIL import Image, ImageTk
import face_recognition
import csv
import subprocess

import util


class App:
    """Facial Recognition Attendance System."""
    
    def __init__(self):
        """Initialize the main application window and required directories."""
        self.main_window = tk.Tk()
        self.main_window.title("Facial Recognition Attendance System")
        self.main_window.geometry("1200x600+350+100")
        self.main_window.configure(bg="#f0f0f0")
        
        self.img_dir = './database/known_faces'
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)

        self.unk_dir = './database/unknown_faces'
        if not os.path.exists(self.unk_dir):
            os.mkdir(self.unk_dir)
        
        self.log_path = './database/log.csv'
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        # Create the main layout frame
        self.main_frame = tk.Frame(self.main_window, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label at the top
        self.title_label = tk.Label(self.main_frame, text="ATTENDANCE SYSTEM", 
                                    font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20, side=tk.TOP)

        # Frame for webcam display
        self.webcam_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.webcam_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Webcam display label
        self.webcam_label = tk.Label(self.webcam_frame, bg="#f0f0f0")
        self.webcam_label.pack()

        # Text label under webcam
        self.live_webcam_label = tk.Label(self.webcam_frame, text="Live Webcam", 
                                          font=("Helvetica", 10), bg="#f0f0f0")
        self.live_webcam_label.pack(pady=5)

        # Frame for buttons on the right side
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, 
                               padx=(0, 50), pady=(70, 0))

        # Attendance system buttons
        self.mark_attendance_button = tk.Button(self.button_frame, text="Mark Attendance", 
                                                command=self.start_attendance_loop, 
                                                font=("Helvetica", 14, "bold"), 
                                                bg="#4CAF50", fg="white", 
                                                width=20, height=2)
        self.mark_attendance_button.pack(pady=10)

        self.enroll_button = tk.Button(self.button_frame, text="Add New Face", 
                                       command=self.enroll_face, 
                                       font=("Helvetica", 14, "bold"), 
                                       bg="#2196F3", fg="white", 
                                       width=20, height=2)
        self.enroll_button.pack(pady=10)

        self.view_log_button = tk.Button(self.button_frame, text="View Attendance Log", 
                                         command=self.view_log, 
                                         font=("Helvetica", 14, "bold"), 
                                         bg="#FFC107", fg="white", 
                                         width=20, height=2)
        self.view_log_button.pack(pady=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", 
                                     command=self.exit_app, 
                                     font=("Helvetica", 14, "bold"), 
                                     bg="#F44336", fg="white", 
                                     width=20, height=2)
        self.exit_button.pack(pady=10)

        # Status label at the bottom
        self.status_label = tk.Label(self.main_window, text="Status: Ready", 
                                     font=("Helvetica", 12), bg="#f0f0f0")
        self.status_label.pack(pady=10)

        # Initialize webcam
        self.add_webcam(self.webcam_label)
        
    def add_webcam(self, label):
        """
        Add the webcam stream to the given label.
        
        Parameters:
        label (tk.Label): The label where the webcam stream is displayed.
        """
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0) # Change 0 to the ID of the webcam connected to your device
            
        self._label = label
        self.update_video_stream()

    def update_video_stream(self):
        """Update the webcam stream and refresh the display."""
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        
        img = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
                
        self.most_recent_capture_pil = Image.fromarray(img)
        
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(10, self.update_video_stream)

    def enroll_face(self):
        """Open a window for enrolling a new face into the database."""
        self.enroll_new_face_window = tk.Toplevel(self.main_window)
        self.enroll_new_face_window.geometry("1200x520+370+120")

        # Add "Accept" and "Try Again" buttons
        self.accept_button_enroll_new_face_window = util.get_button(self.enroll_new_face_window, 
                                                                    'Accept', 'green', 
                                                                    self.accept_enroll_new_face)
        self.accept_button_enroll_new_face_window.place(x=750, y=300)

        self.try_again_button_enroll_new_face_window = util.get_button(self.enroll_new_face_window, 
                                                                       'Try again', 'red', 
                                                                       self.try_again_enroll_new_face)
        self.try_again_button_enroll_new_face_window.place(x=750, y=400)

        # Image capture area
        self.capture_label = util.get_img_label(self.enroll_new_face_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        # Text field for entering username
        self.add_img_to_label(self.capture_label)
        self.entry_text_enroll_new_face = util.get_entry_text(self.enroll_new_face_window)
        self.entry_text_enroll_new_face.place(x=750, y=150)

        # Label prompting for username
        self.text_label_enroll_new_face = util.get_text_label(self.enroll_new_face_window, 
                                                              'Please, \ninput username:')
        self.text_label_enroll_new_face.place(x=750, y=70)

    def try_again_enroll_new_face(self):
        """Close the enroll window and allow the user to try enrolling again."""
        self.enroll_new_face_window.destroy()

    def add_img_to_label(self, label):
        """Display the most recent captured image in the given label."""
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.enroll_new_face_capture = self.most_recent_capture_arr.copy()

    def accept_enroll_new_face(self):
        """
        Save the captured face with the given username after verifying that the 
        face image contains exactly one face.
        """
        name = self.entry_text_enroll_new_face.get(1.0, "end-1c").strip()

        # Define file path for saving the image
        file_path = os.path.join(self.img_dir, f'{name}.jpg')

        if os.path.exists(file_path):
            messagebox.showwarning("Duplicate Name", "A user with this name already exists. Please use a different name.")
            return

        embeddings = face_recognition.face_encodings(self.enroll_new_face_capture)
        if len(embeddings) == 1:
            db_list = sorted(os.listdir(self.img_dir))  # Get list of known faces
            match = False
            
            for img in db_list:
                
                path_ = os.path.join(self.img_dir, img)

                known_face_img = cv2.imread(path_)  # Load known face image
                known_face_encodings = face_recognition.face_encodings(known_face_img)[0]  # Get its encoding

                # Compare the captured face with known faces
                match += face_recognition.compare_faces(known_face_encodings, embeddings)[0]
                
            if match > 0:
                messagebox.showwarning('Duplicate Faces', 'Face was already registered.')
            else:
                # Save the cropped face image
                face_locations = face_recognition.face_locations(self.enroll_new_face_capture)
                for (top, right, bottom, left) in face_locations:
                    face_img = self.enroll_new_face_capture[top:bottom, left:right]
                    cv2.imwrite(file_path, face_img)
                    
                messagebox.showinfo('Success!', 'User was registered successfully!')
        elif len(embeddings) > 1:
            messagebox.showwarning("Multiple Faces", "Please add only one face at a time.")
        else:
            messagebox.showwarning("No Face Detected", "No face detected in the image. Please try again.")

        self.enroll_new_face_window.destroy()

    def mark_attendance(self):
        """Mark attendance by comparing captured faces with the known faces database."""
        
        img = self.most_recent_capture_arr.copy()  # Capture current frame
        embeddings_unknown_list = face_recognition.face_encodings(img)  # Get face encodings

        if len(embeddings_unknown_list) == 0:
            print('No face detected')
            return  # Exit if no face is detected

        db_list = sorted(os.listdir(self.img_dir))  # Get list of known faces

        for embeddings_unknown in embeddings_unknown_list:
            match = False
            j = 0
            while not match and j < len(db_list):
                path_ = os.path.join(self.img_dir, db_list[j])

                known_face_img = cv2.imread(path_)  # Load known face image
                known_face_encodings = face_recognition.face_encodings(known_face_img)[0]  # Get its encoding

                # Compare the captured face with known faces
                match = face_recognition.compare_faces([known_face_encodings], embeddings_unknown)[0]
                j += 1

            if match:
                matched_name = db_list[j - 1][:-4]  # Extract name from filename (without .jpg extension)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_date = datetime.now().strftime("%Y-%m-%d")

                # Check if the person has already been logged today
                already_logged = False
                if os.path.exists(self.log_path):  # Check if log file exists
                    with open(self.log_path, 'r') as log_file:
                        log_reader = csv.reader(log_file)
                        for row in log_reader:
                            log_name, log_time = row
                            log_date = log_time.split(" ")[0]
                            if log_name == matched_name and log_date == current_date:
                                already_logged = True
                                break

                if not already_logged:
                    # Log the attendance to the log file
                    with open(self.log_path, 'a', newline='') as log_file:
                        log_writer = csv.writer(log_file)
                        log_writer.writerow([matched_name, current_time])
                else:
                    print(f"{matched_name} already logged today.")
            else:
                # Save unknown face in the 'unknown_faces' directory
                unknown_face_filename = os.path.join(self.unk_dir, 
                                                    f"unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                face_locations = face_recognition.face_locations(img)
                
                # Save the cropped face regions
                for (top, right, bottom, left) in face_locations:
                    face_img = img[top:bottom, left:right]
                    cv2.imwrite(unknown_face_filename, face_img)
                    
                print('Unknown person detected and saved.')
       
    def start_attendance_loop(self):
        """Starts the loop to capture frames and mark attendance."""
        self.mark_attendance()
        self.attendance_loop_id = self.main_window.after(1000, self.start_attendance_loop)

        self.toggle_attendance_button(text="Stop Attendance", command=self.stop_attendance_loop, color="#F44336")

    def stop_attendance_loop(self):
        """Stops the attendance loop."""
        if hasattr(self, 'attendance_loop_id'):
            self.main_window.after_cancel(self.attendance_loop_id)

        self.toggle_attendance_button(text="Mark Attendance", command=self.start_attendance_loop, color="#4CAF50")

    def toggle_attendance_button(self, text, command, color):
        """Update the attendance button with the given text, command, and color."""
        self.mark_attendance_button.config(text=text, command=command, bg=color)

    def view_log(self):
        """Open the attendance log file using the default application."""
        if not os.path.exists(self.log_path):
            messagebox.showerror("Error", "Log file does not exist.")
            return
        
        try:
            subprocess.run(['start', '', self.log_path], check=True, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log file: {str(e)}")
            print(e)

    def exit_app(self):
        """Release the webcam and close the application."""
        self.cap.release()
        self.main_window.quit()

    def start(self):
        """Start the main application loop."""
        self.main_window.mainloop()

        
if __name__ == "__main__":
    app = App()
    app.start()

