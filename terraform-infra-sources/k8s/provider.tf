provider "kubernetes" {
    config_path    = "~/.kube/config"
    config_context = "minikube"
}

provider "aws" {

    access_key                  = "fake_access_key"
    secret_key                  = "fake_secret_key"
    region                      = var.aws_region

    s3_use_path_style           = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true

    endpoints {
        iam            = var.localstack_endpoint
    }

    default_tags {
        tags = {
        Environment = "Techincal Challenge"
        Company        = "-"
        }
    }
}