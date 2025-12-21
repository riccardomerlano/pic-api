resource "aws_dynamodb_table" "pic_api_users_information_table" {
    billing_mode   = "PROVISIONED"
    read_capacity  = 5
    write_capacity = 5
    name             = "pic-api-users-information"
    hash_key         = "name"

    attribute {
        name = "name"
        type = "S"
    }

    tags = {
        Service = "dynamodb"
    }

    deletion_protection_enabled = true

    replica {
        region_name    = replace(var.aws_region, "1", "2")
        propagate_tags = true
    }
    replica {
        region_name    = var.aws_alternative_region
        propagate_tags = true
    }

}

##########################################################
# Some example items for this technical challenge
# Uncomment and apply in a second terraform plan/apply run
##########################################################

# resource "aws_dynamodb_table_item" "ric_item" {
#   table_name = aws_dynamodb_table.pic_api_users_information_table.name
#   hash_key   = aws_dynamodb_table.pic_api_users_information_table.hash_key

#   item = <<ITEM
# {
#   "name": {"S": "ric"},
#   "email": {"S": "ric@email.com"},
#   "avatar_url": {"S": "s3://pic-api-users-us-west-1/ric/user-avatar.png"}
# }
# ITEM
# }

# resource "aws_dynamodb_table_item" "mr_x_item" {
#   table_name = aws_dynamodb_table.pic_api_users_information_table.name
#   hash_key   = aws_dynamodb_table.pic_api_users_information_table.hash_key

#   item = <<ITEM
# {
#   "name": {"S": "mr-x"},
#   "email": {"S": "x@email.com"},
#   "avatar_url": {"S": "s3://pic-api-users-us-west-1/mr-x/user-default-profile-image.jpg"}
# }
# ITEM
# }

# resource "aws_dynamodb_table_item" "totoro_item" {
#   table_name = aws_dynamodb_table.pic_api_users_information_table.name
#   hash_key   = aws_dynamodb_table.pic_api_users_information_table.hash_key

#   item = <<ITEM
# {
#   "name": {"S": "totoro"},
#   "email": {"S": "totoro@ghiblistudio.com"},
#   "avatar_url": {"S": "s3://pic-api-users-us-west-1/totoro/totoro.jpg"}
# }
# ITEM
# }
