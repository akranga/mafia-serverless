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


def find_all_uncovered():
  return table.scan(
           FilterExpression=Attr('Identity').eq('Uncovered')
          )['Items']


def find_by_identity(identity):
  return table.scan(
           FilterExpression=Attr('TrueIdentity').eq(identity) & 
                            Attr('Identity').eq('Uncovered')
          )['Items']


def handler(event, context): 
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


def response(body, event, code=200):
  if 'resource' in event and 'httpMethod' in event:
    return {
        'statusCode': code,
        'headers': {},
        'body': json.dumps(body, indent=4, cls=DecimalEncoder, separators=(',', ':')) 
      }
  return body