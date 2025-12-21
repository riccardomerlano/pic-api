output "primary_bucket_id" {
  value = aws_s3_bucket.primary_bucket.id
}

output "secondary_bucket_id" {
  value = aws_s3_bucket.secondary_bucket.id
}

