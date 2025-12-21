resource "aws_s3_bucket_replication_configuration" "primary_to_secondary" {

    role   = aws_iam_role.primary_bucket_role.arn
    bucket = aws_s3_bucket.primary_bucket.id

    rule {
        id = "s3-primary-to-secondary"

        destination {
            bucket        = aws_s3_bucket.secondary_bucket.arn
            storage_class = "STANDARD"
        }

        status = "Enabled"
    }

    depends_on = [
        aws_s3_bucket_versioning.secondary_bucket_versioning,
        aws_s3_bucket_versioning.primary_bucket_versioning
    ]
}

resource "aws_s3_bucket_replication_configuration" "secondary_to_primary" {
    provider = aws.secondary_region

    role   = aws_iam_role.secondary_bucket_role.arn
    bucket = aws_s3_bucket.secondary_bucket.id

    rule {
        id = "s3-secondary-to-primary"

        destination {
            bucket        = aws_s3_bucket.primary_bucket.arn
            storage_class = "STANDARD"
        }

        status = "Enabled"
    }

    depends_on = [
        aws_s3_bucket_versioning.secondary_bucket_versioning,
        aws_s3_bucket_versioning.primary_bucket_versioning
    ]
}