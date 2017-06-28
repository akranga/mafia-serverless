import os, sys

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")

import logging, boto3, uuid, json, random
from boto3.dynamodb.conditions import Key, Attr

import game_controller

log = logging.getLogger()
log.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE'])


def save(player):
  table.put_item(Item=player)


def clear_all():
  for i in find_all():
    table.delete_item(Key={'Name': i['Name']})


def find_all():
  return table.scan(IndexName='Masked')['Items']


def find_all_uncovered():
  return table.scan(
           FilterExpression=Attr('Identity').eq('Uncovered')
          )['Items']

def find_by_identity(identity):
  return table.scan(
           FilterExpression=Attr('TrueIdentity').eq(identity) & 
                            Attr('Identity').eq('Uncovered')
          )['Items']

def find_by_name(name):
  return table.scan(
           FilterExpression=Attr('Identity').eq('Uncovered') &
                            Attr('Person').eq(name)
          )['Items']


def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, indent=4, cls=DecimalEncoder, separators=(',', ':')) 
        # 'body': json.dumps(body, separators=(',', ':')) 
      }
  return body


def new_game_handler(event, context):
  num_of_players = int(os.environ['NUMBER_OF_PLAYERS'])
  num_of_mafia   = int(os.environ['NUMBER_OF_MAFIA'])
  players = game_controller.new_game(num_of_players, num_of_mafia)
  
  clear_all()
  for player in players:
    save(player)
  names = [ p['Name'] for p in players ]
  message = "New game started with {}".format(', '.join(names))
  return response( {"message": message}, event )


def game_state_handler(event, context): 
  return find_all()


def night_handler(event, context):
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


def day_handler(event, context):
  message = [
    "Day, time to wake up!",
    "Players see the dead body and makes their accusations"
  ]

  innocent = find_by_identity('Innocent')
  anybody  = find_all_uncovered()

  for p in anybody:
    if p['TrueIdentity'] == 'Mafia':
      accused = random.choice(innocent)
    else:
      accused = random.choice(anybody)
    message.append("{} blames on {}".format(p['Name'], accused['Name']))

  message.append("Who is the Mafia?")
  return response({"Message": message}, event)


def judgement_handler(event, context):
  log.debug(json.dumps(event, separators=(',', ':')))

  name      = event['queryStringParameters']['Name']
  sentenced = find_by_name(name)

  if sentenced['TrueIdentity'] == 'Mafia':
    sentenced['Identity'] = 'Correctly sentenced'
    message = [
        'Mafia has been uncovered!'
        'Guilty member of mafia {} has been sentenced!'.format(sentenced['Name'])
      ]
  else:
    sentenced['Identity'] = 'Correctly sentenced'
    message = [
        'Mafia has not been uncovered!'
        'Innocent {} has been sentenced unfairly'.format(sentenced['Name'])
      ]
  
  save(sentenced)
  return response({"Message": message}, event)


def mafia_win_message():
  return {
    "Message": [
      "Game Over!", 
      "All innocent people has been killed by Mafia",
      "Mafia have won this game!"
    ]}

