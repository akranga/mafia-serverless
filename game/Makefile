.DEFAULT_GOAL := release

AWS_PROFILE ?= default
SHELL := /bin/bash
S3BUCKET ?= mafia-workshop-sourcecode

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

release: package
	$(aws) s3 cp lambda.zip s3://$(S3BUCKET)/lambda.zip
.PHONY: release

