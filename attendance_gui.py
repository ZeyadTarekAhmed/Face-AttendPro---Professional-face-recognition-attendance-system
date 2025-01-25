import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from main import recognize_and_mark_attendance, stop_recognition
from PIL import Image, ImageTk, ImageFilter
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Create the main application window
root = tk.Tk()
root.title("Attendance System")
root.geometry("600x400")

# Global variable to track the state of the recognition process
recognition_running = False

# Function to start/stop face recognition
def toggle_recognition():
    global recognition_running
    if recognition_running:
        stop_recognition()
        recognition_button.config(text="Start Face Recognition", bg="green", fg="white")
        messagebox.showinfo("Info", "Face recognition stopped.")
    else:
        recognition_button.config(text="Stop Face Recognition", bg="red", fg="white")
        threading.Thread(target=recognize_and_mark_attendance, daemon=True).start()  # Run recognition in a separate thread
    recognition_running = not recognition_running

# Function to send attendance report via email with attachment
def send_email():
    try:
        # Email settings
        sender_email = ""  # Sender's email
        sender_password = ""  # Password
        receiver_email = ""  # Receiver's email
        # Email content
        subject = "Attendance Report"
        body = "Hi Dr,Attached is the attendance report for today's lecture."

        # Setup email using MIME
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Add attachment
        filename = "Attendance.csv"  # File you want to attach
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    "attachment; filename={}".format(filename),
                )
                msg.attach(part)
        except FileNotFoundError:
            messagebox.showerror("Error", "File '{}' not found!".format(filename))
            return

        # Connect to SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Change server if needed
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", "Attendance report sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to send email: {}".format(e))

# Load the logo image
try:
    logo_image = Image.open("logo.jpg")
    logo_image = logo_image.resize((600, 400), Image.Resampling.LANCZOS)  # Use LANCZOS for resampling
    blurred_logo_image = logo_image.filter(ImageFilter.GaussianBlur(5))  # Apply Gaussian blur effect
    logo_photo = ImageTk.PhotoImage(blurred_logo_image)
except FileNotFoundError:
    messagebox.showerror("Error", "Logo image not found! Please check the file path.")
    logo_photo = None

# Create and place the background using the logo image (if found)
if logo_photo:
    background_label = tk.Label(root, image=logo_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add a main title at the top of the window
title_label = tk.Label(
    root,
    text="Helwan National University Attendance System",
    bg="darkblue",
    fg="white",
    font=("Arial", 16, "bold")
)
title_label.place(relx=0.5, rely=0.05, anchor='center')  # Centered at the top

# Create and place an instruction label
instruction_label = tk.Label(
    root,
    text="Click the button below to start DSP lecture Attendance",
    bg="lightblue",
    font=("Arial", 12, "bold")
)
instruction_label.place(relx=0.5, rely=0.5, anchor='center', y=-30)

# Create and place a button to start/stop face recognition
recognition_button = tk.Button(
    root,
    text="Start Face Recognition",
    command=toggle_recognition,
    bg="green",
    fg="white",
    font=("Arial", 10, "bold")
)
recognition_button.place(relx=0.5, rely=0.5, anchor='center', y=10)

# Create and place a button to send attendance report via email
email_button = tk.Button(
    root,
    text="Send Attendance Report",
    command=send_email,
    bg="blue",
    fg="white",
    font=("Arial", 10, "bold")
)
email_button.place(relx=0.5, rely=0.5, anchor='center', y=60)

# Add a small text in the bottom left corner
developer_label = tk.Label(
    root,
    text="Developed by Eng.Zeyad Elbagoury",
    bg="lightgray",
    fg="black",
    font=("Arial", 8, "italic")
)
developer_label.place(relx=0.01, rely=0.95, anchor='w')  # Bottom left corner

# Function to update current time and date
def update_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Time and date format
    time_label.config(text=current_time)  # Update label text
    root.after(1000, update_time)  # Call itself every second

# Add a label for time and date in the bottom right corner
time_label = tk.Label(root, text="", bg="darkblue", fg="white", font=("Arial", 10))
time_label.place(relx=0.99, rely=0.95, anchor='e')  # Bottom right corner
update_time()  # Start updating time

# Run the application
root.mainloop()
