import tkinter as tk
from tkinter import messagebox
import threading
import time

# Quiz Data (can be loaded from file later)
quiz_data = {
    "General Knowledge": [
        {"question": "What is the capital of Italy?", "options": ["Rome", "Paris", "Madrid", "Berlin"], "answer": "Rome"},
        {"question": "Who wrote 'Hamlet'?", "options": ["Charles Dickens", "William Shakespeare", "Leo Tolstoy", "Jane Austen"], "answer": "William Shakespeare"},
    ],
    "Technology": [
        {"question": "What does HTML stand for?", "options": ["HighText Machine Language", "HyperText Markup Language", "HyperText Markdown Language", "None"], "answer": "HyperText Markup Language"},
        {"question": "Python was created by?", "options": ["Guido van Rossum", "Dennis Ritchie", "Elon Musk", "Mark Zuckerberg"], "answer": "Guido van Rossum"},
    ],
    "Science": [
        {"question": "What planet is known as the Red Planet?", "options": ["Earth", "Venus", "Mars", "Jupiter"], "answer": "Mars"},
        {"question": "What is H2O?", "options": ["Helium", "Water", "Oxygen", "Hydrogen"], "answer": "Water"},
    ]
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unique Quiz App")
        self.root.geometry("600x400")

        self.category = tk.StringVar()
        self.question_index = 0
        self.score = 0
        self.timer = 15
        self.selected_option = tk.StringVar()

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Select Quiz Category", font=("Arial", 18, "bold")).pack(pady=30)

        for category in quiz_data.keys():
            tk.Radiobutton(self.root, text=category, variable=self.category, value=category,
                           font=("Arial", 14)).pack(anchor='w', padx=100)

        tk.Button(self.root, text="Start Quiz", font=("Arial", 14, "bold"), bg="green", fg="white",
                  command=self.start_quiz).pack(pady=30)

    def start_quiz(self):
        if self.category.get() == "":
            messagebox.showwarning("Warning", "Please select a category!")
            return

        self.questions = quiz_data[self.category.get()]
        self.question_index = 0
        self.score = 0
        self.load_question()

    def load_question(self):
        self.clear_screen()
        self.selected_option.set("")
        self.timer = 15

        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.timer}s", font=("Arial", 12), fg="red")
        self.timer_label.pack(anchor='ne', padx=20, pady=5)

        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

        question_data = self.questions[self.question_index]

        tk.Label(self.root, text=f"Q{self.question_index + 1}: {question_data['question']}",
                 font=("Arial", 16), wraplength=550).pack(pady=20)

        for opt in question_data["options"]:
            tk.Radiobutton(self.root, text=opt, variable=self.selected_option, value=opt,
                           font=("Arial", 14)).pack(anchor='w', padx=50, pady=2)

        self.progress_label = tk.Label(self.root, text=f"Question {self.question_index + 1} of {len(self.questions)}",
                                       font=("Arial", 12), fg="blue")
        self.progress_label.pack(pady=10)

        tk.Button(self.root, text="Next", command=self.check_answer, font=("Arial", 14), bg="#2196F3", fg="white").pack(pady=10)

    def update_timer(self):
        while self.timer > 0:
            time.sleep(1)
            self.timer -= 1
            self.timer_label.config(text=f"Time Left: {self.timer}s")
        if self.timer == 0:
            self.check_answer(timeout=True)

    def check_answer(self, timeout=False):
        if self.timer == 0 or timeout:
            pass  # Timeout, no score added
        elif self.selected_option.get() == self.questions[self.question_index]['answer']:
            self.score += 1

        self.question_index += 1
        if self.question_index < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()
        percent = (self.score / len(self.questions)) * 100
        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 18, "bold"), fg="green").pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score} / {len(self.questions)}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Percentage: {percent:.2f}%", font=("Arial", 14)).pack(pady=5)

        tk.Button(self.root, text="Try Again", font=("Arial", 14), command=self.create_start_screen).pack(pady=20)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.root.destroy).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run App
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
