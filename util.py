import os

import tkinter as tk
from tkinter import messagebox
import face_recognition

def get_button(window, text, color, command, fg='white'):
    """
    Create and return a Tkinter button with specified parameters.
    
    Parameters:
    window (tk.Tk or tk.Toplevel): The window in which the button will be placed.
    text (str): The text to display on the button.
    color (str): Background color of the button.
    command (function): The function to be called when the button is pressed.
    fg (str): The text color of the button (default is 'white').
    
    Returns:
    tk.Button: Configured button ready to be added to the window.
    """
    button = tk.Button(
        window,
        text=text,
        activebackground="black",  # Background color when the button is active
        activeforeground="white",  # Text color when the button is active
        fg=fg,                     # Foreground color (text)
        bg=color,                  # Background color
        command=command,           # Function to call on button click
        height=2,                  # Button height
        width=20,                  # Button width
        font=('Helvetica bold', 20) # Font style and size
    )
    
    return button

def get_img_label(window):
    """
    Create and return a Tkinter label for displaying images.
    
    Parameters:
    window (tk.Tk or tk.Toplevel): The window in which the label will be placed.
    
    Returns:
    tk.Label: Configured label ready to be added to the window.
    """
    label = tk.Label(window)
    label.grid(row=0, column=0)  # Place the label in a grid layout (row 0, column 0)
    return label

def get_text_label(window, text):
    """
    Create and return a Tkinter label with the specified text.
    
    Parameters:
    window (tk.Tk or tk.Toplevel): The window in which the label will be placed.
    text (str): The text to display on the label.
    
    Returns:
    tk.Label: Configured label ready to be added to the window.
    """
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")  # Set the font and alignment
    return label

def get_entry_text(window):
    """
    Create and return a Tkinter text entry box.
    
    Parameters:
    window (tk.Tk or tk.Toplevel): The window in which the text entry box will be placed.
    
    Returns:
    tk.Text: Configured text entry box ready to be added to the window.
    """
    inputtxt = tk.Text(
        window,
        height=2,          # Height of the text entry box
        width=15,          # Width of the text entry box
        font=("Arial", 32) # Font style and size
    )
    return inputtxt
