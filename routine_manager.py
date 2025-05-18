import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time as systime
import threading

class RoutineManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Routine Manager")
        self.root.geometry("500x550")
        self.root.configure(bg="#f0f4f7")
        self.tasks = []

        title_label = tk.Label(root, text="Routine Manager", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#2a4d69")
        title_label.pack(pady=10)

        # Current time display
        self.time_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f4f7", fg="#2a4d69")
        self.time_label.pack(pady=5)
        self.update_clock()

        time_frame = tk.Frame(root, bg="#f0f4f7")
        time_frame.pack(pady=5)

        # Time selectors
        self.start_hour = ttk.Combobox(time_frame, values=[f"{i:02}" for i in range(24)], width=3)
        self.start_minute = ttk.Combobox(time_frame, values=[f"{i:02}" for i in range(60)], width=3)
        self.end_hour = ttk.Combobox(time_frame, values=[f"{i:02}" for i in range(24)], width=3)
        self.end_minute = ttk.Combobox(time_frame, values=[f"{i:02}" for i in range(60)], width=3)

        self.start_hour.set("08")
        self.start_minute.set("00")
        self.end_hour.set("09")
        self.end_minute.set("00")

        tk.Label(time_frame, text="Start Time", bg="#f0f4f7", fg="#2a4d69").grid(row=0, column=0, padx=5, pady=2)
        self.start_hour.grid(row=0, column=1)
        self.start_minute.grid(row=0, column=2)

        tk.Label(time_frame, text="End Time", bg="#f0f4f7", fg="#2a4d69").grid(row=1, column=0, padx=5, pady=2)
        self.end_hour.grid(row=1, column=1)
        self.end_minute.grid(row=1, column=2)

        # Task entry with placeholder
        self.task_entry = ttk.Entry(root, width=60)
        self.task_entry.configure(foreground='grey')
        self.task_entry.insert(0, "Enter your task here")
        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
        self.task_entry.bind("<FocusOut>", self.restore_placeholder)
        self.task_entry.bind("<Return>", self.add_task)
        self.task_entry.pack(pady=10)

        # Display area
        display_frame = tk.Frame(root)
        display_frame.pack(pady=10)
        self.task_display = tk.Text(display_frame, height=12, width=60, bg="#ffffff", fg="#333333", wrap=tk.WORD)
        self.task_display.pack()

        self.current_task_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), bg="#f0f4f7", fg="green")
        self.current_task_label.pack(pady=5)

        # Start checking the routine
        threading.Thread(target=self.check_routine, daemon=True).start()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Current Time: {now}")
        self.root.after(1000, self.update_clock)

    def clear_placeholder(self, event):
        if self.task_entry.get() == "Enter your task here":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(foreground='white')

    def restore_placeholder(self, event):
        if not self.task_entry.get():
            self.task_entry.insert(0, "Enter your task here")
            self.task_entry.config(foreground='grey')

    def add_task(self, event=None):
        start = f"{self.start_hour.get()}:{self.start_minute.get()}"
        end = f"{self.end_hour.get()}:{self.end_minute.get()}"
        task = self.task_entry.get()

        if task == "Enter your task here" or not task:
            return

        new_start = datetime.strptime(start, "%H:%M")
        new_end = datetime.strptime(end, "%H:%M")

        if new_start >= new_end:
            return

        now = datetime.now().strftime("%H:%M")
        self.tasks.append((start, end, task))
        self.task_display.insert(tk.END, f"{start} - {end}: {task}\n")
        self.task_entry.delete(0, tk.END)
        self.restore_placeholder(None)

        if start <= now <= end:
            self.highlight_task(start, end, task)
            self.current_task_label.config(text=f"Current Task: {task}")

    def check_routine(self):
        while True:
            now = datetime.now().strftime("%H:%M")
            task_found = False
            for start, end, task in self.tasks:
                if start <= now <= end:
                    self.highlight_task(start, end, task)
                    self.current_task_label.config(text=f"Current Task: {task}")
                    task_found = True
                    break
            if not task_found:
                self.task_display.tag_remove("highlight", "1.0", tk.END)
                self.current_task_label.config(text="No task scheduled right now.")
            systime.sleep(30)

    def highlight_task(self, start, end, task):
        self.task_display.tag_remove("highlight", "1.0", tk.END)
        lines = self.task_display.get("1.0", tk.END).split("\n")
        for i, line in enumerate(lines):
            if f"{start} - {end}: {task}" in line:
                self.task_display.tag_add("highlight", f"{i+1}.0", f"{i+1}.end")
                self.task_display.tag_config("highlight", background="#ffeb3b")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = RoutineManager(root)
    root.mainloop()




