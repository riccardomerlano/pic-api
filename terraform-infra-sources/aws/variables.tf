variable "aws_region" {
  type        = string
  default     = "us-west-1"
}

variable "aws_alternative_region" {
  type        = string
  default     = "us-east-1"
}

variable "localstack_endpoint" {
  type        = string
  default     = "http://localhost:4566"
}

variable "localstack_s3_endpoint" {
  type        = string
  default     = "http://s3.localhost.localstack.cloud:4566"
}

variable "bucket_name" {
  type        = string
  default     = "pic-api-users"
}