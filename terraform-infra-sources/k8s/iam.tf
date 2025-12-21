resource "aws_iam_user" "pic-api_user" {
    name = "pic-api"
}

resource "aws_iam_user_policy_attachment" "pic-api_user_read_bucket_attachment" {
  user       = aws_iam_user.pic-api_user.name
  policy_arn = data.aws_iam_policy.pic_api_s3_read_policy.arn
}

resource "aws_iam_user_policy_attachment" "pic-api_user_write_bucket_attachment" {
  user       = aws_iam_user.pic-api_user.name
  policy_arn = data.aws_iam_policy.pic_api_s3_write_policy.arn
}
