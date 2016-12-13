import os, sys

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")

import logging, boto3, uuid, json

import game_controller

log = logging.getLogger()
log.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['dynamo_table'])


def flush_old_game():
  resp = table.scan() 
  for i in resp['Items']:
    table.delete_item(Key={'GameId': i['GameId']})


def save_game(current_state):
  table.put_item(Item=current_state)


def load_game():
  resp = table.scan(Limit=1)
  if resp['Count'] > 0:
    return resp['Items'][0]

  return {
    'GameId':     'game not started',
    'Players':    [],
    'LastAction': 'game not started', 
    'Result':     'game not started'
  }


def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, separators=(',', ':')) 
      }
  return body

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

#
# This AWS lambda handler method returns state of the game.
# It will also show if the game has been finished or not
#
def game_state_handler(event, context):
  return response( {"Message": "Welcome to the Serverless Workshop fully powered by AWS Lambda elastic cloud computing service"}, event)

#
# This function method handles a night event when Mafia chooses an innocent victim and iills it
# Then it iwll record state in the databaseb
#
def night_handler(event, context):
  return response( {"Message": "Welcome to the Serverless Workshop fully powered by AWS Lambda elastic cloud computing service"}, event)

#
# This function wil tell you about players accusition process
# where they accusing each other of murders. Please note Mafia
# knows their identities and never accuses their brother
# 
# Result is not stored in the database. Instead uses gets whole
# chain of accusitions and must choice person to judge
#
def day_handler(event, context):
  return response( {"Message": "Welcome to the Serverless Workshop fully powered by AWS Lambda elastic cloud computing service"}, event)

#
# In this function User sends event with suspected person name. It 
# must come in the form of GET variable in the event
#
def judgement_handler(event, context):
  return response( {"Message": "Welcome to the Serverless Workshop fully powered by AWS Lambda elastic cloud computing service"}, event)

