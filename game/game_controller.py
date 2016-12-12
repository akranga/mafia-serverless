import uuid, random

with open('names.txt', 'r') as f:
  all_names = f.read().splitlines()


def new_game(num_of_players=5, num_of_mafia=3):
  players = ['innocent' for x in range(num_of_players)]
  names = list(all_names)
  random.shuffle(names)

  for i in random.sample(range(0, num_of_players), 3):
    players[i] = 'mafia'

    return [ {
        'Name'     : names[index],
        'Identity' : ident 
      } for index, ident in (enumerate(players)) ]


def hide_uncovered_identities(players):
  for player in players:
    if player['Identity'] in ["mafia", "innocent"]:
      player['Identity'] = 'unknown'

def find_by_identity(players, identity):
  result = []
  for index, player in enumerate(players):
    if player['Identity'] == identity:
      result.append(index)
  return result

def find_by_name(players, name):
  for index, player in enumerate(players):
    if player['Name'].lower() == name.lower():
      return index
  return None

def victim_of_mafia(players):
  innocent = find_by_identity(players, 'innocent')
  return random.choice(innocent)

def get_players_accusitions(players):
  innocent  = find_by_identity(players, 'innocent')
  everybody = innocent + find_by_identity(players, 'mafia')
  accusitions = []
  for index, player in enumerate(players):
    name = player['Name']
    if player['Identity'] == "killed":
      accusitions.append( "{} is dead".format(players[index]['Name']) )
    if player['Identity'] == "mafia":
      accusitions.append( "{} accuses {}".format(name, players[random.choice(innocent)]['Name']) )
    if player['Identity'] == "innocent":
      accusitions.append( "{} accuses {}".format(name, players[random.choice(everybody)]['Name']) )
  return accusitions
