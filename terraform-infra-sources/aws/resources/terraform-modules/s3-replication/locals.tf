locals {
    bucket_name = "${var.bucket}-${var.primary_region}"
    fallback_bucket_name = "${var.bucket}-${var.secondary_region}"
}