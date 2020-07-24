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
