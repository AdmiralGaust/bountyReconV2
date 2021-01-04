#!/usr/bin/python3
import logging

logging.basicConfig(
		level = logging.INFO, 
		format='%(asctime)s : %(message)s',
		datefmt='%d/%m/%Y %H:%M')

logger = logging.getLogger('pylogger')