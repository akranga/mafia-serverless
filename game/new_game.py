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
# TODO: Bootstrap a DynamoDB (check env vars for lambda
#
def handler(event, context):
  num_of_players = int(os.environ['NUMBER_OF_PLAYERS'])
  num_of_mafia   = int(os.environ['NUMBER_OF_MAFIA'])
  clear_all()

  names  = random.sample(all_names, num_of_players)
  mafia  = random.sample(range(0, num_of_players), num_of_mafia)

  for i in range(num_of_players):
    player = {
      'Name': names[i],
      'TrueIdentity': 'Mafia' if i in mafia else 'Innocent',
      'Identity':     'Uncovered'
    }
    save(player)

  message = "New game started with {}".format(', '.join(names))
  return response( {"message": message}, event )


def clear_all():
  for i in table.scan()['Items']:
    table.delete_item(Key={'Name': i['Name']})


def save(player):
  table.put_item(Item=player)


def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, indent=4, cls=DecimalEncoder, separators=(',', ':')) 
        # 'body': json.dumps(body, separators=(',', ':')) 
      }
  return body

