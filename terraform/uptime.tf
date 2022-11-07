module "healthcheck" {
  source = "./uptime"

  action_group_id      = azurerm_monitor_action_group.eng_email.id
  application_insights = azurerm_application_insights.main
  # not strictly necessary to include the environment name, but helps to make the alerts more clear
  name = "mst-courtesy-cards-eligibility-server-${local.env_name}-healthcheck"
  url  = "https://${azurerm_linux_web_app.main.default_hostname}/healthcheck"
}
