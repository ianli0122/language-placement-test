import os
import json
import tkinter as tk
from tkinter import ttk

class AdaptiveTestApp:
    student_ids: list[str]
    student_details: dict

    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Test")
        self.root.geometry("800x700")
        self.root.configure(background="grey")

        self.student_ids = []
        self.student_details = {}

        # Apply custom style
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 24))
        self.style.configure("Details.TLabel", font=("Helvetica", 12))

        self.create_widgets()
        self.update_data()
        self.root.after(10000, self.update_data)  # Schedule the directory scan every 10 seconds

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="20")
        top_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

        title_label = ttk.Label(top_frame, text="Adaptive Test", font=("Helvetica", 30, "bold"), foreground="blue")
        title_label.grid(row=0, column=0, pady=10)

        # Left Frame for Student IDs
        left_frame = ttk.Frame(self.root, padding="20")
        left_frame.grid(row=1, column=0, sticky="nsew")

        # Student IDs Listbox
        self.student_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE, height=30, width=20, borderwidth=4)
        self.student_listbox.pack(fill=tk.BOTH, expand=True)
        self.student_listbox.bind('<<ListboxSelect>>', self.on_select)

        # Right Frame for Student Details
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.grid(row=1, column=1, sticky="nsew")

        # Title Label
        student_label = ttk.Label(right_frame, text="Student Details", style="Title.TLabel")
        student_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Labels for Student Details
        self.name_label = ttk.Label(right_frame, text="Name: ", style="Details.TLabel")
        self.name_label.grid(row=1, column=0, sticky=tk.W)

        self.reading_score_label = ttk.Label(right_frame, text="Reading Score: ", style="Details.TLabel")
        self.reading_score_label.grid(row=2, column=0, sticky=tk.W)

        self.listening_score_label = ttk.Label(right_frame, text="Listening Score: ", style="Details.TLabel")
        self.listening_score_label.grid(row=3, column=0, sticky=tk.W)

        ttk.Label(right_frame).grid(row=4, column=0)

        self.writing_prompt_label = ttk.Label(right_frame, text="Writing Prompt: ", style="Details.TLabel")
        self.writing_prompt_label.grid(row=5, column=0, sticky=tk.W)

        self.writing_label = ttk.Label(right_frame, text="Writing: ", style="Details.TLabel", wraplength=500)
        self.writing_label.grid(row=6, column=0, sticky=tk.W)

    def on_select(self, event):
        # Clear previous details
        self.name_label["text"] = "Name: "
        self.reading_score_label["text"] = "Reading Score: "
        self.listening_score_label["text"] = "Listening Score: "
        self.writing_prompt_label["text"] = "Writing Prompt: "
        self.writing_label["text"] = "Writing: "

        # Get selected student ID
        selected_index = self.student_listbox.curselection()
        if selected_index:
            student_id = self.student_listbox.get(selected_index)
            student_detail = self.student_details.get(student_id)
            if student_detail:
                self.name_label["text"] = "Name: " + student_detail["name"]
                self.reading_score_label["text"] = "Reading Score: " + str(student_detail["reading"])
                self.listening_score_label["text"] = "Listening Score: " + str(student_detail["listening"])
                self.writing_prompt_label["text"] = "Writing Prompt: " + student_detail["writing prompt"]
                self.writing_label["text"] = "Writing: " + student_detail["writing"]

    def update_data(self):
        for item in os.listdir("student_data"): # Loop through student_data directory
            if os.path.isdir(f"student_data/{item}") and item[0:4] == "1000" and len(item) == 9: # Check if folder is valid
                if item not in self.student_ids: # Student not in database yet
                    self.student_ids.append(item)
                    self.student_details[item] = {}
                    self.student_listbox.insert(tk.END, item)
        
                with open(f"student_data/{item}/scores.json", 'r', encoding = "utf-8") as file: # Update student data
                    self.student_details[item] = json.load(file)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdaptiveTestApp(root)
    root.mainloop()
