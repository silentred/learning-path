import logging
from logging.handlers import TimedRotatingFileHandler

# create logger with 'spam_application'
logger = logging.getLogger('1188meishi')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
filepath = '/tmp/meishi1188.log'
fh = TimedRotatingFileHandler(filepath, when="d", interval=1, backupCount=4)
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)


# create console handler with a higher log level
# FOR TEST
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)
logger.addHandler(ch)

# logger.info('creating an instance of auxiliary_module.Auxiliary')
# a = app_module.Auxiliary()
# a.do_something()
# app_module.some_function()
# logger.info('done with auxiliary_module.some_function()')

def getLogger():
    return logger
