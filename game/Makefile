.DEFAULT_GOAL := package

function ?= lab01-devops-delivery
AWS_PROFILE ?= default
SHELL := /bin/bash

aws=aws --profile='$(AWS_PROFILE)'

init:
	virtualenv .venv

deploy: package
	$(aws) lambda update-function-code --function-name="$(function)" --zip-file=fileb://lambda.zip --publish
.PHONY: deploy


install:
	source .venv/bin/activate && pip install chalice --upgrade &&  pip install -r requirements.txt -t lib --upgrade

package:
	yes n |rm -f lambda.zip || true
	zip -9 -r lambda.zip . -x@.zipignore
