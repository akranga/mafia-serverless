variable "name" {
  type = "string"
  description = "name of the environment"
}

variable "aws_region" {
  type = "string"
  description = "target aws region"
  default = "eu-west-1"
}

variable "aws_profile" {
  type = "string"
  description = "aws profile from .aws/config file"
  default = "default"
}