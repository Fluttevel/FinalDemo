locals {
  bucket_prefix      = "demo-3-tf"
  aws_account        = "692807581431"
  aws_region         = "eu-west-2"
  ecr_repository_url = "692807581431.dkr.ecr.eu-west-2.amazonaws.com"
  app_name           = "demo"
  environment        = "dev"
  image_tag          = "beta.v.0.3"
  script             = "docker-script.sh"
  working_dir        = "./app" # ?
  app_count          = 1
  server_port        = 80
  count_value        = 2
}

inputs = {
  bucket             = format("%s-%s-%s-%s", local.bucket_prefix, local.app_name, local.environment, local.aws_region)
  aws_account        = local.aws_account
  aws_region         = local.aws_region
  ecr_repository_url = local.ecr_repository_url
  app_name           = local.app_name
  environment        = local.environment
  image_tag          = local.image_tag
  script             = local.script
  working_dir        = local.working_dir
  app_count          = local.app_count
  server_port        = local.server_port
  count_value        = local.count_value
}

remote_state {
  backend = "s3"

  config = {
    encrypt        = true
    bucket         = format("%s-%s-%s-%s", local.bucket_prefix, local.app_name, local.environment, local.aws_region)
    key            = format("%s/terraform.tfstate", path_relative_to_include())
    region         = local.aws_region
    dynamodb_table = format("tflock-%s-%s-%s", local.environment, local.app_name, local.aws_region)
    profile        = local.aws_profile
  }
}

# Version Locking
## tfenv exists to help developer experience for those who use tfenv
## it will automatically download and use this terraform version
generate "tfenv" {
  path              = ".terraform-version"
  if_exists         = "overwrite"
  disable_signature = true

  contents = <<EOF
1.1.2
EOF
}

terraform_version_constraint = "1.1.2"

terragrunt_version_constraint = ">= 0.31.3"

terraform {
  after_hook "remove_lock" {
    commands = [
      "apply",
      "console",
      "destroy",
      "import",
      "init",
      "plan",
      "push",
      "refresh",
    ]

    execute = [
      "rm",
      "-f",
      "${get_terragrunt_dir()}/.terraform.lock.hcl",
    ]

    run_on_error = true
  }
}