#!/usr/bin/python3

#   Author: Qumquat
#   Date: May 2020
#   Project: CLI Login interface and admin panel

import time
import sys
import pickle
from termcolor import colored
import commands as c
from getpass import getpass


vu = False
vp = False
tries = 3
loginfo = pickle.load(open('users.p', 'rb'))
nu = False


# Function to register a new user, checks if username is already registered
# If so, returns prompt to login
# If username is not already registered, prompts for password twice and checks if both match
# If not, returns to username prompt
def signup():
	global nu
	global new_user,new_pass1,new_pass2 
	while nu == True:
		new_user = str(input("Please enter the username you would like to register: "))
		
		if new_user in loginfo:
			print(colored("Username has already been registered"+'\n','red'))
			nu = False
			return
		new_pass1 = str(getpass("Please enter the password you would like to use: "))
		new_pass2 = str(getpass("Please re-enter password: "))

		if new_pass1 != new_pass2:
			print(colored("Passwords did not match"+'\n','red'))
			nu = True
		
		else:
			nu = False
			pass

	if nu == False:
		try:
			loginfo.update( {new_user: new_pass1} )
			pickle.dump( loginfo, open('users.p', 'wb'))
			print(colored("User has been registered, you can now login!"+'\n','green'))
		
		except Exception as e:
			print('ERROR'+str(e))

# Function to login, checks username against db
def login():
	global vu
	global user
	user = input('\n'+"Username: ")
	
	if user in loginfo:
		vu = True
		print(colored("Valid User"+'\n','green'))
	
	elif user not in loginfo:
	
		if user == '!signup':
			global nu
			nu = True
			signup()
			pass
	
		else:
			vu = False
			print(colored("Invalid User"+'\n','red'))

# Function to ask whether user would like to login with an existing user or register a new one
def ask_user():
	global nu
	print("Please enter 1 if you would like to log in or enter 2 if you would like to register a new user")
	choice = input("Enter here: ")
	
	if choice == '1':
		login()
	
	elif choice == '2':
		nu = True
		signup()
	
	else:
		print(colored("Invalid option",'red'))
		sys.exit(1)

# Function to ask for password to given user, allows 3 attempts before exiting
def ask_pass():
	global vp
	global tries
	pwd = getpass("Password: ")

	if pwd == loginfo[user]:
		vp = True
		print(colored("Correct Password"+'\n','green'))
		time.sleep(0.5)
	
	elif tries == 1:
		print(colored("Too many failed attempts, exiting...",'red'))
		time.sleep(0.5)
		sys.exit(1)
	
	elif pwd != loginfo[user]:
		tries -= 1
		vp = False
		print(colored("Invalid password, please try again",'yellow',attrs=['underline']))
	
		if tries == 2:
			print(colored("{} attempts remaining".format(tries)+'\n','yellow'))
	
		elif tries == 1:
			print(colored("{} attempts remaining".format(tries)+'\n','red'))

def prompt_welc():
	welcome = r"""\

 __          __  _                          
 \ \        / / | |                         
  \ \  /\  / /__| | ___ ___  _ __ ___   ___ 
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \
    \  /\  /  __/ | (_| (_) | | | | | |  __/
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|
                                            
                                            
	"""
	options = r"""\
Options:
  1- View Changelog (clog)
  2- Add user (add_user <user> <password>)
  3- Delete user (del_user <user>)
  4- List users (list_users)
  5- Whoami (whoami)
  6- Reset DataBase (reset_db)
  7- Ifconfig (ifconfig)
  8- Ping x2 (ping <ip>)
	"""
	print(colored(welcome,'cyan'))
	time.sleep(0.6)
	print(options)


# Command prompt given when successfully logged in
def prompt():
	global user
	cmd = input("$ ")
	if len(cmd) == 0:
		return
	if cmd.split()[0] in c.coms:
		com = cmd.split()[0]
		
		if len(cmd.split()) > 1:
			arg1 = cmd.split()[1]
		
			if len(cmd.split()) > 2:
				arg2 = cmd.split()[2] 
				c.coms[com](arg1,arg2)
		
			else:
				c.coms[com](arg1)
		
		elif len(cmd.split()) == 1:
			c.coms[cmd]()
	
	elif cmd == 'whoami':
		print(user)
	else:
		print("Invalid option")


# Main function to run everything
def main():
	global nu
	ask_user()
	while vu == False:
		login()
		if nu:
			signup()
		if vu:
			pass
	while vp == False:
		ask_pass()
	if vp:
		prompt_welc()
		while vp:
			prompt()

if __name__ == '__main__':
	main()
	