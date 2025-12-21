module "pic-api-replicated-s3-bucket" {
  providers = {
    aws.secondary_region = aws.secondary_region
  }
  source               = "./resources/terraform-modules/s3-replication"
  primary_region       = var.aws_region
  secondary_region     = var.aws_alternative_region
  bucket               = var.bucket_name
}


##########################################################
# Some example items for this technical challenge
# Uncomment and apply in a second terraform plan/apply run
##########################################################

## Since LocalStack does not support S3 replication, we emulates the replication by creating the same objects in both buckets.
# locals {
#   buckets_list = [
#     module.pic-api-replicated-s3-bucket.primary_bucket_id,
#     module.pic-api-replicated-s3-bucket.secondary_bucket_id
#   ]
# }

# resource "aws_s3_object" "default_user_image" {
#   for_each = toset(local.buckets_list)
#   bucket = each.value
#   key    = "default-user/user-default-profile-image.jpg"
#   source = "./resources/images/user-default-profile-image.jpg"
#   etag   = filemd5("./resources/images/user-default-profile-image.jpg")
#   depends_on = [
#     module.pic-api-replicated-s3-bucket,
#     module.pic-api-replicated-s3-bucket
#   ]
# }

# resource "aws_s3_object" "ric_user_image" {
#   for_each = toset(local.buckets_list)
#   bucket = each.value
#   key    = "ric/user-avatar.png"
#   source = "./resources/images/user-avatar.png"
#   etag   = filemd5("./resources/images/user-avatar.png")
# }

# resource "aws_s3_object" "totoro_user_image" {
#   for_each = toset(local.buckets_list)
#   bucket = each.value
#   key    = "totoro/totoro.jpg"
#   source = "./resources/images/totoro.jpg"
#   etag   = filemd5("./resources/images/totoro.jpg")
# }