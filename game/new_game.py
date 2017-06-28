import os, sys
# to read dependencies from ./lib direcroty
script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")
import logging, boto3, json, random

# setup log level to DEBUG
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE'])

# all player names has been written in the text file
# we read all of them into list so later we can pick random
# to name our Players
with open('names.txt', 'r') as f:
  all_names = f.read().splitlines()


#
# It all starts withe new game
# This is a handler method that creates a new game
# and stores it's state in the database.
# 
# TODO: Bootstrap a DynamoDB (check env vars for lambda)
# Then check game_controller (where logic of Mafia Game encoded)
# and implement a new game
#
def new_game_handler(event, context):
  return response( {"Message": "Welcome to the Serverless Workshop fully powered by AWS Lambda elastic cloud computing service"}, event)


def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, indent=4, separators=(',', ':')) 
      }
  return body

