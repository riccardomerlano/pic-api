resource "aws_s3_bucket_replication_configuration" "primary_to_secondary" {

    role   = aws_iam_role.primary_bucket_role.arn
    bucket = var.primary_bucket.id

    rule {
        id = "s3-primary-to-secondary"

        destination {
            bucket        = var.secondary_bucket.arn
            storage_class = "STANDARD"
        }

        status = "Enabled"
    }
}

resource "aws_s3_bucket_replication_configuration" "secondary_to_primary" {
    provider = aws.secondary_region

    role   = aws_iam_role.secondary_bucket_role.arn
    bucket = var.secondary_bucket.id

    rule {
        id = "s3-secondary-to-primary"

        destination {
            bucket        = var.primary_bucket.arn
            storage_class = "STANDARD"
        }

        status = "Enabled"
    }

}