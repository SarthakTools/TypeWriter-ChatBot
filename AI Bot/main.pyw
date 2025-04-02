import threading
from tkinter import *
import customtkinter as ct
from customtkinter import *
from generate_response import generate_response
from PIL import Image
import os

ct.set_appearance_mode("dark")
root = ct.CTk()
root.geometry("550x600")
root.title("Katyayini")
root.iconbitmap("images\\ai.ico")

def generate_text(text):
    response = generate_response(text)
    return response
  
def typewriter(label, text, counter=0):
    if counter <= len(text):
        label.configure(text=text[:counter] + " █")
        root.after(16, lambda: typewriter(label, text, counter + 1))
    else:
        label.configure(text=text)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def respond_message(event):
    image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
    bot_image = CTkImage(Image.open(os.path.join(image_path, "infinity.png")), size=(40, 40))
    user_image = CTkImage(Image.open(os.path.join(image_path, "ai.png")), size=(40, 40))

    message = entry.get()
    entry.delete(0, END)
    
    # Create a user message frame with image and text
    
    frame = ct.CTkFrame(label_frame, fg_color="#222", corner_radius=0)
    user_frame = ct.CTkFrame(frame, fg_color="#222", corner_radius=0)
    user_frame.pack(side=TOP, fill=X, padx=40, pady=(10, 0), ipady=10)
    frame.pack(side=TOP, fill=X, ipady=5)

    # User image and message label in horizontal alignment
    CTkLabel(user_frame, text="", image=user_image).pack(side=LEFT, padx=(10, 15))
    user_label = Label(user_frame, text=message, font=("Poppins", 20), bg="#222", fg="white",)
    user_label.pack(side=LEFT, anchor="w")

    # Create a bot frame with image and text in a horizontal layout
    response_frame = ct.CTkFrame(label_frame, fg_color="transparent")  # Bot frame will be transparent
    response_frame.pack(side=TOP, fill=X, padx=40, pady=(10, 0))

    # Inside response frame, pack bot image and response text in one line
    bot_frame = ct.CTkFrame(response_frame, fg_color="transparent", corner_radius=10)
    bot_frame.pack(side=TOP, fill=X, anchor="center", ipady=20, ipadx=10)  # Center the frame

    # Display the bot image and the text in a row, side by side
    CTkLabel(bot_frame, text="", image=bot_image).pack(side=LEFT, padx=(10, 15))
    bot_label = Label(bot_frame, text="", font=("Poppins", 20), bg="#333542", fg="white", wraplength=1000, justify=LEFT)
    bot_label.pack(side=LEFT, anchor="w")

    # Generate the bot response
    response = generate_text(message)
    
    threading.Thread(target=typewriter, args=(bot_label, response)).start()
    
    root.update_idletasks()
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def configure_scroll_region(e):
    canvas.configure(scrollregion=canvas.bbox('all'))
        
def resize_frame(e):
    canvas.itemconfigure(scrollable_window, width=e.width)

canvas = Canvas(root, bg="#353740", highlightthickness=0)
# label_frame = CTkFrame(canvas, fg_color="#353740")
root.configure(fg_color="#353740")
label_frame = CTkFrame(canvas, fg_color="#353740")
label_frame.pack(side="left", fill="both", expand=True, pady=(20, 10))

scrollable_window = canvas.create_window((0, 0), window=label_frame, anchor="nw")
canvas.pack(side=TOP, fill=BOTH, expand=True, pady=10)

label_frame.bind("<Configure>", configure_scroll_region)
scrollbar = ct.CTkScrollbar(canvas, orientation="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.yview_moveto(1.0)
scrollbar.pack(side="right", fill=Y)
canvas.bind("<Configure>", resize_frame)

image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
send_image = CTkImage(Image.open(os.path.join(image_path, "send.png")), size=(30, 30))

entry_frame = CTkFrame(root, fg_color="#222")
entry = ct.CTkEntry(entry_frame, font=("Poppins", 20), fg_color="transparent", placeholder_text="Send a message", border_color="#222")
entry.pack(side=LEFT, fill=X, expand=True, ipady=10, padx=10)
entry.bind("<Return>", respond_message)

CTkButton(entry_frame, text="", image=send_image, fg_color="transparent", width=0, command=lambda: respond_message("")).pack(side=RIGHT)
entry_frame.pack(side=BOTTOM, fill=X, padx=20, pady=10)

root.mainloop()
