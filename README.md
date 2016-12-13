# Welcome

Welcome to the serverless workshop. Herer we will practice some common concepts of serverless architecture as well as review some of the common use cases

# What is Serverless

Core of serverless architectures is so called FaaS (Function as a Servie).
Which is a lightweight container that contains OS and Runtime and has been attached to the code baseline (FaaS code). Main benefit: it is only takes few milliseconds to spin up a new contaner instance that will execute code functioun attached to it. If it only takes few milliseconds why should we run it all the time? What if Cloud Provider will keep container disabled (you will not pay) and only spin it when certain event will happen and let the code inside of the container to react (be executed, triggered by event).

So, in difference to VMs you pay only for every 100milliseconds of execution instead of paying by hour. Sounds great, isn't it? Where is the catch? 

And yes there is a catch. Serverless Architecture comes with some limitations. So you need to think on architecture design how to dodge it. But, if ycan get savings up to 100 and more times if you design properly.

This workshop will highlight some of the AWS (They far are leading in serverless computing) Lamba service specifics and will give you possibility to try by yourself what works good what for you.

More details about Serverless you will get in the first Lab

# Tools we use

We need to have a comprehensive toolset of the tools to do development for serverless. We will use the following:

- *AWS*: cloud native services of Amazon Web Services. They are far behind of Google and Microsoft (in terms of maturity of cloud services for serverless )

- *Terraform*: FaaS does not live in the vacuum. In order it to exist it needs to operatie with other cloud resources such as: storage, security, networking, eetc. So, instead of single FaaS (AWS Lambda) we need to deploy a stack of interconnected cloud resources. Terraform a "Mercedes" of the stacks provisioning. It's capabiilties goes beyond similar service from Amazon.

- *Python 2.7*: You don't need to be an expert of Python to complete this workshop however some programming experience (any language is good) can be be efitial. We have choisen Python because it is easier to illustrate some of the FaaS concepts rather than other language runtimes (such as: nodejs or Java)

- *CMake*: After spending some time with tons of differnet build tools. Author decided to pick CMake as a canonical build tool. It is less opiniated and well know for few decades (+ easy to learn)


# Lifecicle of the CMake

Well, CMake is probably easiest tool you can imagine. Everything has been expressed in `Makefile`. It should be operated from the same directory where `Makefile` exists. You need to run `make <tsk-name>` and that's it. \

Here are our tasks. As you will see (check the `Makefile`) it wraps some terraform commands, so you would have better user experience.

`plan` - this task allows to build deployment plan for Terraform

`deploy` - this applies deployment plan built by previous command

`all` - combines both tasks (this also a default task for makefile)

`destroy` - deletes stack that has been built with Terraform


# LAB - 0: prep the environment

There are two options how to use this workshop. 
1. Bring your own AWS. This will not going to cost you much. We estimate the whole workhop will cost less than 1USD. Your own cloud environment will guarantee that you are working on isolated from the other users environment wihtout risk of interference

2. User shared environment provided by us. Please be respectful to tother colleagues, don't kill other's stuff... Be careful to your's and it's all going to be just fine

If you use your own cloud then many steps from this tutororial can be skipped.

### Setting up Terraform variables

Choose a good name. Please note, the name for your environment needs to be unique but distinctive. It needs to be "small letters and dash separated"

Once you are ready: create a Terraform variables file: `terraform.tfvars`

```
name = "your-wonderful-name"
aws_region = "eu-west-1"
aws_profile = "default"
```

Make shure you have Terraform available in the PATH environment variable:

- You already have Terraform instlled (v0.7.2 and later). 
- Download one from (http://terraform.io/downloads.html)
- Copy from USB stick

If you want to run Terraform from your custom location, then please adjust `Makefile` (line # 8 to point to terraform alternative location)

By completion you should ber abe to run terraform via `Makefile`. Run following command:

`make all`

Waring Bug ahead: If terraform provisioning fails with error: 

```
aws_api_gateway_deployment.prod: Error creating API Gateway Deployment: BadRequestException: No integration defined for method
    status code: 400, request id: 6b25f33c-c04e-11e6-9ee2-7525de577dec
```

Down't worry. Wait 30 seconds to allow API Gateway to settle down and then run `make all` command again.

After completion you should be able to see creted resources by terraform. Pleaser put note of Terrform output, we are going to need it later.

Example of Terraform output

```
api_gateway_url = https://meo41ti2r7.execute-api.eu-west-1.amazonaws.com/prod
kms_arn = arn:aws:kms:eu-west-1:111222333444:key/0caebd58-5cec-4499-89cb-03eda35774e5
lambda_arn_01_new_game = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-new-game
lambda_arn_02_check_game_state = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-game-state
lambda_arn_03_night_murder = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-night-murder
lambda_arn_04_daily_accusition = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-day-accusition
lambda_arn_05_user_judgement = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-user-judgement
role_arn = arn:aws:iam::111222333444:role/role-00688b5357814c9474f5424323
role_name = role-00688b5357814c9474f5424323
```

If you missed outputs. You can always run: `make out` to see outputs again.

If you messed up enironment. Run the following
```
make destroy
make all
```

You should be able to get initial state of your environment

### LAB 01: Getting started with AWS Lambda

1. With your Internet Browser. Connect to AWS Web Console [here](http://akranga.signin.aws.amazon.com/console?region=eu-west-1) or to your own Cloud Account.

2. Switch to the region Ireland (eu-west-1). Since now we will presume you are located in the Ireland region. All links will be to this region. If you decided to go to the other region, you might want to adjust direct links to your desired region.

3. Switch to AWS Lambda service: [direct link](https://eu-central-1.console.aws.amazon.com/lambda/home?region=eu-west-1)

![Screenshot 1](docs/images/pic-001.png)

4. Select lambda function that has been tagged as `your-environment-name-01-new-game` 

![Screenshot 2](docs/images/pic-002.png)

You will see several tabs. Let me guide through these it:
- *Code*: this tab shall be used to modify the code. Configuration management parameters can be injected via Environment Variables (scroll down)

- *Configuration*: This tab has been used to customize this Lambda function. Probably ost importaant text field is: Handler. It looks like the following: `main.new_game_handler`. Where, first part corresponds to the source code file name and second part is the name of the function to be executed.

Advanced settings also contains: RAM and Timeout constraints for this lambda function

- *Triggers*: here you can customize event source for the Lambda function (we will come back here in further Labs)

- *Monitoring*: contains reference to the LambdaFunction CloudWatch Logs. AWS Lmbda has no remote debugger functionality. So, logs become vitally important

On top left you will also find few buttons. Click on blue `Test` button. For the first time you should be able to see dialog to configure test event. It must be expressed in valid JSON format. Empty event looks like on the picture (`{}`) below. And then click "Save and Test" button (bottom right corner).

![Screenshot 3](docs/images/pic-003.png)

If execution has been completed successfully you shouls see. Result message, and function logs as well as used RAM and Function time statistics

![Screenshot 4](docs/images/pic-004.png)

### Lab 01.2: Modify behaviour of Lambda function

Knowing how to change code and test it, let's implement `new_game_handler` function. We should be able to create create a new game (gererate Players and assign Mafia identities to them). Because we don't want to reveal players identity to the User (remember Lambda is stateless) we are going to add backend database table to our AWS Lambda. We shall use it as cache to make sure our data survive Lambda container restart. But first let's start with the behavour of the `new_game_handler` function

Change imlementation to code that looks like below:
```python
def new_game_handler(event, context):
  game = {
    'GameId':     str(uuid.uuid1()),
    'Players':    game_controller.new_game(),
    'LastAction': 'new', 
    'Result':     'unknown'
  }

  names = [ player['Name'] for player in game['Players'] ]
  message = "New game started with {}".format(', '.join(names))
  return response( {"message": message}, event)
```

For your convinience. Mafia game control logic has been already implemen ted in file `game_controller.py` which is imported in the beginning of the file

Click `Save` button and then click `Test` button.

You should bet something like:
```javascript
{
  "message": "New game started with Christopher, Adam, Kevin, Brenda, Nicholas"
}
```
Where names are randomly selected player names. Few of them are `innocent` others hide `mafia` identity.

Let's add a database. If you will scroll down, you will find that Environment Variable `dynamo_table` has been set to the DynamoDB table name (that happend during provisioning with Terraform).

Let's initialize this table by placing code (just below log inicialization).
```python
log = logging.getLogger()
log.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['dynamo_table'])
```

And let's implement Dynamo DB CRUD functions.
```python
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
```

Please modify `new_game_handler` function so it would now include DB functions. You should get something like the follwing:

```python
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
```

Checking the data. We can switch to the `DynamoDB` service by following this [link](https://eu-west-1.console.aws.amazon.com/dynamodb/home?region=eu-west-1)

Navigate to the database that has been propogated to the Lambda function through the environment variable. `make out` can help to navigate the command

![Screenshot 5](docs/images/pic-005.png)

You can drill down to the data 

![Screenshot 6](docs/images/pic-006.png)

### Lab 01.2: Add behavior to the game_state_handler function

In a similar manner let's come back to our lambda functions [link](http://akranga.signin.aws.amazon.com/console?region=eu-west-1)

![Screenshot 1](docs/images/pic-001.png)

Now let's select function `your-environment-name-02-game-state`

Before we try to modify this function, let's make shure it works. Click "Test"button and end "empty" (`{}`) as Test Input Message. If you see the same  as on the screenshot below...

![Screenshot 2](docs/images/pic-002.png)

...then you feel free to proceed with this activity. Otherwise you might want to correct error first.

!!! Please apply same modifications as they were for for *Lab 01.1* and then add the following 

```python
def game_state_handler(event, context):
  game = load_game()
  players = game['Players']
  game_controller.hide_uncovered_identities( players )
  return response(game, event)
```

Then click "Test". You shuld see function execution successfull otherwise you might want to correct an error.

### Lab 01.3: Add behavior to night_murder function

Based on what you learned in *Lab 01.1* and *Lab 01.2*
let's modify all other functions. (!!! Don't forget to propogate DB shared functions)

And Lambda implementation code:
```python
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
```

Uppon successful execution you should see something like this
```javascript
{
  "Message": [
    "Night, time to sleep",
    "Mafia awaken",
    "Mafia kills Deborah",
    "Mafia sleeps"
  ]
}
```

### Lab 01.4: Add behavior to daily_accusition function

Very similar to previous ones:
```python
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

```

And successful execution result should look like this
```javascript
{
  "Message": [
    "Day, time to awakenPlayers accuse each other",
    "Deborah is dead",
    "Amy accuses Gregory",
    "Brandon accuses Brandon",
    "Dennis accuses Amy",
    "Gregory accuses Amy",
    "Who is the guilty?"
  ]
}
```

### Lab 01.5: Add behavior to judgement function

Propogate DB shared functions and lambda handler
```python
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
```

But you will see this function relies on user argument that comes with event
```javascript
{
  "body": "{\"Message\":[\"Amy has been accused\",\"Plyers identity has been revealed\",\"Amy is not guilty!\"]}",
  "headers": {},
  "statusCode": 200
}
```

### Tear Down

To destroy your cloud resources, please run:
`make destroy`
