provider "aws" {

    access_key                  = "fake_access_key"
    secret_key                  = "fake_secret_key"

    region                      = var.aws_region

    s3_use_path_style           = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true

    endpoints {
        s3             = var.localstack_s3_endpoint
        dynamodb       = var.localstack_endpoint
        iam            = var.localstack_endpoint
    }

    default_tags {
        tags = {
        Environment = "Techincal Challenge"
        Company        = "-"
        }
    }
}

# Same as above with an alias for the secondary region.
provider "aws" {

    access_key                  = "fake_access_key"
    secret_key                  = "fake_secret_key"

    alias                      = "secondary_region"
    region                      = var.aws_alternative_region

    s3_use_path_style           = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true

    endpoints {
        s3             = var.localstack_s3_endpoint
        dynamodb       = var.localstack_endpoint
        iam            = var.localstack_endpoint
    }

    default_tags {
        tags = {
        Environment = "Techincal Challenge"
        Company        = "-"
        }
    }
}