# No lifecycle management is implemented in this module, in a real-world scenario
# it should be implemented to move to a cooler storage class if the avatar is not accessed for a certain period of time.

resource "aws_s3_bucket" "primary_bucket" {
    bucket = local.bucket_name
}

resource "aws_s3_bucket_public_access_block" "primary_bucket_access_block" {
    bucket                  = aws_s3_bucket.primary_bucket.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "primary_bucket_versioning" {
    bucket = aws_s3_bucket.primary_bucket.id
    versioning_configuration {
        status = "Enabled"
    }
}

## SECONDARY BUCKET S3 RESOURCES

resource "aws_s3_bucket" "secondary_bucket" {
    provider = aws.secondary_region
    bucket = local.fallback_bucket_name
}

resource "aws_s3_bucket_public_access_block" "secondary_bucket_access_block" {
    provider = aws.secondary_region

    bucket                  = aws_s3_bucket.secondary_bucket.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "secondary_bucket_versioning" {
    provider = aws.secondary_region

    bucket = aws_s3_bucket.secondary_bucket.id
    versioning_configuration {
        status = "Enabled"
    }
}
