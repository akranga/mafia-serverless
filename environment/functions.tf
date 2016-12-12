resource "aws_lambda_function" "new_game" {
    function_name    = "${var.name}-01-new-game"
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
    function_name    = "${var.name}-03-night-murder"
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
    function_name    = "${var.name}-04-day-accusition"
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
    function_name    = "${var.name}-02-game-state"
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
    function_name    = "${var.name}-05-user-judgement"
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
