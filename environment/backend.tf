resource "aws_dynamodb_table" "main" {
    name = "player-${uuid()}"
    read_capacity = 20
    write_capacity = 20
    hash_key = "GameId"
    attribute {
      name = "GameId"
      type = "S"
    }
    # global_secondary_index {
    #   name = "GameTitleIndex"
    #   hash_key = "GameTitle"
    #   range_key = "TopScore"
    #   write_capacity = 10
    #   read_capacity = 10
    #   projection_type = "INCLUDE"
    #   non_key_attributes = [ "UserId" ]
    # }
}
