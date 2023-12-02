import tkinter as tk
from tkinter import ttk

def submit_answer():
    # Placeholder function for submitting an answer
    print("Answer submitted.")

def request_feedback():
    # Placeholder function for requesting feedback
    feedback = "Sample Feedback"
    return feedback

def generate_question():
    # Placeholder for actual question generation logic
    question_text = "New question text here"
    # app.frames[QuestionPage].generate_question(question_text)
    return question_text

def view_progress_report():
    # Placeholder function for viewing progress report
    print("Progress report viewed.")

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LIGN 167 Quiz Generator")

        self.frames = {}
        for F in (MainPage, DifficultyPage, QuestionPage, ProgressReportPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        topics_list = [
            "Supervised Learning",
            "Linear Regression",
            "Logistic Regression",
            "Optimization through Gradient Descent",
            "Multilayer Perceptrons",
            "Backpropagation",
            "Word2Vec",
            "Autoregressive Models",
            "Attention",
            "Transformers",
            "Autoregressive Language Modeling",
            "Masked Language Modeling",
            "Encoder-decoder Architectures"
        ]

        # Increase the font size for better visibility
        large_font = ('Verdana', 20)  # Example font and size

        topics_label = tk.Label(self, text="Select Topic:", font=large_font)
        topics_label.pack(pady=10)

        # Increase the size of the Combobox
        self.topics = ttk.Combobox(self, values=topics_list, state="readonly", font=large_font)
        self.topics.pack(pady=10)

        enter_button = tk.Button(self, text="Enter", command=lambda: parent.show_frame(DifficultyPage), font=large_font)
        enter_button.pack(pady=20)

class DifficultyPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # Add difficulty selection widgets here
        difficulty_label = tk.Label(self, text="Select Difficulty:")
        
        difficulty_label.pack()
        difficulty = tk.StringVar()
        tk.Radiobutton(self, text="Easy", variable=difficulty, value="easy").pack()
        tk.Radiobutton(self, text="Medium", variable=difficulty, value="medium").pack()
        tk.Radiobutton(self, text="Hard", variable=difficulty, value="hard").pack()

        next_button = tk.Button(self, text="Next", command=lambda: parent.show_frame(QuestionPage))
        next_button.pack(pady=(20, 5))  # Increase space above the "Next" button

        back_button = tk.Button(self, text="Back", command=lambda: parent.show_frame(MainPage))
        back_button.pack(pady=(5, 20))  # Increase space below the "Back" button

class QuestionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Label for the question display
        question_label = tk.Label(self, text="Question")
        question_label.pack(pady=(10, 0))

        # Text area for displaying the question (read-only)
        self.question_display = tk.Text(self, height=5, width=50, wrap='word', state='disabled')
        self.question_display.pack(pady=(10, 0))

        # Label for the answer input
        answer_label = tk.Label(self, text="Answer")
        answer_label.pack(pady=(5, 0))

        # Textbox for user input (larger size)
        self.answer_input = tk.Text(self, height=5, width=50)  # Adjust height as needed
        self.answer_input.pack(pady=(5, 10))

         # Submit Answer Button
        self.submit_button = tk.Button(self, text="Submit Answer", command=self.update_question)
        self.submit_button.pack()


        # Feedback label and text box (read-only)
        feedback_label = tk.Label(self, text="Feedback")
        feedback_label.pack(pady=(5, 0))
        self.feedback_display = tk.Text(self, height=5, width=50, wrap='word', state='disabled')
        self.feedback_display.pack(pady=(0, 10))

        # Preload the first question
        self.first_question = True
        self.update_question()

        # New Question Button
        self.new_question_button = tk.Button(self, text="New Question", command=self.update_question)
        self.new_question_button.pack()

        progress_button = tk.Button(self, text="Generate Progress Report", command=lambda: parent.show_frame(ProgressReportPage))
        progress_button.pack(pady=5)

        back_button = tk.Button(self, text="Back", command=lambda: parent.show_frame(DifficultyPage))
        back_button.pack(pady=5)

    def submit_answer(self):
        # Placeholder for actual answer submission logic and feedback generation
        feedback_text = request_feedback()
        self.update_feedback(feedback_text)
        self.answer_input.delete(1.0, 'end')  # Clear the answer input

    def generate_new_question(self):
        # Placeholder for actual new question generation logic
        self.update_feedback("")  # Clear the feedback
        self.answer_input.delete(1.0, 'end')  # Clear the answer input

    def update_question(self):
        # Clear current question and answer
        self.question_display.config(state='normal')
        self.question_display.delete(1.0, tk.END)

        # Insert new question
        new_question_text = generate_question()
        self.question_display.insert(tk.END, new_question_text)
        self.question_display.config(state='disabled')

        # Clear the answer input
        self.answer_input.delete(1.0, tk.END)

        # Update the feedback
        if not self.first_question:
            feedback = request_feedback()
            self.update_feedback(feedback)
        else:
            self.first_question = False

    def update_feedback(self, feedback_text):
        self.feedback_display.config(state='normal')  # Enable editing to update text
        self.feedback_display.delete(1.0, 'end')  # Clear existing text
        self.feedback_display.insert('end', feedback_text)  # Insert new feedback text
        self.feedback_display.config(state='disabled')  # Set back to read-only

class ProgressReportPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        progress_report_label = tk.Label(self, text="Progress Report", font=('Verdana', 12))  # Adjust font size as needed
        progress_report_label.pack(pady=(10, 0))

        self.progress_report_display = tk.Text(self, height=10, width=50, wrap='word', state='disabled')  # Set state to disabled
        self.progress_report_display.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=lambda: parent.show_frame(QuestionPage))
        back_button.pack(pady=5)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()