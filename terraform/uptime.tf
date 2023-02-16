# when setting up access restrictions, make sure to allow the ApplicationInsightsAvailability service tag
module "healthcheck" {
  source = "./uptime"

  action_group_id      = azurerm_monitor_action_group.eng_email.id
  application_insights = azurerm_application_insights.main
  # not strictly necessary to include the environment name, but helps to make the alerts more clear
  name = "mst-courtesy-cards-eligibility-server-${local.env_name}-healthcheck"
  url  = "https://${azurerm_linux_web_app.main.default_hostname}/healthcheck"
}

# ignore when app restarts as data is being reloaded
# https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-processing-rules
resource "azurerm_monitor_action_rule_suppression" "suppression" {
  name                = "ignore-data-loading"
  resource_group_name = data.azurerm_resource_group.main.name

  scope {
    type         = "Resource"
    resource_ids = [module.healthcheck.metric_alert_id]

  }

  suppression {
    recurrence_type = "Daily"

    schedule {
      start_date_utc = "2020-01-01T00:00:00Z"
      end_date_utc   = "2050-01-01T00:00:00Z"
      start_time_utc = "11:00AM"
      end_time_utc   = "11:10AM"
    }
  }
}
