#!/usr/bin/python
# -*- encoding: utf-8 -*-

import logging
import logger

# create logger
module_logger = logging.getLogger('v1188ys.importer')
#logger = logging.getLogger('spam_app')
logger = logger.getLogger()

class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger('v1188ys.image')
        self.logger.info('creating an instance of Auxiliary')
    def do_something(self):
        self.logger.info('doing something')
        a = 1 + 1
        self.logger.info('done doing something')

def some_function():
    module_logger.info('received a call to "some_function"')


logger.info('creating an instance of auxiliary_module.Auxiliary')
a = Auxiliary()
a.do_something()
some_function()
logger.info('done with auxiliary_module.some_function()')


# import某个文件，该文件中的变量不能访问，但是该文件确实被执行了，所以logger中关于logger的配置在当前文件中生效
#此外，logging.getLogger('spam_app.auxiliary') 这里logger的名字也很关键，logger文件中定义了spam_app，这里spam_app.auxiliary继承了spam_app的配置。
#如果改了名字，例如改为spam_appxx.auxiliary就会去使用默认配置，估计是stdout输出。