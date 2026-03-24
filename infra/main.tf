# 1. Le decimos a Terraform qué "plugins" necesita descargar
terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.4.0"
    }
  }
}

# 2. Configuramos el proveedor (no necesita credenciales porque usa el Docker local)
provider "kind" {}

# 3. Definimos el recurso que queremos crear
resource "kind_cluster" "mi_cluster" {
  name           = "cluster-gitops-pro"
  node_image     = "kindest/node:v1.30.0"
  wait_for_ready = true
}