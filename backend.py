from openai import OpenAI


class QuizGenerator:
	def __init__(self):
		self.model =  "gpt-4-1106-preview" # "gpt-3.5-turbo-1106"
		self.client = OpenAI()

		self.topics_list = [
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
            "Word2Vec"
    	]

		self.difficulty_list =  ['Easy', 'Medium', 'Hard']



	def get_chatgpt_response(self, messages):
		response = self.client.chat.completions.create(
		    model=self.model,
		    messages=messages
	    )
		return response.choices[0].message.content

	def generate_question(self, topic, difficulty, question_history):
		generate_question_sys_text = "Your role is to generate quiz questions for a class on \
	                              deep learning for natural language understanding. \
	                              I will provide you a topic from the course and a difficulty \
	                              level (easy, medium, or hard) to guide what kind of question \
	                              I want you to generate. Questions can be short-answer, fill-in-the-blank, \
	                              or multiple choice. \
	                              Your questions should, however, consider \
	                              adaptive difficulty, meaning that if an user is getting too many \
	                              questions wrong, you should make questions easier, while if they are \
	                              getting a lot of questions right, you should make questions harder. \
	                              After you have generated a question for the user, the user will provide \
	                              you with their answer to the question. You will give the user feedback to \
	                              their answer to the question."

		generate_question_user_text = "Generate a " + difficulty + " question in the topic of " + topic + \
	    							  ". Only provide the question in less than 50 words."

	    # if there has been questions for this topic previously, don't repeat them
		if question_history:
			generate_question_user_text += " Do not use any variants of the following questions: "

			for question in question_history:
			    generate_question_user_text += question + " "
		
		# Restart message history
		self.message_history = [
		        {'role': 'system', "content": generate_question_sys_text},
		        {'role': 'user', "content": generate_question_user_text}
	    ]

	    # generate the question
		question = self.get_chatgpt_response(self.message_history)
		
		# add question to message history
		self.message_history.append({
			'role': 'assistant',
			'content': question
		})

		return question, self.message_history

	def provide_feedback(self, question, answer, topic, difficulty, message_history):
		generate_feedback_sys_text = "Your role is to provide feedback for the user \
	                              on their answer to a question. You will \
	                              then start your response either with the word \
	                              correct or incorrect depending on if the user \
	                              got the question right or wrong. Then, you will \
	                              give an explanation in less than 50 words why they \
	                              got the question right or wrong."
		message_history.append({
			'role': 'user',
			'content': answer
		})
		message_history.append({
			'role': 'system',
			'content': generate_feedback_sys_text
		})

		response = self.get_chatgpt_response(message_history)
		
		# if answer is correct, correct=True
		correct=False
		if response.split()[0].lower().strip('.,!') == "correct":
			correct=True

		# add response to message history
		message_history.append({
			'role': 'assistant',
			'content': response
		})

		return response, correct, message_history

	def get_progress_report_stats(self, answered_counter, correct_counter, answered, correct):
		progress_report_stats = []
		for topic in self.topics_list:
			num_easy_answered = answered_counter[topic]['Easy']
			num_medium_answered = answered_counter[topic]['Medium']
			num_hard_answered = answered_counter[topic]['Hard']

			num_easy_correct = correct_counter[topic]['Easy']
			num_medium_correct = correct_counter[topic]['Medium']
			num_hard_correct = correct_counter[topic]['Hard']

			# percentage of each difficulty of question for that topic answered correctly
			if num_easy_answered > 0:
				easy_accuracy_rate = round((num_easy_correct / num_easy_answered) * 100, 2)
			else:
				easy_accuracy_rate = -1

			if num_medium_answered > 0:
				medium_accuracy_rate = round((num_medium_correct / num_medium_answered) * 100, 2)
			else:
				medium_accuracy_rate = -1

			if num_hard_answered > 0:
				hard_accuracy_rate = round((num_hard_correct / num_hard_answered) * 100, 2)
			else:
				hard_accuracy_rate = -1

			# overall percentage of correctly answered questions for that topic
			if num_easy_answered + num_medium_answered + num_hard_answered > 0:
				topic_accuracy_rate = round(((num_easy_correct + num_medium_correct + num_hard_correct) / \
									 (num_easy_answered + num_medium_answered + num_hard_answered)) * 100, 2)
			else:
				topic_accuracy_rate = -1

			progress_report_stats.append([topic, num_easy_answered, num_medium_answered, num_hard_answered, \
										  easy_accuracy_rate, medium_accuracy_rate, hard_accuracy_rate, topic_accuracy_rate])
				

		if answered > 0:
			overall_accuracy_rate = round((correct / answered) * 100, 2)
		else:
			overall_accuracy_rate = -1

		return overall_accuracy_rate, progress_report_stats

	def create_progress_report(self, answered_counter, correct_counter, answered, correct):
	
		overall_accuracy_rate, progress_report_stats = self.get_progress_report_stats(answered_counter, correct_counter, answered, correct)

		# user is considered to struggle if topic accuracy rate is less than 70%
		struggled_topics = []
		for topic_stats in progress_report_stats:
			# if user didn't answer question for topic, continue
			topic = topic_stats[0]
			topic_accuracy_rate = topic_stats[-1]
			if topic_accuracy_rate == -1:
				continue
			elif topic_accuracy_rate < 70:
				struggled_topics.append((topic, topic_accuracy_rate))

		# sort struggled topics by accuracy, from least to greatest
		sorted_struggled_topics = [pair[0] for pair in sorted(struggled_topics, key=lambda x:x[1])]

		generate_study_tips_sys_text = "Your role is to provide study tips for the user. \
		                                The user will give a list of topics they are struggling \
		                                with, and your job is to give them advice on how to study \
		                                for those topics. Keep your response to 50 words maximum \
		                                for each topic."

		generate_study_tips_user_text = "The following is a list of topics I am struggling with: " + \
		                                ', '.join(sorted_struggled_topics) + ". Please provide " + \
		                                "study tips for each topic."

		study_tips = self.get_chatgpt_response([
		        {'role': 'system', "content": generate_study_tips_sys_text},
		        {'role': 'user', "content": generate_study_tips_user_text}
		])

		return [overall_accuracy_rate, progress_report_stats, sorted_struggled_topics, study_tips]
	
	def provide_hint(self, reason, message_history):
		generate_hint_sys_text = "Your role is to provide a brief hint for the user, \
								  based on the reason they are stuck,\
				  				  to help them answer the question."
		message_history.append({
			'role': 'user',
			'content': reason
		})
		message_history.append({
			'role': 'system',
			'content': generate_hint_sys_text
		})

		hint = self.get_chatgpt_response(message_history)

		message_history.append({
			'role': 'assistant',
			'content': hint
		})

		return hint
