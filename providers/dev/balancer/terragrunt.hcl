terraform {
  source = "../../../modules//balancer"
}

include {
  path = find_in_parent_folders()
}

dependency "network" {
  config_path = "../network"
}

inputs = merge({
  vpc_id = dependency.network.outputs.vpc_id
  public_subnets_id = dependency.network.outputs.public_subnets_id
})