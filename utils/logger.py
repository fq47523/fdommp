#!/usr/bin/env python
#coding:utf-8
import logging.config,os
pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (pwd)
logging.config.fileConfig("{}/conf/logger.ini".format(pwd))
logger = logging.getLogger("fdommp")


if __name__=='__main__':
    logger.info(msg="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    logger.error(msg="eyJ1c2VybmFtZSI6IndlbGxpYW0iLCJ1c2VyX2lkIjoyLCJlbWFpbCI6IjMwMzM1MDAxOUBxcS5jb20iLCJleHAiOjE1MTk2NTUzNTB9")