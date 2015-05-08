import logging
from logging.handlers import TimedRotatingFileHandler

# create logger with 'spam_application'
logger = logging.getLogger('v1188ys')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
filepath = '/tmp/spam.log'
fh = TimedRotatingFileHandler(filepath, when="d", interval=7, backupCount=4)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
#ch = logging.StreamHandler()
#ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
#ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
#logger.addHandler(ch)

# logger.info('creating an instance of auxiliary_module.Auxiliary')
# a = app_module.Auxiliary()
# a.do_something()
# app_module.some_function()
# logger.info('done with auxiliary_module.some_function()')

def getLogger():
    return logger
