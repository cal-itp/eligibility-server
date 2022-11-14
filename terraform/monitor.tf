resource "azurerm_log_analytics_workspace" "main" {
  name                = "eligibility-server"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
}


resource "azurerm_application_insights" "main" {
  name                = "eligibility-server"
  application_type    = "web"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  sampling_percentage = 0
  workspace_id        = azurerm_log_analytics_workspace.main.id
}

# created manually
# https://slack.com/help/articles/206819278-Send-emails-to-Slack
data "azurerm_key_vault_secret" "slack_benefits_notify_email" {
  name         = "slack-benefits-notify-email"
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_monitor_action_group" "eng_email" {
  name                = "benefits-notify Slack channel email"
  resource_group_name = data.azurerm_resource_group.main.name
  short_name          = "slack-notify"

  email_receiver {
    name          = "Benefits engineering team"
    email_address = data.azurerm_key_vault_secret.slack_benefits_notify_email.value
  }
}
