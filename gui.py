import tkinter as tk
from tkinter import ttk

# Function to generate feedback
def generate_feedback():
    user_feedback_text.config(state='normal')
    user_feedback_text.delete("1.0", tk.END)
    user_feedback_text.insert(tk.END, "PLACEHOLDER FEEDBACK")
    user_feedback_text.config(state='disabled')

# Function to generate progress report
def generate_progress_report():
    progress_window = tk.Toplevel()
    progress_window.title("Progress Report")
    progress_label = tk.Label(progress_window, text="Progress Report")
    progress_label.pack()
    progress_text = tk.Text(progress_window, height=10, width=40)
    progress_text.pack()
    progress_text.insert(tk.END, "PLACEHOLDER PROGRESS REPORT")
    progress_text.config(state=tk.DISABLED)

# Function to generate question
def generate_question():
    # Clear user feedback
    user_feedback_text.config(state='normal')
    user_feedback_text.delete("1.0", tk.END)
    user_feedback_text.config(state='disabled')

    # Clear user answer
    user_answer_text.delete("1.0", tk.END)

    # Clear old question
    question_feedback_text.config(state='normal')
    question_feedback_text.delete("1.0", tk.END)
    

    # Generate new question
    question_feedback_text.insert(tk.END, "PLACEHOLDER QUESTION")
    question_feedback_text.config(state='disabled')

# Create the main window
root = tk.Tk()
root.title("Quiz Generator")

# Set the size of the window
root.geometry("800x600")

# Create frames for layout
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Create and place the topic selection widgets
topic_label = tk.Label(top_frame, text="Select Topic:")
topic_label.pack(side=tk.TOP, padx=5, pady=5)

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

topic_combobox = ttk.Combobox(top_frame, values=topics_list, state="readonly")
topic_combobox.pack(side=tk.TOP, padx=5, pady=5)

# Create and place the difficulty selection widgets
difficulty_label = tk.Label(top_frame, text="Select Difficulty:")
difficulty_label.pack(side=tk.TOP, padx=5, pady=5)

difficulty_list =  ['Easy', 'Medium', 'Hard']

difficulty_combobox = ttk.Combobox(top_frame, values=difficulty_list, state="readonly")
difficulty_combobox.pack(side=tk.TOP, padx=5, pady=5)

# Create and place the generate question button
generate_button = tk.Button(top_frame, text="Generate Question", command=generate_question)
generate_button.pack(side=tk.TOP, padx=5, pady=5)

# Create and place the question and feedback text area
question_feedback_label = tk.Label(left_frame, text="Question:")
question_feedback_label.pack(side=tk.TOP, padx=5, pady=5)

question_feedback_text = tk.Text(left_frame, height=10, width=40, wrap='word', state='disabled')
question_feedback_text.pack(side=tk.TOP, padx=5, pady=5)

# Create and place the user answer text area
user_answer_label = tk.Label(right_frame, text="Your Answer:")
user_answer_label.pack(side=tk.TOP, padx=5, pady=5)

user_answer_text = tk.Text(right_frame, height=10, width=40)
user_answer_text.pack(side=tk.TOP, padx=5, pady=5)

# Create and place the feedback text area
user_feedback_label = tk.Label(right_frame, text="Feedback:")
user_feedback_label.pack(side=tk.TOP, padx=5, pady=5)

user_feedback_text = tk.Text(right_frame, height=10, width=40, wrap='word', state='disabled')
user_feedback_text.pack(side=tk.TOP, padx=5, pady=5)

# Create and place the submit button
submit_button = tk.Button(bottom_frame, text="Submit", height=2, width=8, command=generate_feedback)
submit_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create and place the generate progress report button
progress_report_button = tk.Button(bottom_frame, text="Generate \nProgress Report", height=2, width=15, command=generate_progress_report)
progress_report_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the application
root.mainloop()
