# ServerConf
# 2017-11-01 K.OHWADA

'''  ServerConf
handling setting flie of server
'''

import os
import json


# class ServerConf
class ServerConf():
 	DIR_NAME = "conf";
 	FILE_NAME = "user.conf";

# readConf 	
 	def readConf(self, user, appname):
 		basedir = self.getBasedir( user,appname )
		# print basedir
		path = self.getConfigPath( basedir )
		# print path
		obj = self.readConfFile( path )
		return obj
	# ---
	 		
# readConfFile
	def readConfFile(self, path):        
    		if os.path.exists(path):
    			f = open(path)
			obj = json.load(f)
			f.close()
        		return obj
		return None
# ---

# getBasedir
	def getBasedir(self, user, appname ):
			home = "/home/" + user
			# home = "~";
			basedir = os.path.expanduser(os.path.join( home, "." + appname.lower()))
			return basedir
# ---

# getConfigPath
	def getConfigPath(self, basedir):
		path = self.getBasePath( basedir, self.DIR_NAME,  self.FILE_NAME )
		return path
# ---

# getBasePath
	def getBasePath(self, basedir, subdir, name):
		dir = os.path.join( basedir, subdir )
 		return os.path.join( dir, name )
# ---

# class end
