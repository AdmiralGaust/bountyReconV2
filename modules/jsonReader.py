import json
import logging
from modules import pylogger


logger = logging.getLogger('pylogger')

class ReadError(Exception):
	"""docstring for ReadError"""
	def __init__(self, message):
		logger.info(message)		


class read(object):
	"""docstring for read"""

	data = None

	def __init__(self, filename):

		if filename==None or filename=='':
			ReadError("[-] Please provide a filename to read from")
		else:
			try:
				fileContent = open(filename,'r').read()
				self.data = json.loads(fileContent)
			except Exception as e:
				print(str(e))
				#ReadError("[-] Error Reading json file " + filename)

	def get(self,key):

		if self.data!=None:
			if self.data.get(key)!=None:
				return self.data.get(key)

		return None
