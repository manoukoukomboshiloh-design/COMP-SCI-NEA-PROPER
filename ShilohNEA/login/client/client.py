
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
	print("\n~~~~ DASHBOARD ~~~~") #curly thing for fancy for nice layout
	print(f"Hey there: {username}! (Your ID is : {user_id})") #Displays the username and user ID at the top of the dashboard for a personalized touch
	print(f"You have taken: {get_total_quizzes(user_id)} quizzes, SHEESH!")
	print(f"This is your best score: {get_best_score(user_id)}")
	print("\nAnd here are your average scores per topic g:")
	for topic, avg in get_topic_averages(user_id):
		print(f"- {topic}: {avg:.2f}")
		#Loops through list of (topic,average) pairs and displays all scores with respective topic for the user
	print("~~~~~~~~~~~~~~~~~~~~~\n")


def main():                    #Connecting our client to the server now
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(("localhost", 9999))
		logging.info('Connected to server at localhost:9999')
		#got a TCP 	socket with IPv4 addressing for client side with the connection to a server at port 9999, then confirming to the user that the connection has been made
	except Exception as e:             #debugging catching any errors on connection
		logging.error(f'Failed to connect to server: {e}')    #error message kept for later debugging
		print("Could not connect to server. See client_debug.log for details.")
		return  #ends program

	try:
		message = client.recv(1024).decode()
		username = input(message) #this is the user entering a username
		client.send(username.encode())
		logging.debug(f'Username entered: {username}') # keeps username entered for debugging later on if a problem occurs
		message = client.recv(1024).decode()
		password = input(message)
		client.send(password.encode())
		logging.debug('Password sent to server.')
		login_response = client.recv(1024).decode()
		#sending password to server for validation
		print(login_response)
		logging.info(f'Login response: {login_response}') # either gives valid or invalid details entered
	except Exception as e:
		logging.error(f'Error during login process: {e}')  # again logs
		print("An error occurred during login. See client_debug.log for details.") # will catch any errors during login communication
		return

	if "successful" in login_response.lower():
		# Checks the users inputted username and passoword against the server side user and password
		# This lower part turns all letter to lowercase, making it case insensitive
		user_id = 1
		show_dashboard(user_id, username)       #assign fixed user id and passing it through the displaying dashboard according to id and the username
		selected_topic = display_menu(question_data)
		if selected_topic:
			import threading   #lets part of the program run at the same time
			sys.path.append(QUIZ_DISPLAY_DIR)    #from the python import paths addind a folder and allowing imports from this directory (gonna be used in other parts of the program)
			from auto_timer_with_skip_flag import auto_timer_with_skip_flag   #starts the timer
			display_notes(selected_topic, question_data)
			skip_flag = {'skip': False}
			def ask_skip():
				answer = input("\nDo you want to skip the timer and go straight to the quiz? Please put 'yes' or 'no', nothing else...: ").strip().lower()
				if answer == 'yes':
					skip_flag['skip'] = True      #skips timer if user requests
			t = threading.Thread(target=ask_skip)      #new thread created to run ask skip separately
			t.start()
			auto_timer_with_skip_flag(skip_flag)
			user = User(user_id, username)
			quiz = Quiz(user, question_data)
			quiz.run(selected_topic)
			logging.info('Quiz started for user.')
			#Running the quiz when the skip is true or when the timer expires
			return
	else:
		logging.warning('Login failed for user.')  #logs warning for further debugging
		print("Login failed. Exiting.")

if __name__ == "__main__":
	main()                   # this will make sure main program only runs whne the file is executed directly and not whenm imported as a module
