resource "aws_lambda_function" "new_game" {
    function_name    = "${var.name}-new-game"
    filename         = "${path.cwd}/game/lambda.zip"
    runtime          = "python2.7"
    role             = "${aws_iam_role.iam_for_lambda.arn}"
    handler          = "main.new_game_handler"
    memory_size      = "128"
    timeout          = "60"
    publish          = true
    kms_key_arn      = "${aws_kms_key.a.arn}"
    environment {
      variables = {
        dynamo_table = "${aws_dynamodb_table.main.name}"
      }
    }
}


resource "aws_lambda_function" "night_murder" {
    function_name    = "${var.name}-night-murder"
    filename         = "${path.cwd}/game/lambda.zip"
    runtime          = "python2.7"
    role             = "${aws_iam_role.iam_for_lambda.arn}"
    handler          = "main.night_handler"
    memory_size      = "128"
    timeout          = "60"
    publish          = true
    kms_key_arn      = "${aws_kms_key.a.arn}"
    environment {
      variables = {
        dynamo_table = "${aws_dynamodb_table.main.name}"
      }
    }
}


resource "aws_lambda_function" "daily_accusition" {
    function_name    = "${var.name}-day-accusition"
    filename         = "${path.cwd}/game/lambda.zip"
    runtime          = "python2.7"
    role             = "${aws_iam_role.iam_for_lambda.arn}"
    handler          = "main.day_handler"
    memory_size      = "128"
    timeout          = "60"
    publish          = true
    kms_key_arn      = "${aws_kms_key.a.arn}"
    environment {
      variables = {
        dynamo_table = "${aws_dynamodb_table.main.name}"
      }
    }
}

resource "aws_lambda_function" "check_game_state" {
    function_name    = "${var.name}-game-state"
    filename         = "${path.cwd}/game/lambda.zip"
    runtime          = "python2.7"
    role             = "${aws_iam_role.iam_for_lambda.arn}"
    handler          = "main.game_state_handler"
    memory_size      = "128"
    timeout          = "60"
    publish          = true
    kms_key_arn      = "${aws_kms_key.a.arn}"
    environment {
      variables = {
        dynamo_table = "${aws_dynamodb_table.main.name}"
      }
    }
}

resource "aws_lambda_function" "user_judgement" {
    function_name    = "${var.name}-user-judgement"
    filename         = "${path.cwd}/game/lambda.zip"
    runtime          = "python2.7"
    role             = "${aws_iam_role.iam_for_lambda.arn}"
    handler          = "main.judgement_handler"
    memory_size      = "128"
    timeout          = "60"
    publish          = true
    kms_key_arn      = "${aws_kms_key.a.arn}"
    environment {
      variables = {
        dynamo_table = "${aws_dynamodb_table.main.name}"
      }
    }
}

# module "lab01_lambda" {
#   # source      = "../../../agilestacks/terraform-modules//lambda"
#   source   = "github.com/akranga/terraform-modules//lambda"
#   name        = "lab01-${var.name}"
#   handler     = "main.handler"
#   zip_file    = "${path.cwd}/game/lambda.zip"
#   policy      = "${file("${path.cwd}/game/policy.json")}"
#   kms_key_arn = "${aws_kms_key.a.arn}"
#   variables = {
#     dynamo_table = "${aws_dynamodb_table.main.name}"
#   }
# }