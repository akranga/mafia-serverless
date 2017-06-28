import os, sys
# to read dependencies from ./lib direcroty
script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.insert(0, script_dir + os.sep + "lib")
import logging, boto3, json

# for dynamodb filter queries
from boto3.dynamodb.conditions import Key, Attr

# setup log level to DEBUG
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE'])


def get_name_from_event(event):
  if 'queryStringParameters' in event:
    if 'Name' in event['queryStringParameters']:
      return event['queryStringParameters']['Name']
  return event['Name']


def find_by_name(name):
  result = table.scan(
           FilterExpression=Attr('Identity').eq('Uncovered') &
                            Attr('Name').eq(name)
          )['Items']
  return result[0] if result else None


def handler(event, context):
  log.debug(json.dumps(event, separators=(',', ':')))

  name      = get_name_from_event(event)
  sentenced = find_by_name(name)
  if sentenced == None:
    return response({
        "Message": "Player with name {} not found".format(name)
      }, event, 404
    )

  print(sentenced)
  if sentenced['TrueIdentity'] == 'Mafia':
    sentenced['Identity'] = 'Correctly sentenced'
    message = [
        'Mafia has been uncovered!',
        'Guilty member of mafia {} has been sentenced!'.format(sentenced['Name'])
      ]
  else:
    sentenced['Identity'] = 'Incorrectly sentenced'
    message = [
        'Mafia has not been uncovered!',
        'Innocent {} has been sentenced unfairly'.format(sentenced['Name'])
      ]
  
  save(sentenced)
  return response({"Message": message}, event)



def save(player):
  table.put_item(Item=player)



def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, indent=4, separators=(',', ':')) 
      }
  return body