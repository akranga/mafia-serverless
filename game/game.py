import uuid, random

with open('names.txt', 'r') as f:
  all_names = f.read().splitlines()


def new_game(num_of_players=5):
  players = ["innocent" for x in range(num_of_players)]
  names = list(all_names)
  random.shuffle(names)

  for i in random.sample(range(0, num_of_players), 3):
    players[i] = 'mafia'

  return {
    'id': str(uuid.uuid1()),
    'players': [ {
        'name'     : names[index],
        'identity' : ident 
    } for index, ident in (enumerate(players)) ]
  }

def find_innocent(players):
  innocent = []
  for index, player in enumerate(players):
    if player['identity'] == 'innocent':
      innocent.append(index)
  return innocent


def find_mafia(players):
  innocent = []
  for index, player in enumerate(players):
    if player['identity'] == 'mafia':
      innocent.append(index)
  return innocent


def night_handler(players):
  print "Time to sleep"
  print "Mafia awaken"
  innocent = find_innocent(players)
  victim = random.choice(innocent)
  print "Mafia kills {}".format(players[victim]['name'])
  players[victim]['identity'] = "killed"
  print "Mafia sleeps"
  return players


def day_handler(players):
  print "Time to awaken"
  print "Players makes an accusition"
  innocent = find_innocent(players)
  survived = innocent + find_mafia(players)

  for index, player in enumerate(players):
    name = player['name']
    if player['identity'] == "killed":
      print "{} is dead".format(players[index]['name'])
    if player['identity'] == "mafia":
      print "{} accuses {}".format(name, players[random.choice(innocent)]['name'])
    if player['identity'] == "innocent":
      print "{} accuses {}".format(name, players[random.choice(survived)]['name'])

  print "Detective, who is the mafia?"

game = new_game()

print game

players = game['players']
players = night_handler(players)
print day_handler(players)

