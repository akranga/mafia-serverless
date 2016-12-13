resource "aws_dynamodb_table" "main" {
    name = "player-${uuid()}"
    read_capacity = 20
    write_capacity = 20
    hash_key = "GameId"
    attribute {
      name = "GameId"
      type = "S"
    }
}
