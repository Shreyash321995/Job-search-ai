terraform {
  backend "s3" {
    bucket       = "shreyashd-602506756303"
    key          = "storage/s3/dev/terraform.tfstate"
    region       = "ap-south-1"
    use_lockfile = false

  }
}