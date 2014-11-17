import subprocess
import os,sys,shlex

class Command():

    #def __init__(self,commandLine=None):
	#self.commandlline=commandLine

 

    def Process_Command(self,argumentsList, concatenator, information_msg = None):
	output = ""; errors = ""
  	try:
		print information_msg
		commandLine =concatenator.join(argumentsList)
		p = subprocess.Popen(shlex.split(commandLine), stdout=subprocess.PIPE)
		output, errors = p.communicate()
		
		if errors:
			raise Exception('Something went wrong while running, error is: %s , Output is: %s ' % (errors,output))
			
  	except:
        	raise Exception('The command failed to run in directory %s  : error is: %s , Output is: %s , command: %s' % (os.getcwd(),errors,output,commandLine))


    def Get_program_path(self,executable):
  	binpath = os.path.dirname(os.path.abspath(sys.argv[0]))
  	#print binpath
	path = os.path.join(binpath, executable)
	
    	if path and os.path.exists(path):
      		return path
    	p = subprocess.Popen("which %s 2>/dev/null" % (executable), shell=True, stdout=subprocess.PIPE)
    	path, errors = p.communicate()
    	path = path.strip()
	#print path
   	if path and os.path.exists(path):
     	 	return path
        		
      
