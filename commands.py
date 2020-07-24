import os
import pickle
from termcolor import colored
from getpass import getpass


f = open('adminpass','r')
adminpass = f.read()
f.close()


def prompt_adminpass():
	global adminpass
	print("Please input the administrator password to execute this command",'\n')
	password = getpass("Password: ")
	if password == adminpass:
		print(colored("Correct password"+'\n','green'))
		return True
	else:
		print(colored("Incorrect password"+'\n','red'))
		return False

def clog():
	if prompt_adminpass() == True:
		f = open("changelog.txt",'r')
		changelog = f.read()
		print('\n'+changelog)
		f.close()
	else:
		return

def add_user(user,pwd):
	try:
		loginfo = pickle.load(open('users.p', 'rb'))
		if user not in loginfo:
			loginfo.update( {user: pwd} )
			pickle.dump( loginfo, open('users.p', 'wb'))
			print(colored("Result: ",'cyan'))
			print("User added!")
		else:
			print("Error: User already exists")
	except TypeError as e:
		print(str(e))


def del_user(user):
	try:
		if prompt_adminpass() == True:
			loginfo = pickle.load(open('users.p', 'rb'))
			if user in loginfo:
				loginfo.pop(user)
				pickle.dump( loginfo, open('users.p', 'wb'))
				print(colored("Result: ",'cyan'))
				print('User {} has been removed.'.format(user))
			else:
				print(colored("Error: User does not exist",'red'))
		else:
			return
	except Exception as e:
		print(str(e))

def list_users():
	if prompt_adminpass() == True:
		loginfo = pickle.load(open('users.p', 'rb'))
		print(colored("Result: ",'cyan'))
		for user in loginfo.keys():
			print(user)
	else:
		return

def reset_db():
	if prompt_adminpass() == True:
		loginfo = {'admin': 'admin'}
		pickle.dump(loginfo,open('users.p','wb'))
		print(colored("Result: ",'cyan'))
		print('Database reset!')
	else:
		return

def ifconfig():
	if prompt_adminpass() == True:
		print(colored("Result: ",'cyan'))
		os.system('ifconfig')
	else:
		return

def ping(ip):
	try:
		print(colored("Result: ",'cyan'))
		os.system('ping -c 2 {}'.format(ip))
	except Exception as e:
		print(str(e))

coms = {'clog':clog,'add_user':add_user,'del_user':del_user,'list_users':list_users,'reset_db':reset_db,'ifconfig':ifconfig,'ping':ping}
