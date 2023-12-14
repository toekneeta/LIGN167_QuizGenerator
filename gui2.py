import streamlit as st
from backend2 import QuizGenerator

#What happens when you press the Generate Question button
def generate_question_button():
    #Clear answer
    st.session_state["answer_text"] = ""
    #Clear feedback
    st.session_state["feedback_text"] = ""
    # Call the generate_question function and update the question text in session state
    question = qg.generate_question(topic, difficulty)
    st.session_state['question_text'] = question

#What happens when you press the Submit button
def generate_feedback_button():
    # Call the provide_feedback function and update the feedback text in session state
    feedback = qg.provide_feedback(st.session_state['question_text'], answer, topic, difficulty)
    st.session_state['feedback_text'] = feedback

# Initialize the quiz generator
qg = QuizGenerator()

# Layout and widgets
st.title("LIGN 167 Quiz Generator")

#Help info in sidebar
st.sidebar.markdown("Welcome to the LIGN 167 Quiz Generator!\n\n"
        "Here's how to get started:\n\n"
        "1) Select a topic from the dropdown menu\n"
        "2) Select a difficulty from the dropdown menu\n"
        "3) Click the Generate Question button to create a new question\n"
        "4) A question will appear in the Question box\n"
        "5) Type your answer in the Answer box on the right\n"
        "6) Click the Submit button at the bottom\n"
        "7) Feedback will be provided in the Feedback box below the Answer box\n"
        "8) Repeat!\n\n"
        "You may also click on the Generate Progress Report button that will \n"
        "generate a progress report with your overall question accuracy, the topics and difficulties \n"
        "that you've covered, the topics you did well in and/or didn't do well in, \n"
        "and tips on how to improve!")

#Check if 'question_text' is already in the session state 
#If not, initialize it
if 'question_text' not in st.session_state:
    st.session_state['question_text'] = ""

#Check if 'feedback_text' is already in the session state 
#If not, initialize it
if 'feedback_text' not in st.session_state:
    st.session_state['feedback_text'] = ""

#Check if 'answer_text' is already in the session state 
#If not, initialize it
if 'answer_text' not in st.session_state:
    st.session_state['answer_text'] = ""

#Check if 'topic' is already in the session state 
#If not, initialize it
if 'topic' not in st.session_state:
    st.session_state['topic'] = "Attention"

#Check if 'difficulty' is already in the session state 
#If not, initialize it
if 'difficulty' not in st.session_state:
    st.session_state['difficulty'] = "Easy"

# Topic and difficulty selection at top of screen
st.session_state['topic'] = st.selectbox("Select Topic", [
            "Attention",
            "Autoregressive Language Modeling",
            "Autoregressive Models",
            "Backpropagation",
            "Encoder-Decoder Architectures",
            "Linear Regression",
            "Logistic Regression",
            "Masked Language Modeling",
            "Multilayer Perceptrons",
            "Optimization through Gradient Descent",
            "Supervised Learning",
            "Transformers",
            "Word2Vec"])
topic = st.session_state['topic']
st.session_state['difficulty'] = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
difficulty = st.session_state['difficulty']

#Generate question button
if st.button("Generate Question"):
    generate_question_button()

#Make 2 column containers on the page for the question/answer + feedback: 
col1, col2 = st.columns(2)

#Left column: question area
with col1:
    with st.container():
        st.text_area("Question", value=st.session_state['question_text'], disabled=True)
        

#Right column: answer + feedback area
with col2:
    with st.container():
        st.text_area("Enter your answer", value=st.session_state['answer_text'], disabled=False)
        answer = st.session_state["answer_text"]
        st.text_area("Feedback", value=st.session_state['feedback_text'], disabled=True)
        feedback = st.session_state["feedback_text"]

#Submit button
if st.button("Submit"):
    generate_feedback_button()
    

#Hint button
        

#Progress Report Button


