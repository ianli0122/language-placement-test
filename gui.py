import os, json, subprocess, sys, requests
import tkinter as tk
from tkinter import ttk

# Methods
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
                    student_data[item] = json.load(file)
            except:
                pass
    root.after(3000, update_data)

def on_select(event):
    student = listbox.item(listbox.focus(), "text")
    if student in student_data: # TODO only get data when it exists
        student_name["text"] = student_data[student]["name"]
        reading_score["text"] = student_data[student]["reading"]
        listening_score["text"] = student_data[student]["listening"]
        writing_prompt["text"] = student_data[student]["writing prompt"]
        writing["text"] = student_data[student]["writing"]

def start_app():
    process = subprocess.Popen([sys.executable, "app.py"])
    print(process.pid)

def stop_app():
    response = requests.post("http://localhost:3001/shutdown") # TODO figure out how to shutdown https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    if response.status_code == 200:
        print("shutdown")
    else:
        print("bad shutdown")

# Initial config
root = tk.Tk()
root.geometry("1280x720")
root.title("Adaptive Test Dashboard")

# Data initialization
student_data: dict = {}

# Styles
s = ttk.Style()
s.configure("Top.TFrame", background="#2d9ccc")
s.configure("Top.TLabel", background="#2d9ccc", foreground="white", font=("Arial", 36, "bold"))
s.configure("Title.TLabel", font=("Arial", 24, "bold"))
s.configure("DataType.TLabel", font=("Arial", 16, "bold"))
s.configure("Data.TLabel", font=("Arial", 12), wraplength=500)

# Main
# Top
top_frame = ttk.Frame(root, style="Top.TFrame")
top_label = ttk.Label(top_frame, text="Adaptive Test Dashboard", style="Top.TLabel")

# Left
left_frame = ttk.Frame(root)
scrollbar = ttk.Scrollbar(left_frame)
left_label = ttk.Label(left_frame, text="Student IDs", style="Title.TLabel")
listbox = ttk.Treeview(left_frame, yscrollcommand=scrollbar.set, show="tree")
listbox.bind("<<TreeviewSelect>>", on_select)
scrollbar["command"] = listbox.yview

# Center
data_frame = ttk.Frame(root)
data_label = ttk.Label(data_frame, text="Student Data", style="Title.TLabel")
student_name_label = ttk.Label(data_frame, text="Name: ", style="DataType.TLabel")
reading_score_label = ttk.Label(data_frame, text="Reading Score: ", style="DataType.TLabel")
listening_score_lable = ttk.Label(data_frame, text="Listening Score: ", style="DataType.TLabel")
gap = ttk.Label(data_frame)
writing_prompt_label = ttk.Label(data_frame, text="Writing Prompt: ", style="DataType.TLabel")
writing_label = ttk.Label(data_frame, text="Writing: ", style="DataType.TLabel")

student_name = ttk.Label(data_frame, style="Data.TLabel")
reading_score = ttk.Label(data_frame, style="Data.TLabel")
listening_score = ttk.Label(data_frame, style="Data.TLabel")
writing_prompt = ttk.Label(data_frame, style="Data.TLabel")
writing = ttk.Label(data_frame, style="Data.TLabel")

# Right
right_frame = ttk.Frame(root)
start_button = ttk.Button(right_frame, text="Start Test", command=lambda: start_app())
stop_button = ttk.Button(right_frame, text="Stop Test", command=lambda: stop_app())


# Packing
top_frame.pack(side="top", fill="x", pady=(0, 20))
top_label.pack(side="top", pady=(10, 10))

left_frame.pack(side="left", fill="y", padx=20, pady=(0, 20))
left_label.pack(side="top", fill="x")
scrollbar.pack(side="right", fill="y")
listbox.pack(side="left", expand=True, fill="both")

data_frame.pack(side="right", fill="both", expand=True)
data_label.grid(row=0, columnspan=2, sticky=tk.NW)
student_name_label.grid(row=1, column=0, sticky=tk.NW)
reading_score_label.grid(row=2, column=0, sticky=tk.NW)
listening_score_lable.grid(row=3, column=0, sticky=tk.NW)
gap.grid(row=4, columnspan=2)
writing_prompt_label.grid(row=5, column=0, sticky=tk.NW)
writing_label.grid(row=6, column=0, sticky=tk.NW)
student_name.grid(row=1, column=1, sticky=tk.W)
reading_score.grid(row=2, column=1, sticky=tk.W)
listening_score.grid(row=3, column=1, sticky=tk.W)
writing_prompt.grid(row=5, column=1, sticky=tk.W)
writing.grid(row=6, column=1, sticky=tk.W)

right_frame.pack(side="right", fill="y")
start_button.pack(side="top") # TODO fix button packing
stop_button.pack(side="top")

update_data()
root.mainloop()