variable "app_name" {
  description = "The name of the application."
  type        = string
}

variable "aws_account_id" {
  description = "The AWS account ID."
  type        = string
  default     = "617961504899"
}

variable "aws_region" {
  description = "The AWS region."
  type        = string
  default     = "eu-west-1"
}
