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


def new_game_handler(event, context):
  game = {
    'GameId':     str(uuid.uuid1()),
    'Players':    game_controller.new_game(),
    'LastAction': 'new', 
    'Result':     'unknown'
  }
  flush_old_game()
  save_game(game)
  names = [ player['Name'] for player in game['Players'] ]
  message = "New game started with {}".format(', '.join(names))
  return response( {"message": message}, event)


def game_state_handler(event, context):
  game = load_game()
  players = game['Players']
  game_controller.hide_uncovered_identities( players )
  return response(game, event)


def night_handler(event, context):
  game = load_game()
  players = game['Players']

  victim = game_controller.victim_of_mafia(players)

  players[victim]['Identity'] = 'killed'
  game['LastAction']          = 'night murder'

  save_game(game)
  return response( {"Message": [
      "Night, time to sleep",
      "Mafia awaken",
      "Mafia kills {}".format(players[victim]['Name']),
      "Mafia sleeps"
    ]}, event)


def day_handler(event, context):
  game = load_game()
  players = game['Players']
  accusitions = game_controller.get_players_accusitions(players)
  log.info("accusitions")
  log.info(accusitions)
  game['LastAction'] = 'day accusitions'
  return response( {"Message": ["Day, time to awaken"
                                "Players accuse each other"] 
                                + accusitions + 
                               ["Who is the guilty?"] }, event)

def judgement_handler(event, context):
  log.debug(json.dumps(event, separators=(',', ':')))

  accused_player = event['queryStringParameters']['player']

  game    = load_game()

  players = game['Players']

  accused = game_controller.find_by_name(players, accused_player)
  if accused == None:
    return response( {"Message": "Sorry player {} not found".format(accused_player)}, event, 404)

  sentensed = players[accused]
  if sentensed['Identity'] == 'mafia':
    sentensed['Identity'] = 'Sentensed, guilty!'
    sentence = "{} is guilty!".format(sentensed['Name'])
  elif sentensed['Identity'] == 'innocent':
    sentensed['Identity'] = 'Sentensed, not guilty!'
    sentence = "{} is not guilty!".format(sentensed['Name'])
  else:
    return response( {"Message": "Sorry player {} is {} ".format(accused_player, sentensed['Identity'])}, event, 403) 

  game['LastAction'] = 'judgement'
  save_game(game)

  return response( {"Message": [
      "{} has been accused".format(sentensed['Name']),
      "Plyers identity has been revealed",
      sentence
    ]}, event)
