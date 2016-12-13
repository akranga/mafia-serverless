provider "aws" {
    region  = "${var.aws_region}"
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
}

module "apig" {
  source     = "github.com/akranga/terraform-modules//api_gateway"
  name       = "api.${var.name}"
  aws_region = "${var.aws_region}"
}

resource "aws_api_gateway_deployment" "prod" {
  rest_api_id = "${module.apig.id}"
  stage_name  = "prod"

  variables  = {
    hello = "world"
  }
}

resource "aws_api_gateway_api_key" "main" {
  name = "prod"
  description = "API gateway key"

  stage_key {
    rest_api_id = "${module.apig.id}"
    stage_name  = "${aws_api_gateway_deployment.prod.stage_name}"
  }
}

resource "aws_kms_key" "a" {
    description = "KMS key 1"
    deletion_window_in_days = 10
}
