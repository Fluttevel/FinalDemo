terraform {
  source = "../../../modules//cluster"
}

include {
  path = find_in_parent_folders()
}

dependency "balancer" {
  config_path = "../balancer"
}

dependency "network" {
  config_path = "../network"
}

inputs = merge({
  private_subnets_id = dependency.network.outputs.private_subnets_id
  lb_target_group_id = dependency.balancer.outputs.lb_target_group_id
  lb_listener        = dependency.balancer.outputs.lb_listener
})