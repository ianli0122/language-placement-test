import os, json, threading, signal
import app
import customtkinter as ctk
from tkinter import ttk

'''Methods'''
def update_data():
    for item in os.listdir("student_data"): # Loop through student_data directory
        if os.path.isdir(f"student_data/{item}") and item.startswith("1000") and len(item) == 9: # Check if folder is valid
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
                with open(f"student_data/{item}/scores.json", 'r', encoding = "utf-8") as file: # Update student data
                    student_data[item] = json.load(file) # Reload json data
            except:
                pass
    root.after(3000, update_data) # Refresh every 3s

def on_select(event):
    student = listbox.item(listbox.focus(), "text")
    if student in student_data: # TODO only get data when it exists
        student_name.configure(text=student_data[student]["name"])
        reading_score.configure(text=student_data[student]["reading"])
        listening_score.configure(text=student_data[student]["listening"])
        writing_prompt.configure(text=student_data[student]["writing prompt"])
        writing.configure(state="normal")
        writing.delete("1.0", "end")
        writing.insert("1.0", student_data[student]["writing"])
        writing.configure(state="disabled")

def start_test():
    app.allow_connections = True

def stop_test():
    app.allow_connections = False

# Root Init
root = ctk.CTk()
root.geometry("1280x720")
root.title("Adaptive Testing Dashboard")
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("light")
student_data: dict = {}

'''Main'''
# Top
top_frame = ctk.CTkFrame(root)
top_label = ctk.CTkLabel(top_frame, text="Adaptive Test Dashboard", font=("Arial", 36, "bold"))

# Left
left_frame = ctk.CTkFrame(root, width=170, height=300, corner_radius=20)
left_label = ctk.CTkLabel(left_frame, text="Student IDs", font=("Arial", 24, "bold"))
listbox_scroll = ctk.CTkScrollableFrame(left_frame)
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
listening_score_lable = ctk.CTkLabel(data_frame, text="Listening Score: ", font=("Arial", 16, "bold"))
gap = ctk.CTkLabel(data_frame, text="")
writing_prompt_label = ctk.CTkLabel(data_frame, text="Writing Prompt: ", font=("Arial", 16, "bold"))
writing_label = ctk.CTkLabel(data_frame, text="Writing: ", font=("Arial", 16, "bold"))
student_name = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
reading_score = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
listening_score = ctk.CTkLabel(data_frame, text="", font=("Arial", 12))
writing_prompt = ctk.CTkLabel(data_frame, text="", font=("Arial", 12), wraplength=500)
writing = ctk.CTkTextbox(data_frame, font=("Arial", 12), width=400, height=300, wrap="word", corner_radius=0, border_spacing=0, fg_color="transparent")

# Right
right_frame = ctk.CTkFrame(root, corner_radius=20)
right_label = ctk.CTkLabel(right_frame, text="Actions", font=("Arial", 24, "bold"), anchor="w")
start_test_button = ctk.CTkButton(right_frame, text="Start Test", command=start_test)
stop_test_button = ctk.CTkButton(right_frame, text="Stop Test", command=stop_test)


'''Pack/Grid'''
# Top
top_frame.pack(side="top", fill="x", pady=(0, 10))
top_label.pack(side="top", pady=20)

# Left
left_frame.pack(side="left", fill="y", padx=10, pady=(0, 10))
left_label.pack(side="top", fill="x", pady=10, padx=10)
listbox_scroll.pack(side="top", fill="both", padx=10, pady=(0, 10), expand=True)
listbox.pack(side="top", expand=True, fill="both")

# Right
right_frame.pack(side="right", fill="y", padx=10, pady=(0, 10))
right_label.pack(side="top", fill="x", padx=15, pady=10)
start_test_button.pack(side="top", fill="x", padx=10, pady=(10, 5))
stop_test_button.pack(side="top", fill="x", padx=10, pady=5)

# Data
data_frame.pack(side="right", fill="both", expand=True, padx=10, pady=(0, 10))
data_label.grid(row=0, sticky="n", pady=10, padx=15)
student_name_label.grid(row=1, column=0, sticky="nw", padx=10)
reading_score_label.grid(row=2, column=0, sticky="nw", padx=10)
listening_score_lable.grid(row=3, column=0, sticky="nw", padx=10)
gap.grid(row=4, columnspan=2)
writing_prompt_label.grid(row=5, column=0, sticky="nw", padx=10)
writing_label.grid(row=6, column=0, sticky="nw", padx=10)
student_name.grid(row=1, column=1, sticky="w")
reading_score.grid(row=2, column=1, sticky="w")
listening_score.grid(row=3, column=1, sticky="w")
writing_prompt.grid(row=5, column=1, sticky="w")
writing.grid(row=6, column=1, sticky="w")


update_data() # Initial update data
flask_thread = threading.Thread(target=app.run) 
flask_thread.start() # Start server
root.protocol("WM_DELETE_WINDOW", lambda: os.kill(os.getpid(), signal.SIGTERM)) # Exit cleanup, kill server
root.mainloop()