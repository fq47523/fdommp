from os import getenv
from sys import exit

if getenv('FDOMMP_RUN_ENV') == 'DEV':
    from .dev import *
elif getenv('FDOMMP_RUN_ENV') == 'PROD':
    from .prod import *
else:
    print ('没有设置系统运行环境变量')
    exit(1)