terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "Cohort25_ChiBha_ProjectExercise"
    storage_account_name = "chibhaex12storageaccount"
    container_name       = "chibhaex12storagecontainer"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

locals {
  prefix = "${var.prefix}-${var.env}"
}

data "azurerm_resource_group" "main" {
  name = "Cohort25_ChiBha_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${local.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${local.prefix}-linux-web-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name = "cbhatti/todo-app"
      docker_image_tag  = "prod"
    }
  }

  app_settings = {
    "CLIENT_ID"                           = var.client_id
    "CLIENT_SECRET"                       = var.client_secret
    "CONNECTION_STRING"                   = azurerm_cosmosdb_account.main.connection_strings[0]
    "DB_NAME"                             = "cosmos-db"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://index.docker.io"
    "FLASK_APP"                           = "todo_app/app"
    "FLASK_ENV"                           = var.env
    "SECRET_KEY"                          = var.secret_key
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                      = "${local.prefix}-cosmosdb-account"
  enable_automatic_failover = true
  kind                      = "MongoDB"
  location                  = data.azurerm_resource_group.main.location
  mongo_server_version      = 3.6
  offer_type                = "Standard"
  resource_group_name       = data.azurerm_resource_group.main.name

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level = "Strong"
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${local.prefix}-cosmosdb"
  account_name        = azurerm_cosmosdb_account.main.name
  resource_group_name = data.azurerm_resource_group.main.name

  lifecycle {
    prevent_destroy = true
  }
}
