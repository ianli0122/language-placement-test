from os import kill, getpid, listdir, path
from socket import getfqdn, gethostbyname_ex
from threading import Thread
from signal import SIGTERM
from json import load
import app, sessions
import customtkinter as ctk
from tkinter import ttk

'''Methods'''
def update_student_data():
    print("update")
    for item in listdir("data/student_data"): # Loop through student_data directory
        if path.isdir(f"data/student_data/{item}") and item.startswith("1000") and len(item) == 9: # Check if folder is valid
            if item not in student_data: # Student not in database yet
                student_data[item] = {}
                inserted = False
                for index, i in enumerate(listbox.get_children()):
                    if int(item) < int(listbox.item(i, "text")):
                        listbox.insert("", index, text=item)
                        inserted = True
                        break
                if not inserted:
                    listbox.insert("", "end", text=item)
            try:
                with open(f"data/student_data/{item}/scores.json", 'r', encoding = "utf-8") as file: # Update student data
                    student_data[item] = load(file) # Reload json data
            except:
                pass
    root.after(2000, update_student_data) # Refresh every 3s

def update_connections():
    users.configure(text=str(sessions.total_session()))
    root.after(2000, update_connections)

def on_select(event):
    student = listbox.item(listbox.focus(), "text")
    student_name.configure(text="")
    reading_score.configure(text="")
    listening_score.configure(text="")
    writing_prompt.configure(text="")
    writing.configure(state="normal")
    writing.delete("1.0", "end")
    writing.configure(state="disabled")

    try:
        student_name.configure(text=student_data[student]["name"])
        reading_score.configure(text=student_data[student]["reading"])
        listening_score.configure(text=student_data[student]["listening"])
        writing_prompt.configure(text="\n\n" + student_data[student]["writing prompt"])
        writing.configure(state="normal")
        writing.insert("1.0", "\n" + student_data[student]["writing"])
        writing.configure(state="disabled")
    except:
        pass

def start_test():
    app.allow_connections = True
    connection.configure(text="Allowed", text_color="green")

def stop_test():
    app.allow_connections = False
    connection.configure(text="Blocked", text_color="red")

def close():
    kill(getpid(), SIGTERM)

# Root Init
root = ctk.CTk()
root.geometry("1280x720")
root.title("Adaptive Testing Dashboard")
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")
student_data: dict = {}

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

# Data
data_frame = ctk.CTkFrame(root, corner_radius=20)
data_label = ctk.CTkLabel(data_frame, text="Student Data", font=("Arial", 24, "bold"), anchor="w")
student_name_label = ctk.CTkLabel(data_frame, text="Name: ", font=("Arial", 16, "bold"))
reading_score_label = ctk.CTkLabel(data_frame, text="Reading Score: ", font=("Arial", 16, "bold"))
listening_score_label = ctk.CTkLabel(data_frame, text="Listening Score: ", font=("Arial", 16, "bold"))
writing_prompt_label = ctk.CTkLabel(data_frame, text="\nWriting Prompt: ", font=("Arial", 16, "bold"))
writing_label = ctk.CTkLabel(data_frame, text="Writing: ", font=("Arial", 16, "bold"))
student_name = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
reading_score = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
listening_score = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
writing_prompt = ctk.CTkLabel(data_frame, text="", font=("Arial", 12), wraplength=500)
writing = ctk.CTkTextbox(data_frame, font=("Arial", 12), width=400, height=300, wrap="word", corner_radius=0, border_spacing=0, fg_color="transparent", state="disabled")

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
ip_label = ctk.CTkLabel(status_frame, text="\nIP Address: " + gethostbyname_ex(getfqdn())[2][1] + ":3001", font=("Arial", 16, "bold"))


'''Pack/Grid'''
# Gridsetup
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=5)
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=4)
root.columnconfigure(2, weight=1)

# Top
top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
top_label.pack(side="top", pady=20)

# List
list_frame.grid(row=1, column=0, rowspan=2, padx=10, pady=(0, 10), sticky="nsew")
list_label.pack(side="top", fill="x", pady=10, padx=15)
listbox_scroll.pack(side="top", fill="both", padx=10, pady=(0, 10), expand=True)
listbox.pack(side="top", expand=True, fill="both")

# Data
data_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=(0, 10), sticky="nsew")
data_label.grid(row=0, sticky="n", pady=10, padx=15)
student_name_label.grid(row=1, column=0, sticky="nw", padx=10)
reading_score_label.grid(row=2, column=0, sticky="nw", padx=10)
listening_score_label.grid(row=3, column=0, sticky="nw", padx=10)
writing_prompt_label.grid(row=4, column=0, sticky="nw", padx=10)
writing_label.grid(row=5, column=0, sticky="nw", padx=10)
student_name.grid(row=1, column=1, sticky="w")
reading_score.grid(row=2, column=1, sticky="w")
listening_score.grid(row=3, column=1, sticky="w")
writing_prompt.grid(row=4, column=1, sticky="w")
writing.grid(row=5, column=1, sticky="w")

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

update_student_data() # Initial update data
update_connections()
flask_thread = Thread(target=app.run) 
flask_thread.start() # Start server
root.protocol("WM_DELETE_WINDOW", close) # Exit cleanup, kill server
root.mainloop()