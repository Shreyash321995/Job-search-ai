variable "region" {}

variable "environment" {}

variable "vpc_cidr" {}

variable "availability_zone" {
  type = list(string)
}

variable "public_subnet_cidr" {
  type = list(string)
}

variable "private_subnet_cidr" {
  type = list(string)
}


variable "ami" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "key_name" {
  type = string
}
variable "my_ip" {}

#variable "environment" {
# type = string
#}

#variable "vpc_id" {
# type = string
#}

#variable "alb_sg_id" {
# type = string
#}

#variable "public_subnet_ids" {
# type = list(string)
#}