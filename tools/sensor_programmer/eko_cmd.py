import cmd
import readline
import rlcompleter
import configmemory


class EkoCmd(cmd.Cmd):
	prompt = "eko_client: "

	def do_connect(self,line):
		"""connect device_id:
		connects to a sensor module with device id 'device_id'"""
		pass
 
	def do_read(self,line):
		if line and len(line.split()) >= 1 :
			args = line.split()
			if len(args) == 1:
				#Read Config
				pass
			elif len(args) == 2:
				#Read from start to start+bytes
				start = args[0]
				rbytes = args[1]
				try:
					print ("Reading %d bytes from address 0x%d"%(int(rbytes),int(start)))
					#Read data into a buffer using Modbus protocol
					#Present the contents in a pretty form

				except ConfigReadError as e:
					print (e)
			else:
				print "Command not recognised. Type in 'help read' for more information."
					
		else:
			print "Please specify the arguments."

	def help_read(self):	
		s = "\nread config | start bytes: \n\n"
		s += "read config: \n\n"
		s += "\treads the configuration of sensor module written in the EEPROM\n\n"
		s += "read start end:\n\n"
		s += "\treads 'bytes' number of bytes from address 0x'start' in the EEPROM\n"
		print s

	def complete_read(self, text, line, begidx, endidx):
		str_cfg = 'config'
		str_addr = '8000'	
		if not text:
			#auto completetions available for config read or data read from address 0x8000 (configuration space)
			completions = ['config', '8000']
		elif text in str_cfg:
			completions = ['config']
		elif text in str_addr:
			completions = ['8000']
		return completions

	def do_exit(self,line):
		return True


if __name__=="__main__":
	#Following changes required for Macs to do auto completion
	if 'libedit' in readline.__doc__:
    		readline.parse_and_bind("bind ^I rl_complete")
	else:
    		readline.parse_and_bind("tab: complete")	
	EkoCmd().cmdloop()
