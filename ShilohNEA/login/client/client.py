
import socket
import sys
import os
import logging

# Need sys for python runtime interaction, these 3 libraries are the basis of networking and file management
# Debugging/logging setup for NEA evidence
logging.basicConfig(
	filename='client_debug.log',
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s:%(message)s'
)
logging.debug('Client started and logging initialized.')


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
PROGRESS_DIR = os.path.join(BASE_DIR, 'progress')
QUIZ_DISPLAY_DIR = os.path.join(BASE_DIR, 'quiz', 'display')
QUIZ_GETQUIZ_DIR = os.path.join(BASE_DIR, 'quiz', 'getquiz')

#Sets up my directory paths for the various modules, and adds them to sys.path if not already present, allowing for imports from those directories.
#This is absically like the roots of my revision guide tree, and allows me to keep my code organized in different folders without import issues.


if PROGRESS_DIR not in sys.path:
	sys.path.insert(0, PROGRESS_DIR)
if QUIZ_DISPLAY_DIR not in sys.path:
	sys.path.insert(0, QUIZ_DISPLAY_DIR)
if QUIZ_GETQUIZ_DIR not in sys.path:
	sys.path.insert(0, QUIZ_GETQUIZ_DIR)

#Ts makes the whole program look nice ye with custom folders that python can import from


from dashboard import get_topic_averages, get_total_quizzes, get_best_score
from quizdisplay import display_menu, display_notes
from question_bank import question_data
from getquestions import Quiz, User

#Taking the functions and classes from my other folders so I can set up the dashboard, all thats missing is a leaderboard of all my users ordering them on how many questions they ahave answered INSTEAD of how many right as effort shall be rewarded (ts for later)
#OOP 
#data abstraction 
#use of modules 

def show_dashboard(user_id, username):
	print("\n~~~~ DASHBOARD ~~~~") #equals sign for nice layout
	print(f"User: {username} (ID: {user_id})") #Displays the username and user ID at the top of the dashboard for a personalized touch
	print(f"Total quizzes taken: {get_total_quizzes(user_id)}")
	print(f"Best score: {get_best_score(user_id)}")
	print("\nAverage scores by topic:")
	for topic, avg in get_topic_averages(user_id):
		print(f"- {topic}: {avg:.2f}")
		#Loops through list of (topic,average) pairs and displays them for the user
	print("~~~~~~~~~~~~~~~~~~~~~\n")


def main():
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(("localhost", 9999))
		logging.info('Connected to server at localhost:9999')
	except Exception as e:
		logging.error(f'Failed to connect to server: {e}')
		print("Could not connect to server. See client_debug.log for details.")
		return

	try:
		message = client.recv(1024).decode()
		username = input(message)
		client.send(username.encode())
		logging.debug(f'Username entered: {username}')
		message = client.recv(1024).decode()
		password = input(message)
		client.send(password.encode())
		logging.debug('Password sent to server.')
		login_response = client.recv(1024).decode()
		print(login_response)
		logging.info(f'Login response: {login_response}')
	except Exception as e:
		logging.error(f'Error during login process: {e}')
		print("An error occurred during login. See client_debug.log for details.")
		return

	if "successful" in login_response.lower():
		# This lower part makes the login check case sensitive.
		user_id = 1
		show_dashboard(user_id, username)
		# Topic selection and quiz
		selected_topic = display_menu(question_data)
		if selected_topic:
			import threading
			sys.path.append(QUIZ_DISPLAY_DIR)
			from auto_timer_with_skip_flag import auto_timer_with_skip_flag
			display_notes(selected_topic, question_data)
			skip_flag = {'skip': False}
			def ask_skip():
				answer = input("\nDo you want to skip the timer and go straight to the quiz? Please put 'yes' or 'no': ").strip().lower()
				if answer == 'yes':
					skip_flag['skip'] = True
			t = threading.Thread(target=ask_skip)
			t.start()
			auto_timer_with_skip_flag(skip_flag)
			user = User(user_id, username)
			quiz = Quiz(user, question_data)
			quiz.run(selected_topic)
			logging.info('Quiz started for user.')
			return
	else:
		logging.warning('Login failed for user.')
		print("Login failed. Exiting.")

if __name__ == "__main__":
	main()