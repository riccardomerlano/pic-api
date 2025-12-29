resource "aws_iam_role" "primary_bucket_role" {

    name               = "rp-s3-primary-bucket-role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "primary_bucket_policy" {

    name   = "rp-s3-primary-bucket-policy"
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": [
        "${var.primary_bucket.arn}"
      ]
    },
    {
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectVersionTagging"
      ],
      "Effect": "Allow",
      "Resource": [
        "${var.primary_bucket.arn}/*"
      ]
    },
    {
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete",
        "s3:ReplicateTags"
      ],
      "Effect": "Allow",
      "Resource": "${var.secondary_bucket.arn}/*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "primary_bucket_role_attachment" {
    role       = aws_iam_role.primary_bucket_role.name
    policy_arn = aws_iam_policy.primary_bucket_policy.arn
}

## SECONDARY BUCKET IAM RESOURCES

resource "aws_iam_role" "secondary_bucket_role" {
    provider = aws.secondary_region

    name               = "rp-s3-secondary-bucket-role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "secondary_bucket_policy" {
    provider = aws.secondary_region

    name   = "rp-s3-secondary-bucket-policy"
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": [
        "${var.secondary_bucket.arn}"
      ]
    },
    {
      "Action": [
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectVersionTagging"
      ],
      "Effect": "Allow",
      "Resource": [
        "${var.secondary_bucket.arn}/*"
      ]
    },
    {
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete",
        "s3:ReplicateTags"
      ],
      "Effect": "Allow",
      "Resource": "${var.primary_bucket.arn}/*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "secondary_bucket_role_attachment" {
    provider = aws.secondary_region
    role       = aws_iam_role.secondary_bucket_role.name
    policy_arn = aws_iam_policy.secondary_bucket_policy.arn
}