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

Example Terraform output

```
api_gateway_url = https://meo41ti2r7.execute-api.eu-west-1.amazonaws.com/prod
kms_arn = arn:aws:kms:eu-west-1:111222333444:key/0caebd58-5cec-4499-89cb-03eda35774e5
lambda_arn_01_new_game = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-new-game
lambda_arn_02_check_game_state = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-game-state
lambda_arn_03_night_murder = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-night-murder
lambda_arn_04_daily_accusition = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-day-accusition
lambda_arn_05_user_judgement = arn:aws:lambda:eu-west-1:111222333444:function:my-environment-name-user-judgement
role_arn = arn:aws:iam::111222333444:role/role-00688b5357814c9474f5424323
role_name = role-00688b5357814c9474f5424323```

If you missed outputs. You can always run: `make out` to see outputs again.

If you messed up enironment. Run the following
```
make destroy
make all
```

You should be able to get initial state of your environment

### LAB 01: Getting started with AWS Lambda

1. With your Internet Browser. Connect to AWS Web Console [here](http://akranga.signin.aws.amazon.com/console?region=eu-west-1) or to your own Cloud Account.

2. Switch to the region Ireland (eu-west-1). Since now we will presume you are located in the Ireland region. All links will be to this region. If you decided to go to the other region, you might want to adjust commands

3. Switch to AWS Lambda service. 