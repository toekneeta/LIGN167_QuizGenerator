import tkinter as tk
from tkinter import ttk, simpledialog
from backend import QuizGenerator

class MultiLineInputDialog(simpledialog.Dialog):
    def body(self, master):
        self.text = tk.Text(master, width=50, height=10, font="Helvetica 10")
        self.text.pack()
        return self.text  # initial focus on the text widget

    def apply(self):
        self.result = self.text.get("1.0", tk.END)  # get text from Text widget

# Function to generate feedback
def generate_feedback():
    question_feedback_text.config(state='normal')
    user_feedback_text.config(state='normal')
    user_feedback_text.delete("1.0", tk.END)

    question = question_feedback_text.get("1.0", tk.END)
    answer = user_answer_text.get("1.0", tk.END)
    topic = topic_combobox.get()
    difficulty = difficulty_combobox.get()


    feedback = qg.provide_feedback(question, answer, topic, difficulty)
    
    user_feedback_text.insert(tk.END, feedback)

    user_feedback_text.config(state='disabled')
    question_feedback_text.config(state='disabled')

    
# Function to generate progress report
def generate_progress_report():
    overall_accuracy_rate, progress_report_stats, struggled_topics, study_tips = qg.create_progress_report()

    progress_window = tk.Toplevel()
    progress_window.geometry("1600x800")
    progress_window.title("Progress Report")
    
    headers = ['Topics', '# of Easy Questions Answered', '# of Medium Questions Answered', '# of Hard Questions Answered', \
               'Easy Accuracy Rate', 'Medium Accuracy Rate', 'Hard Accuracy Rate', 'Topic Accuracy Rate']

    e = tk.Entry(progress_window, width=36, font="Helvetica 8 bold")
    e.grid(row=0, column=0)
    e.insert(tk.END, headers[0])

    for i in range(1, 1 + len(topics_list)):
        e = tk.Entry(progress_window, width=36, font="Helvetica 8")
        e.grid(row=i, column=0)
        e.insert(tk.END, progress_report_stats[i-1][0])

    for j in range(1, 8):
        e = tk.Entry(progress_window, width=32, font="Helvetica 8 bold")
        e.grid(row=0, column=j)
        e.insert(tk.END, headers[j])

        for i in range(1, 1 +len(topics_list)):
            e = tk.Entry(progress_window, width=32, font="Helvetica 8")
            e.grid(row=i, column=j)
            if progress_report_stats[i-1][j] == -1:
                e.insert(tk.END, "")
            elif j < 4:
                e.insert(tk.END, progress_report_stats[i-1][j])
            else:
                e.insert(tk.END, str(progress_report_stats[i-1][j]) + "%")


    progress_text = tk.Text(progress_window, height=30, font="Arial 10")
    progress_text.grid(row=len(topics_list) + 2, column=0, columnspan=8)

    if overall_accuracy_rate == -1:
        progress_str = "Total accuracy rate across topics: \n\n"
    else:
        progress_str = "Total accuracy rate across topics: " + str(overall_accuracy_rate) + "%\n\n"
    progress_str += "Topics to refresh: " + ', '.join(struggled_topics) + '\n\n'
    progress_str += "Tips on studying:\n"

    if struggled_topics:
        progress_str += study_tips

    progress_text.insert(tk.END, progress_str)
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
    
    # Hide hint text area
    hint_label.pack_forget()
    hint_text.configure(bg="#add8e6")
    hint_text.pack_forget()

    # get topic and difficulty
    topic = topic_combobox.get()
    difficulty = difficulty_combobox.get()

    # Generate new question
    question = qg.generate_question(topic, difficulty)

    question_feedback_text.insert(tk.END, question)
    question_feedback_text.config(state='disabled')

def open_help():
    # Create a new top-level window
    help_window = tk.Toplevel(background=bg_color)
    help_window.title("Help")

    # Help text with bold parts
    help_text = (
        "Welcome to the **LIGN 167 Quiz Generator**!\n\n"
        "Here's how to get started:\n\n"
        "1) Select a topic from the dropdown menu\n"
        "2) Select a difficulty from the dropdown menu\n"
        "3) Click the **Generate Question** button to create a new question\n"
        "4) A question will appear in the **Question** box\n"
        "5) Type your answer in the **Answer** box on the right\n"
        "6) Click the **Submit** button at the bottom\n"
        "7) Feedback will be provided in the **Feedback** box below the **Answer** box\n"
        "8) Repeat!\n\n"
        "You may also click on the **Generate Progress Report** button that will \n"
        "generate a progress report with your overall question accuracy, the topics and difficulties \n"
        "that you've covered, the topics you did well in and/or didn't do well in, \n"
        "and tips on how to improve!"
    )

    guide_text = tk.Text(help_window, font="Helvetica 12")
    guide_text.tag_configure("bold", font="Helvetica 12 bold")

    guide_text.insert("end", "Welcome to the ")
    guide_text.insert("end", "LIGN 167 Quiz Generator\n\n", "bold")
    guide_text.insert("end", "Here's how to get started:\n\n")
    guide_text.insert("end", "1) Select a topic from the dropdown menu\n")
    guide_text.insert("end", "2) Select a difficulty from the dropdown menu\n")
    guide_text.insert("end", "3) Click the ")
    guide_text.insert("end", "Generate Question", "bold")
    guide_text.insert("end", " button to create a new question\n")
    guide_text.insert("end", "4) A question will appear in the ")
    guide_text.insert("end", "Question", "bold")
    guide_text.insert("end", " box\n")
    guide_text.insert("end", "5) Type your answer in the ")
    guide_text.insert("end", "Answer", "bold")
    guide_text.insert("end", " box on the right\n")
    guide_text.insert("end", "6) Click the ")
    guide_text.insert("end", "Submit", "bold")
    guide_text.insert("end", " button at the bottom\n")
    guide_text.insert("end", "7) Feedback will be provided in the ")
    guide_text.insert("end", "Feedback", "bold")
    guide_text.insert("end", " box below the ")
    guide_text.insert("end", "Answer", "bold")
    guide_text.insert("end", " box\n")
    guide_text.insert("end", "8) Repeat!\n\n")
    guide_text.insert("end", "You may also click on the ")
    guide_text.insert("end", "Generate Progress Report", "bold")
    guide_text.insert("end", " button that will generate a progress report \n")
    guide_text.insert("end", "with your overall question accuracy, the topics and difficulties that you've covered, \n")
    guide_text.insert("end", "the topics you did well in and/or didn't do well in, and tips on how to improve!")

    guide_text.configure(state="disabled")
    guide_text.pack(anchor='w')

def get_user_hint_reason():
    dialog = MultiLineInputDialog(root, title="What are you having trouble with?")
    return dialog.result

def provide_hint():
    # Do nothing if no question is active
    if not question_feedback_text.get("1.0", tk.END).strip():
        return
    
    reason = get_user_hint_reason()
    if reason:
        reason = reason.strip()
        response = qg.provide_hint(reason)

        # Unhide hint section and show the hint response
        hint_label.pack(side=tk.TOP, padx=10, pady=10)
        hint_text.config(state=tk.NORMAL, font="Helvetica 10")
        hint_text.insert(tk.END, response)
        hint_text.insert(tk.END, "\n\n")
        hint_text.pack(side=tk.TOP, padx=200, pady=10)
        hint_text.config(bg = "#FFFFFF")
        hint_text.config(state=tk.DISABLED)

qg = QuizGenerator()

# Data Structures
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
            "Encoder-Decoder Architectures"
]


difficulty_list =  ['Easy', 'Medium', 'Hard']

# Create the main window
root = tk.Tk()
root.title("Quiz Generator")

# Set the size of the window
root.geometry("1600x1000")

# Set fonts and colors
label_font = "Helvetica 12"
text_font = "Helvetica 10"
bg_color = "light blue"

# Create frames for layout
top_frame = tk.Frame(root, background=bg_color)
top_frame.pack(side=tk.TOP, fill=tk.X)

bottom_frame = tk.Frame(root, background=bg_color)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

right_frame = tk.Frame(root, background=bg_color)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

left_frame = tk.Frame(root, background=bg_color)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Create and place the topic selection widgets
topic_label = tk.Label(top_frame, text="Select Topic:", font=label_font, background=bg_color)
topic_label.pack(side=tk.TOP, padx=5, pady=5)

topic_combobox = ttk.Combobox(top_frame, values=topics_list, state="readonly", width=45, font=label_font)
topic_combobox.current(0)
topic_combobox.pack(side=tk.TOP, padx=5, pady=5)


# Create and place the difficulty selection widgets
difficulty_label = tk.Label(top_frame, text="Select Difficulty:", font=label_font, background=bg_color)
difficulty_label.pack(side=tk.TOP, padx=5, pady=5)

difficulty_combobox = ttk.Combobox(top_frame, values=difficulty_list, state="readonly", font=label_font)
difficulty_combobox.current(0)
difficulty_combobox.pack(side=tk.TOP, padx=5, pady=5)


# Create and place the generate question button
generate_button = tk.Button(top_frame, text="Generate Question", command=generate_question, font=label_font)
generate_button.pack(side=tk.TOP, padx=5, pady=5)


# Create and place the question and feedback text area
question_feedback_label = tk.Label(left_frame, text="Question:", font=label_font, background=bg_color)
question_feedback_label.pack(side=tk.TOP, padx=10, pady=10)

question_feedback_text = tk.Text(left_frame, height=15, width=60, wrap='word', state='disabled', font=text_font)
question_feedback_text.pack(side=tk.TOP, padx=200, pady=10)


# Create and place the user answer text area
user_answer_label = tk.Label(right_frame, text="Your Answer:", font=label_font, background=bg_color)
user_answer_label.pack(side=tk.TOP, padx=10, pady=10)

user_answer_text = tk.Text(right_frame, height=15, width=60, font=text_font)
user_answer_text.pack(side=tk.TOP, padx=200, pady=10)


# Create and place the feedback text area
user_feedback_label = tk.Label(right_frame, text="Feedback:", font=label_font, background=bg_color)
user_feedback_label.pack(side=tk.TOP, padx=10, pady=10)

user_feedback_text = tk.Text(right_frame, height=15, width=60, wrap='word', state='disabled', font=text_font)
user_feedback_text.pack(side=tk.TOP, padx=10, pady=10)


# Create and place the hint text area
hint_label = tk.Label(left_frame, text="Hint:", font=label_font, background=bg_color)
hint_text = tk.Text(left_frame, height=15, width=60, wrap='word', state='disabled')

# Create and place the submit button
submit_button = tk.Button(bottom_frame, text="Submit", height=2, width=8, command=generate_feedback, font=label_font)
submit_button.pack(side=tk.TOP, padx=10, pady=10)

# Create and place the hint button
hint_button = tk.Button(bottom_frame, text="Hint", width=4, command=provide_hint, font=label_font)
hint_button.pack(side=tk.TOP, padx=10, pady=5)

# Create and place the generate progress report button
progress_report_button = tk.Button(bottom_frame, text="Generate \nProgress Report", height=2, width=15, command=generate_progress_report, font=label_font)
progress_report_button.pack(side=tk.TOP, padx=10, pady=10)


# Add Help button
help_button = tk.Button(top_frame, text="Help", command=open_help, font=label_font)
help_button.pack(side=tk.TOP, padx=5, pady=5)

# Run the application
root.mainloop()
