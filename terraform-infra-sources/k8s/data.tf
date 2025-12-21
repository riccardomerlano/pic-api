
data "aws_iam_policy" "pic_api_s3_read_policy" {
    name = "pic-api-s3-read-policy"
}

data "aws_iam_policy" "pic_api_s3_write_policy" {
    name = "pic-api-s3-write-policy"
}
