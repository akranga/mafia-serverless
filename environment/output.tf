output "api_gateway_url" {
  value = "https://${module.apig.endpoint_host}/${aws_api_gateway_deployment.prod.stage_name}"
}

output "role_name" {
  value = "${aws_iam_role.iam_for_lambda.name}"
}

output "role_arn" {
  value = "${aws_iam_role.iam_for_lambda.arn}"
}

output "kms_arn" {
  value = "${aws_kms_key.a.arn }"
}

output "lambda_arn_01_new_game" {
  value = "${aws_lambda_function.new_game.arn }"
}

output "lambda_arn_02_check_game_state" {
  value = "${aws_lambda_function.check_game_state.arn }"
}

output "lambda_arn_03_night_murder" {
  value = "${aws_lambda_function.night_murder.arn }"
}

output "lambda_arn_04_daily_accusition" {
  value = "${aws_lambda_function.daily_accusition.arn }"
}

output "lambda_arn_05_user_judgement" {
  value = "${aws_lambda_function.user_judgement.arn }"
}