# No lifecycle management is implemented in this module, in a real-world scenario
# it should be implemented to move to a cooler storage class if the avatar is not accessed for a certain period of time.

resource "aws_s3_bucket" "bucket" {
    bucket = local.bucket_name
}

resource "aws_s3_bucket_public_access_block" "bucket_access_block" {
    bucket                  = aws_s3_bucket.bucket.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "bucket_versioning" {
    bucket = aws_s3_bucket.bucket.id
    versioning_configuration {
        status = "Enabled"
    }
}

