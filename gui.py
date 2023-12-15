import streamlit as st
import os
from backend import QuizGenerator
import pandas as pd


def main():
    qg = QuizGenerator()

    st.title("LIGN 167 Quiz Generator")

    difficulty_list = ["Easy", "Medium", "Hard"]


    # counter for number of questions answered for each topic and difficulty
    if 'answered_counter' not in st.session_state:
        st.session_state['answered_counter'] = {topic: {difficulty: 0 for difficulty in difficulty_list} for topic in qg.topics_list}
    if 'answered' not in st.session_state:
        st.session_state['answered'] = 0

    # counter for number of questions correct for each topic and difficulty
    if 'correct_counter' not in st.session_state:
        st.session_state['correct_counter'] = {topic: {difficulty: 0 for difficulty in difficulty_list} for topic in qg.topics_list}
    if 'correct' not in st.session_state:
        st.session_state['correct'] = 0

    if 'question_history' not in st.session_state:
        st.session_state['question_history'] = {topic: [] for topic in qg.topics_list}

    if 'question' not in st.session_state:
        st.session_state['question'] = ""

    if "feedback" not in st.session_state:
        st.session_state['feedback'] = ""

    if "hint" not in st.session_state:
        st.session_state['hint'] = ""

    if "hint_active" not in st.session_state:
        st.session_state['hint_active'] = False

    if "hint_response" not in st.session_state:
        st.session_state['hint_response'] = ""

    if "submit_hint_req" not in st.session_state:
        st.session_state['submit_hint_req'] = False

    # all past dialog for current question
    message_history = []

    # Help sidebar

    st.sidebar.markdown("""
        Welcome to the **LIGN 167 Quiz Generator**

        Here's how to get started:

        1) Select a topic from the dropdown menu
        2) Select a difficulty from the dropdown menu
        3) Click the **Generate Question** button to create a new question
        4) A question will appear in the **Question** box
        5) Type your answer in the **Answer** box on the right
        6) If you don't know the answer, you can click the **New Hint Request** button, 
           which will generate a hint for the current question. You can request as many hints as you want.
        7) Click the **Submit** button at the bottom
        8) Feedback will be provided in the **Feedback** box below the **Answer** box
        9) Repeat!

        You may also click on the **Generate Progress Report** button that will generate a progress report with your overall question accuracy, the topics and difficulties that you've covered, the topics you could refresh on, and tips on how to improve!
    """)

    # Dropdown for topic selection
    topic = st.selectbox("Select a topic:", qg.topics_list)

    # Dropdown for difficulty selection
    difficulty = st.selectbox("Select difficulty:", difficulty_list)

    # Button to generate a question
    if st.button("Generate Question"):
        question, message_history = qg.generate_question(topic, difficulty, st.session_state['question_history'][topic])
        st.session_state['question'] = question
        st.session_state['question_history'][topic].append(question)
        st.session_state['message_history'] = message_history
        st.session_state['hint'] = ""
        st.session_state['hint_active'] = False
        st.session_state['feedback'] = ""
    
    st.text_area("Question", value=st.session_state['question'], disabled=True)

    # Text area for answer input
    st.session_state['Answer'] = st.text_area("Your Answer:")

    # Button to submit an answer
    if st.button("Submit Answer"):
        if 'question' in st.session_state:
            answer = st.session_state['Answer']
            st.session_state['feedback'], correct, message_history = qg.provide_feedback(st.session_state['question'], answer, topic, difficulty, st.session_state['message_history'])
            st.session_state['message_history'] = message_history
            if correct:
                st.session_state['correct'] += 1
                st.session_state['correct_counter'][topic][difficulty] += 1
            st.session_state['answered'] += 1
            st.session_state['answered_counter'][topic][difficulty] += 1
        else:
            st.warning("Please generate a question first.")

    st.text_area("Feedback", value=st.session_state['feedback'], disabled=True)

    #Hint button
    if st.button("New Hint Request"):
        if st.session_state['question']:
            st.session_state['hint_response'] = st.text_input("What are you struggling with?")
            st.session_state['submit_hint_req'] = True
        else:
            st.warning("Plese generate a question first.")
    
    if st.button("Submit Hint Request", disabled=not st.session_state['submit_hint_req']):
        st.session_state['hint'] += qg.provide_hint(st.session_state['hint_response'], st.session_state['message_history']) + "\n\n"
        st.session_state['submit_hint_req'] = False
        st.session_state['hint_active'] = True
        st.experimental_rerun()

    if st.session_state['hint_active']:
        st.text_area("Hint", value=st.session_state['hint'], disabled=True)

    # Generate Progress Report button
    if st.button("Generate Progress Report"):
        # Logic to generate and display progress report
        overall_accuracy_rate, progress_report_stats, struggled_topics, study_tips = qg.create_progress_report(st.session_state['answered_counter'], st.session_state['correct_counter'], st.session_state['answered'], st.session_state['correct'])

       

        columns = ['Topics', '# of Easy Questions Answered', '# of Medium Questions Answered', '# of Hard Questions Answered', \
                   'Easy Accuracy Rate', 'Medium Accuracy Rate', 'Hard Accuracy Rate', 'Topic Accuracy Rate']

        data = []
        for topic_stats in progress_report_stats:
            # Replace -1 with empty string for display purposes
            topic_data = ["" if stat == -1 else stat for stat in topic_stats]
            data.append(topic_data)

        df = pd.DataFrame(data, columns=columns).set_index('Topics')
        st.table(df)

        # Display overall accuracy rate
        overall_accuracy_display = "" if overall_accuracy_rate == -1 else f"{overall_accuracy_rate:.2f}%"
        st.write(f"**Overall Accuracy Rate**: {overall_accuracy_display}")

        # Display topics to improve on
        if struggled_topics:
            st.write("**Topics to Improve On**:", ', '.join(struggled_topics))

            st.write("**Study Tips**:")
            st.write(study_tips)
            

            
if __name__ == "__main__":
    main()
