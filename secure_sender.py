import os
import sys
import smtplib
import threading
import getpass
import datetime
import customtkinter as ctk
from tkinter import messagebox
from email.message import EmailMessage

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    print("Error: tkinterdnd2 module not found.")
    print("Please install it using: pip install tkinterdnd2")
    sys.exit(1)

# --- Configuration ---
SMTP_SERVER = '######'
SMTP_PORT = 465  # Put here your SSL
SENDER_EMAIL = '########'  
SENDER_PASSWORD = '######' 
RECEIVER_EMAIL = '#######' 

# Set Appearance Mode
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # Window Setup
        self.title("Corporate Secure Sender")
        self.geometry("400x350")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        # Get Current User
        self.username = getpass.getuser()

        # Grid Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Drop Zone
        self.grid_rowconfigure(2, weight=0) # Status
        self.grid_rowconfigure(3, weight=0) # Progress

        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, pady=(20, 10), sticky="ew")

        self.user_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"User: {self.username}", 
            font=("Roboto", 14, "bold"),
            text_color="#cfcfcf"
        )
        self.user_label.pack()

        self.sub_label = ctk.CTkLabel(
            self.header_frame, 
            text="Secure File Transfer", 
            font=("Roboto", 12),
            text_color="#a0a0a0"
        )
        self.sub_label.pack()

        # 2. Drop Zone
        self.drop_frame = ctk.CTkFrame(
            self, 
            width=300, 
            height=150, 
            corner_radius=15,
            border_width=2,
            border_color="#1f6aa5",
            fg_color="#2b2b2b"
        )
        self.drop_frame.grid(row=1, column=0, padx=20, pady=10)
        self.drop_frame.pack_propagate(False) # Prevent shrinking

        self.drop_label = ctk.CTkLabel(
            self.drop_frame, 
            text="📁 Drop File Here", 
            font=("Segoe UI", 16, "bold"),
            text_color="#1f6aa5"
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        # 3. Status Label
        self.status_label = ctk.CTkLabel(
            self, 
            text="Ready to send", 
            font=("Roboto", 12),
            text_color="#3b8ed0" # default blue-ish
        )
        self.status_label.grid(row=2, column=0, pady=(5, 5))

        # 4. Progress Bar (Initially Hidden)
        self.progressbar = ctk.CTkProgressBar(self, width=300, mode="indeterminate")
        self.progressbar.grid(row=3, column=0, pady=(0, 20))
        self.progressbar.grid_remove() # Hide initially

        # Enable Drag and Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        if os.path.isfile(file_path):
            self.start_sending(file_path)
        else:
            self.update_status("Error: Not a valid file", "red")
            self.flash_error()

    def start_sending(self, file_path):
        # UI Updates for Sending State
        self.drop_frame.configure(border_color="#e5b800") # Yellow/Orange for processing
        self.drop_label.configure(text="Processing...", text_color="#e5b800")
        self.update_status("Sending secure email...", "#3b8ed0") # Blue
        
        self.progressbar.grid() # Show progress bar
        self.progressbar.start()
        
        # Start Thread
        threading.Thread(target=self.send_email_thread, args=(file_path,), daemon=True).start()

    def send_email_thread(self, file_path):
        try:
            filename = os.path.basename(file_path)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            subject = f"File from employee: {self.username} ({filename})"
            body = (
                f"File Transfer Notification\n"
                f"--------------------------\n"
                f"Sender: {self.username}\n"
                f"File: {filename}\n"
                f"Original Path: {file_path}\n"
                f"Timestamp: {timestamp}\n"
            )

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            msg.set_content(body)

            with open(file_path, 'rb') as f:
                file_data = f.read()

            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=filename)

            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD.replace(" ", ""))
                server.send_message(msg)

            # Success Callback
            self.after(0, self.on_success, filename)

        except Exception as e:
            # Error Callback
            error_msg = str(e)
            self.after(0, self.on_error, error_msg)

    def on_success(self, filename):
        self.progressbar.stop()
        self.progressbar.grid_remove()
        
        self.drop_frame.configure(border_color="#2cc985") # Green
        self.drop_label.configure(text="Sent!", text_color="#2cc985")
        
        self.update_status("Sent Successfully!", "#2cc985") # Green
        
        # Reset UI after delay
        self.after(3000, self.reset_ui)

    def on_error(self, error_msg):
        self.progressbar.stop()
        self.progressbar.grid_remove()
        
        self.drop_frame.configure(border_color="#FF5555") # Red
        self.drop_label.configure(text="Failed", text_color="#FF5555")
        
        self.update_status("Error Sending File", "#FF5555")
        print(f"Error details: {error_msg}")
        
        # Reset UI after delay
        self.after(3000, self.reset_ui)

    def reset_ui(self):
        self.drop_frame.configure(border_color="#1f6aa5")
        self.drop_label.configure(text="📁 Drop File Here", text_color="#1f6aa5")
        self.update_status("Ready to send", "#3b8ed0")

    def update_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

    def flash_error(self):
        self.drop_frame.configure(border_color="#FF5555")
        self.after(500, lambda: self.reset_ui())

if __name__ == "__main__":
    app = App()
    app.mainloop()
