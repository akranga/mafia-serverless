provider "aws" {
    profile = "${var.aws_profile}"
    region  = "${var.aws_region}"
}

module "apig" {
  source     = "github.com/akranga/terraform-modules//api_gateway"
  name       = "api.${var.name}"
  aws_region = "${var.aws_region}"
}

resource "aws_api_gateway_deployment" "dev" {
  rest_api_id = "${module.apig.id}"
  stage_name  = "dev"

  variables  = {
    hello = "world"
  }
}

resource "aws_api_gateway_api_key" "main" {
  name = "dev"
  description = "API gateway key"

  stage_key {
    rest_api_id = "${module.apig.id}"
    stage_name  = "${aws_api_gateway_deployment.dev.stage_name}"
  }
}

