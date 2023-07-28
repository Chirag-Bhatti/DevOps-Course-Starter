variable "client_id" {
  description = "The client ID of the github OAuth app"
  sensitive   = true
}

variable "client_secret" {
  description = "The client secret of the github OAuth app"
  sensitive   = true
}

variable "env" {
  description = "The environment for all resources"
}

variable "prefix" {
  default     = "chibha-ex12"
  description = "The prefix used for all resources in this environment"
}

variable "secret_key" {
  description = "The secret key for the flask application"
  sensitive   = true
}