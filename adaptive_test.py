from os import kill, getpid, listdir, path
from socket import getfqdn, gethostbyname_ex
from threading import Thread
from signal import SIGTERM
from json import load
from pygame import mixer
import logging
import app, sessions
import customtkinter as ctk
from tkinter import ttk

'''Methods'''
def update_student_data():
    for id in listdir("data/student_data"): # Loop through student_data directory
        if path.isdir(f"data/student_data/{id}") and id.startswith("1000") and len(id) == 9: # Check if folder is valid
            if id not in student_data: # Student not in database yet
                student_data[id] = {}
                inserted = False
                for index, i in enumerate(listbox.get_children()):
                    if int(id) < int(listbox.item(i, "text")):
                        listbox.insert("", index, text=id)
                        inserted = True
                        break
                if not inserted:
                    listbox.insert("", "end", text=id)
                logging.info(f"{id}: inserted")
            try:
                with open(f"data/student_data/{id}/scores.json", 'r', encoding = "utf-8") as file: # Update student data
                    json_data = load(file)
                    if not(len(student_data[id]) == len(json_data) or len(student_data[id]) == len(json_data) + 1):
                        student_data[id] = json_data # Reload json data
                        logging.info(f"{id}: json data reloaded")
                if len(student_data[id]) == 5:
                    for audio in listdir(f"data/student_data/{id}"):
                        if path.splitext(audio)[1] in [".mp3", ".m4a", ".wav"]:
                            student_data[id]["audio"] = f"data/student_data/{id}/{audio}"
                            logging.info(f"{id}: audio loaded")
                            break
            except:
                pass

def update_connections():
    users.configure(text=str(sessions.total_session()))

def update_audio_slider():
    global audio_file, playback
    if audio_controls.cget("text") == "\u23F8":
        playback += 1

    try:
        if playback / mixer.Sound.get_length(audio_file) > 1:
            playback = 0
            logging.info("Music looped, reset slider")
        audio_slider.set(playback / mixer.Sound.get_length(audio_file))
    except:
        pass

def updates(): # Main update functions
    update_student_data()
    update_connections()
    update_audio_slider()
    root.after(1000, updates) # Wait 2s

def on_select(event):
    global audio_file, playback
    # Resets
    student = listbox.item(listbox.focus(), "text")
    student_name.configure(text="")
    reading_score.configure(text="")
    listening_score.configure(text="")
    writing_prompt.configure(text="")
    writing.configure(state="normal")
    writing.delete("1.0", "end")
    writing.configure(state="disabled")
    mixer.music.unload()
    audio_file = 0
    audio_slider.set(0)
    audio_controls.configure(text="\u23F5")
    playback = 0
    logging.info(f"Cleared data in preparation for {student}")

    try:
        student_name.configure(text=student_data[student]["name"])
        reading_score.configure(text=student_data[student]["reading"])
        listening_score.configure(text=student_data[student]["listening"])
        writing_prompt.configure(text="\n\n" + student_data[student]["writing prompt"])
        writing.configure(state="normal")
        writing.insert("1.0", "\n" + student_data[student]["writing"])
        writing.configure(state="disabled")
        logging.info(f"Loaded {student} into data")
    except:
        logging.warning(f"Error loading main data: {student_data[student]}")

    try:
        mixer.music.load(student_data[student]["audio"])
        audio_file = mixer.Sound(student_data[student]["audio"])
    except:
        logging.warning(f"Error loading audio: {student_data[student]}")

def on_play():
    try:
        if audio_controls.cget("text") == "\u23F5":
            if playback == 0:
                mixer.music.play(loops=-1)
                logging.info("Audio started")
            else:
                mixer.music.unpause()
                logging.info("Audio resumed")
            audio_controls.configure(text="\u23F8")
        else:
            mixer.music.pause()
            logging.info("Audio paused")
            audio_controls.configure(text="\u23F5")
    except:
        logging.warning("Error playing audio")

def on_audio_scroll(event):
    global audio_file, playback
    try:
        time = mixer.Sound.get_length(audio_file) * audio_slider.get()
        mixer.music.set_pos(time)
        playback = time
        logging.info(f"Audio set to {time}")
    except:
        audio_slider.set(0)
        logging.warning("No audio to scroll")

def on_volume_scroll(event):
    mixer.music.set_volume(volume_slider.get())

def start_test():
    app.allow_connections = True
    connection.configure(text="Allowed", text_color="green")
    logging.info("Test started")

def stop_test():
    app.allow_connections = False
    connection.configure(text="Blocked", text_color="red")
    logging.info("Test stopped")

def close():
    logging.info("Closing app")
    kill(getpid(), SIGTERM)

'''Root init'''
root = ctk.CTk()
root.geometry("1280x720")
root.title("Adaptive Testing Dashboard")
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")
student_data: dict = {}
audio_file = 0
playback = 0

'''Main'''
# Top
top_frame = ctk.CTkFrame(root, corner_radius=20)
top_label = ctk.CTkLabel(top_frame, text="Adaptive Test Dashboard", font=("Arial", 36, "bold"))

# List
list_frame = ctk.CTkFrame(root, width=170, height=300, corner_radius=20)
list_label = ctk.CTkLabel(list_frame, text="Student IDs", font=("Arial", 24, "bold"), anchor="w")
listbox_scroll = ctk.CTkScrollableFrame(list_frame)
listbox = ttk.Treeview(
    listbox_scroll, 
    show="tree",
    height=60)
treestyle = ttk.Style()
treestyle.theme_use('default')
treestyle.configure(
    "Treeview", 
    background=root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]), 
    foreground=root._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]), 
    fieldbackground=root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]), 
    borderwidth=0)
treestyle.map(
    'Treeview', 
    background=[('selected', root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]))], 
    foreground=[('selected', root._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"]))])
listbox.bind("<<TreeviewSelect>>", on_select)

# Data Labels
data_frame = ctk.CTkFrame(root, corner_radius=20)
data_label = ctk.CTkLabel(data_frame, text="Student Data", font=("Arial", 24, "bold"), anchor="w")
student_name_label = ctk.CTkLabel(data_frame, text="Name: ", font=("Arial", 16, "bold"))
reading_score_label = ctk.CTkLabel(data_frame, text="Reading Score: ", font=("Arial", 16, "bold"))
listening_score_label = ctk.CTkLabel(data_frame, text="Listening Score: ", font=("Arial", 16, "bold"))
writing_prompt_label = ctk.CTkLabel(data_frame, text="\nWriting Prompt: ", font=("Arial", 16, "bold"))
writing_label = ctk.CTkLabel(data_frame, text="Writing: ", font=("Arial", 16, "bold"))
audio_label = ctk.CTkLabel(data_frame, text="Audio: ", font=("Arial", 16, "bold"))
# Data
student_name = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
reading_score = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
listening_score = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
writing_prompt = ctk.CTkLabel(data_frame, text="", font=("Arial", 12), wraplength=500)
writing = ctk.CTkTextbox(data_frame, font=("Arial", 12), width=400, height=300, wrap="word", corner_radius=0, border_spacing=0, fg_color="transparent", state="disabled")
audio_controls = ctk.CTkButton(data_frame, text="\u23F5", font=("Arial", 16, "bold"), width=20, height=20, command=on_play)
audio_slider = ctk.CTkSlider(data_frame, command=on_audio_scroll)
volume_icon = ctk.CTkLabel(data_frame, text="\U0001F50A", font=("Arial", 24, "bold"))
volume_slider = ctk.CTkSlider(data_frame, width=100, command=on_volume_scroll)
audio_slider.set(0)
volume_slider.set(1)

# Action
action_frame = ctk.CTkFrame(root, corner_radius=20)
action_label = ctk.CTkLabel(action_frame, text="Actions", font=("Arial", 24, "bold"), anchor="w")
start_test_button = ctk.CTkButton(action_frame, text="Start Test", command=start_test)
stop_test_button = ctk.CTkButton(action_frame, text="Stop Test", command=stop_test)

# Status
status_frame = ctk.CTkFrame(root, corner_radius=20)
status_label = ctk.CTkLabel(status_frame, text="Status", font=("Arial", 24, "bold"))
connection_label = ctk.CTkLabel(status_frame, text="Connection: ", font=("Arial", 16, "bold"))
users_label = ctk.CTkLabel(status_frame, text="Active Connections: ", font=("Arial", 16, "bold"))
connection = ctk.CTkLabel(status_frame, text="Blocked", text_color="red", font=("Arial", 14, "bold"))
users = ctk.CTkLabel(status_frame, text="", font=("Arial", 14, "bold"))
ip_label = ctk.CTkLabel(status_frame, text="\nIP Address: " + gethostbyname_ex(getfqdn())[1][0] + ":3001", font=("Arial", 16, "bold"))
# ip_label = ctk.CTkLabel(status_frame, text="IP Address not found")

'''Pack/Grid'''
# Gridsetup
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=5)
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=4)
root.columnconfigure(2, weight=1)
data_frame.columnconfigure((0, 4), weight=2)
data_frame.columnconfigure((1, 3), weight=1)
data_frame.columnconfigure(2, weight=4)

# Top
top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
top_label.pack(side="top", pady=20)

# List
list_frame.grid(row=1, column=0, rowspan=2, padx=10, pady=(0, 10), sticky="nsew")
list_label.pack(side="top", fill="x", pady=10, padx=15)
listbox_scroll.pack(side="top", fill="both", padx=10, pady=(0, 10), expand=True)
listbox.pack(side="top", expand=True, fill="both")

# Data labels
data_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=(0, 10), sticky="nsew")
data_label.grid(row=0, sticky="n", pady=10, padx=15)
student_name_label.grid(row=1, column=0, sticky="nw", padx=15)
reading_score_label.grid(row=2, column=0, sticky="nw", padx=15)
listening_score_label.grid(row=3, column=0, sticky="nw", padx=15)
writing_prompt_label.grid(row=4, column=0, sticky="nw", padx=15)
writing_label.grid(row=5, column=0, sticky="nw", padx=15)
audio_label.grid(row=6, column=0, sticky="nw", padx=15)
# Data
student_name.grid(row=1, column=1, columnspan=4, sticky="w")
reading_score.grid(row=2, column=1, columnspan=4, sticky="w")
listening_score.grid(row=3, column=1, columnspan=4, sticky="w")
writing_prompt.grid(row=4, column=1, columnspan=4, sticky="w")
writing.grid(row=5, column=1, columnspan=4, sticky="w")
audio_controls.grid(row=6, column=1)
audio_slider.grid(row=6, column=2, sticky="w")
volume_icon.grid(row=6, column=3, sticky="e")
volume_slider.grid(row=6, column=4, sticky="w")

# Action
action_frame.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="nsew")
action_label.pack(side="top", fill="x", padx=15, pady=10)
start_test_button.pack(side="top", fill="x", padx=10, pady=(10, 5))
stop_test_button.pack(side="top", fill="x", padx=10, pady=5)

# Status
status_frame.grid(row=2, column=2, padx=20, pady=(0, 10), sticky="nsew")
status_label.grid(row=0, column=0, columnspan=2, pady=10, padx=15)
connection_label.grid(row=1, column=0, padx=10, sticky="nw")
users_label.grid(row=2, column=0, padx=10, sticky="nw")
connection.grid(row=1, column=1, sticky="w")
users.grid(row=2, column=1, sticky="w")
ip_label.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")

'''Init'''
mixer.init() # Mixer initialization
updates() # Initial update call
flask_thread = Thread(target=app.run) 
flask_thread.start() # Start server
root.protocol("WM_DELETE_WINDOW", close) # Exit cleanup, kill server
root.mainloop()