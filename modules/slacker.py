from slack import WebClient
import logging


class NoSlackForYou(Exception):
	"""Handling slack error messages"""
	def __init__(self,messages):
		print(messages)
		

class SlackClient(object):
	"""Create a slack object for posting messages"""

	#Place your token here
	token = ''
	client = None

	def __init__(self):

		if self.token != None or self.token != '':
			try:
				client = WebClient(token=self.token)
				self.client = client
			except:
				NoSlackForYou("[-] Error occured while connecting to slack API")


	def sendMessage(self,message, channel='general'):

		if self.client==None:
			NoSlackForYou("Cannot connect to slack API")

		if message =='':
			NoSlackForYou("[-] Cannot send a empty message to slack channel")
		
		if self.client != None and message != '' and self.token !='':
			try:	
				res = self.client.chat_postMessage(
					channel=channel,
					text=message,
					as_user=True)
				
				assert res ["ok"]
			except:
				print("[-] Slack Error while posting message with provided API token")
