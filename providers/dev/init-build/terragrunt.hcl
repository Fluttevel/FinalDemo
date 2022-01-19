terraform {
  source = "../../../modules//init-build"
}

include {
  path = find_in_parent_folders()
}