resource "helm_release" "pic-api" {
  name = "pic-api"

  chart = "${path.module}/../../helm-charts/helm-api-deployment"

  create_namespace = true
  namespace        = local.namespace

  values = [
    file("./resources/pic-api-helm-values.yaml")
  ]

}
