output "api_gateway_url" {
  value = "https://${module.apig.endpoint_host}/${aws_api_gateway_deployment.dev.stage_name}"
}

output "role_name" {
  value = "${aws_iam_role.main.name}"
}

output "role_arn" {
  value = "${aws_iam_role.main.arn}"
}

# output "kms_id" {
#   value = "${aws_kms_key.a.key_id}"
# }

output "kms_arn" {
  value = "${aws_kms_key.a.arn }"
}