#pylogger usage example
import logging
from modules import pylogger
logger = logging.getLogger('pylogger')

logfilename = 'target.txt'	#Log to file instead
logger.addHandler(logging.FileHandler(logfilename))
logger.info('logging is now fine')


#Slacker usage example
from modules import slacker
a = slacker.SlackClient()   #configure slack api token in core/config.json file
a.sendMessage('slacker done',channel="general")


#jsonReader usage example
from modules import jsonReader
content = jsonReader.read('./core/config.json')  #file to read
content.get("Slack_token")  #get specific key value

#processor usage example
from modules import processor

target = "example"
filename="domains.txt"

p = processor.processor()

p.targetname = target
p.filename = filename

p = processor.processor()
p.configure(run="subdomains")
p.process()
