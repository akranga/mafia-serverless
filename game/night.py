import os, sys
# to read dependencies from ./lib direcroty
script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")
import logging, boto3, json, random

# for dynamodb filter queries
from boto3.dynamodb.conditions import Key, Attr

# setup log level to DEBUG
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE'])


def find_by_identity(identity):
  return table.scan(
           FilterExpression=Attr('TrueIdentity').eq(identity) & 
                            Attr('Identity').eq('Uncovered')
          )['Items']


def save(player):
  table.put_item(Item=player)


def handler(event, context): 
  players = find_by_identity('Innocent')
  if len(players) == 0:
    return response( mafia_win_message(), event)

  victim  = random.choice(players)
  victim['Identity'] = 'Killed by mafia'

  save(victim)
  return response( {"Message": [
      "Night, time to sleep",
      "Mafia awakes",
      "Mafia kills {}".format(victim['Name']),
      "Mafia sleeps"
    ]}, event)



def mafia_win_message():
  return {
    "Message": [
      "Game Over!", 
      "All innocent people has been killed by Mafia",
      "Mafia have won this game!"
    ]}


def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, indent=4, cls=DecimalEncoder, separators=(',', ':')) 
        # 'body': json.dumps(body, separators=(',', ':')) 
      }
  return body

