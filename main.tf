
module "vpc" {

  source = "./Modules/vpc"

  environment         = var.environment
  region              = var.region
  vpc_cidr            = var.vpc_cidr
  availability_zone   = var.availability_zone
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
}

module "security_group" {

  source = "./Modules/security_group"

  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  my_ip       = var.my_ip
}

#module "ec2" {
 # source = "./modules/ec2"

  #ami           = var.ami
  #instance_type = var.instance_type
  #key_name      = var.key_name

  #public_subnet_id = module.vpc.public_subnet_ids[0]

#  ec2_sg_id = module.security_group.ec2_sg_id#
#}

module "alb" {

  source = "./modules/alb"

  environment = var.environment

  vpc_id = module.vpc.vpc_id

  alb_sg_id = module.security_group.alb_sg_id

  public_subnet_ids = module.vpc.public_subnet_ids
}

#module "asg" {
# source = "./modules/asg"
#} 
module "launch-template" {

  source = "./Modules/launch-template"

  environment = var.environment

  ami           = var.ami
  instance_type = var.instance_type
  key_name      = var.key_name

  ec2_sg_id = module.security_group.ec2_sg_id
}

module "asg" {

  source = "./Modules/asg"

  environment = var.environment

  launch_template_id = module.launch-template.launch_template_id

  target_group_arn = module.alb.target_group_arn

  public_subnet_ids = module.vpc.public_subnet_ids
}