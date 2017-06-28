.DEFAULT_GOAL := all

export TF_LOG := debug
export TF_LOG_PATH := terraform.log
export SHELL := /bin/bash

export terraform=terraform

export TF_OPTS ?=

all: package plan apply

plan:
	$(terraform) get -update
	$(terraform) plan $(TF_OPTS) -module-depth=-1 -state=terraform.tfstate -var-file terraform.tfvars -out terraform.tfplan
.PHONY: plan

apply:
	$(terraform) apply -Xshadow=false -backup=- -state=terraform.tfstate terraform.tfplan
.PHONY: apply

destroy:
	$(terraform) plan $(TF_OPTS) -destroy -var-file terraform.tfvars -state=terraform.tfstate -out terraform.tfplan
	@$(MAKE) apply
.PHONY: destroy

clean: destroy
	yes n |rm -f terraform.log || true
	yes n |rm -f terraform.tfplan || true
	yes n |rm -f terraform.tfstate || true 
	yes n |rm -fR .terraform
.PHONY: clean

package:
	cd ../game && $(MAKE) package
	cp -f ../game/lambda.zip .
.PHONY: package


out:
	$(terraform) output --state=terraform.tfstate
.PHONY: out