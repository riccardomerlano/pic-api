resource "aws_iam_policy" "pic_api_s3_read_policy" {
  name        = "pic-api-s3-read-policy"
  description = "Read access to ${var.bucket_name}"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}-${var.aws_region}",
          "arn:aws:s3:::${var.bucket_name}-${var.aws_region}/*",
          "arn:aws:s3:::${var.bucket_name}-${var.aws_alternative_region}",
          "arn:aws:s3:::${var.bucket_name}-${var.aws_alternative_region}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "pic_api_s3_write_policy" {
  name        = "pic-api-s3-write-policy"
  description = "Write access to ${var.bucket_name}"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:PutObject",
          "s3:DeleteObject",              
          "s3:DeleteObjectVersion"
          ,
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}-${var.aws_region}",
          "arn:aws:s3:::${var.bucket_name}-${var.aws_region}/*",
          "arn:aws:s3:::${var.bucket_name}-${var.aws_alternative_region}",
          "arn:aws:s3:::${var.bucket_name}-${var.aws_alternative_region}/*"
        ]
      }
    ]
  })
}