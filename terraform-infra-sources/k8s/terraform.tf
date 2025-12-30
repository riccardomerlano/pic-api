terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
    helm = {
      source = "hashicorp/helm"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67"
    }
  }
}