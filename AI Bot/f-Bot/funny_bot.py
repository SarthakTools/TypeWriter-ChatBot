import threading
from tkinter import *
import customtkinter as ct
from generate_response import generate_response
import random

ct.set_appearance_mode("dark")
root = ct.CTk()
root.geometry("550x600")

root.title("System_GPT - Comedy Edition")

def make_it_funny(original_text):
    """ Converts a normal chatbot response into a super funny one, with short funny replies for greetings. """
    simple_responses = {
        "hi": "Hey there! I was just about to take a nap!",
        "hello": "Hello! You just unlocked chatbot mode!",
        "hey": "Hey! What's up? Besides my CPU temperature...",
        "bye": "Bye! Don't forget to recharge your human battery!",
        "goodbye": "Goodbye! May your WiFi always be strong!",
        "thanks": "You're welcome! That'll be $0.00, please.",
        "thank you": "No problem! Just doing my chatbot duties!"
    }
    
    if original_text.lower() in simple_responses:
        return simple_responses[original_text.lower()]  # Return funny direct response

    funny_templates = [
        "Oh wow, you really wanted to know this? Alright, here goes:\n{}",
        "I could've just said '{}', but where’s the fun in that?",
        "Listen up, genius! Here's the deal:\n{}",
        "I asked my grandma, and she said:\n'{}'",
        "AI mode: OFF. Comedic mode: ON. Here's your answer:\n{}",
        "Bro, I had to consult the Oracle for this one:\n{}",
        "If I had a dollar for every time someone asked this... anyway:\n{}",
        "Not sure if you’re serious, but here’s what I got:\n{}",
        "I ran this through my joke generator, and it spat out:\n{}",
        "Processing... Processing... Just kidding! Here’s your answer:\n{}",
        "Imagine a world where this response makes sense... now wake up:\n{}",
        "I was gonna give a normal answer, but then I thought... why be normal?\n{}",
        "Hold up—lemme call NASA to confirm... Okay, they said:\n{}",
        "Bro, even Google had to think twice about this one. Anyway:\n{}",
        "I asked ChatGPT, and it said: '{}'. Wait a second—👀",
        "Are you SURE you wanna know? Alright, here’s the brutal truth:\n{}",
        "I wanted to give you a serious answer, but my contract says I gotta be funny:\n{}",
        "If I had a nickel for every time someone asked this, I'd have at least 5 cents. Anyway:\n{}",
        "I showed this question to my pet goldfish. It blinked twice. I think that means:\n{}",
        "I put your question into an AI. It generated a meme. But here’s your real answer:\n{}",
        "Dude, even Shakespeare would be like 'nah bro'. But here’s my best try:\n{}",
        "I tried asking Siri, but she just laughed. So here’s what I got:\n{}",
        "Oh, you want the premium answer? That costs $0.00! Here it is:\n{}",
        "I was about to answer, then my brain went on vacation. Luckily, I wrote this before it left:\n{}",
        "This answer is brought to you by... my last two brain cells:\n{}",
        "Hold on, lemme summon the ancient wisdom of the internet...\n{}",
        "I sent your question to the moon, and the astronauts replied:\n{}",
        "Bro, I whispered your question into the wind. The wind said:\n{}",
        "Even my grandma would’ve facepalmed at this, but here’s the answer:\n{}",
        "The council of memes has spoken. They declare:\n{}",
        "If you don’t like this answer, take it up with the Comedy Department:\n{}",
        "I was gonna tell you a joke about this, but then I realized the real joke is...\n{}",
        "I asked an 8-ball. It said 'ask again later'. I ignored it and got this:\n{}",
        "I asked my toaster for advice. It said 'be warm and toasty'. Anyway, here's the answer:\n{}",
        "I Googled your question and accidentally ordered a pizza. But here’s your answer:\n{}",
        "I ran your question through my sarcasm filter, but it broke. So here’s the raw response:\n{}",
        "This response has been approved by the International Society of Funny Bots™:\n{}",
        "BREAKING NEWS: Your question has been answered! Read all about it:\n{}",
        "Oh, you want an answer? I was too busy laughing, but okay:\n{}",
        "This response is brought to you by: caffeine, chaos, and questionable decisions:\n{}",
        "I asked my dog. He said 'woof'. I translated that into:\n{}",
        "The aliens have confirmed: the official response to your question is:\n{}"
    ]
    
    return random.choice(funny_templates).format(original_text)


def generate_text(text):
    response = generate_response(text)  # Get the original response
    return make_it_funny(response)  # Convert it to a funny version

def typewriter(label, text, counter=0):
    if counter <= len(text):
        label.configure(text=text[:counter] + " █")
        root.after(10, lambda: typewriter(label, text, counter + 1))
    else:
        label.configure(text=text)

def respond_message(event):
    message = entry.get()
    entry.delete(0, END)
    
    user_label = Label(label_frame, text=message, font=("Poppins", 15), bg="#333541", fg="white", wraplength=1000, justify=LEFT)
    user_label.pack(side=TOP, fill=X, anchor="w", pady=(10, 0))
    
    bot_frame = ct.CTkFrame(label_frame, fg_color="#333541")
    bot_frame.pack(side=TOP, fill=X, anchor="w", padx=10, ipady=5, ipadx=10)

    bot_label = Label(bot_frame, text="", font=("Poppins", 15), bg="#444654", fg="white", wraplength=1000, justify=LEFT)
    bot_label.pack(side=TOP, fill=X, anchor="w", ipady=10, pady=(10, 0))
    
    response = generate_text(message)  # Get the funny response
    
    threading.Thread(target=typewriter, args=(bot_label, response)).start()
    
    root.update_idletasks()
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def configure_scroll_region(e):
    canvas.configure(scrollregion=canvas.bbox('all'))
        
def resize_frame(e):
    canvas.itemconfigure(scrollable_window, width=e.width-10)

canvas = Canvas(root, bg="#353740", highlightthickness=0)
label_frame = Frame(canvas, bg="#353740")
label_frame.pack(side="left", fill="both", expand=True)
scrollable_window = canvas.create_window((0, 0), window=label_frame, anchor="nw")
canvas.pack(side=TOP, fill=BOTH, expand=True)

label_frame.bind("<Configure>", configure_scroll_region)
scrollbar = ct.CTkScrollbar(canvas, orientation="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.yview_moveto(1.0)
scrollbar.pack(side="right", fill=Y)
canvas.bind("<Configure>", resize_frame)

entry = ct.CTkEntry(root, font=("Poppins", 16), fg_color="#40414f", placeholder_text="Send a message")
entry.pack(side=BOTTOM, fill=X, ipady=10, pady=10, padx=10)
entry.bind("<Return>", respond_message)

root.mainloop()
