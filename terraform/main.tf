provider "azurerm" {
  features {}
}

# Création d'un groupe de ressources
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "France Central"
}

# Création d'un serveur SQL Azure
resource "azurerm_sql_server" "example" {
  name                         = "example-sqlserver"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234!"

  tags = {
    environment = "production"
  }
}

# Création d'une base de données SQL Azure dans le modèle Serverless
resource "azurerm_sql_database" "example" {
  name                = "example-sqldb"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  server_name         = azurerm_sql_server.example.name

  sku_name = "GP_S_Gen5_1"
  auto_pause_delay_in_minutes = 60 # Pause automatique après inactivité (min 60 minutes pour Serverless)
  min_capacity                = 0.5 # Capacité minimale en vCores (dépend du niveau de service et de la génération)

  tags = {
    environment = "production"
  }
}
