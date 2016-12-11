import os, sys

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")

import logging, random, uuid

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
  return {"Message": "Welcome to the Serverless Workshop fully powered by AWS Lambda elastic cloud computing service"}
