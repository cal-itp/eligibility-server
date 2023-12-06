# when setting up access restrictions, make sure to allow the ApplicationInsightsAvailability service tag
module "healthcheck" {
  source = "./uptime"

  action_group_id      = azurerm_monitor_action_group.eng_email.id
  application_insights = azurerm_application_insights.main
  # not strictly necessary to include the environment name, but helps to make the alerts more clear
  name = "${var.AGENCY_CARD}-eligibility-server-${local.env_name}-healthcheck"
  url  = "https://${azurerm_cdn_frontdoor_endpoint.main.host_name}/healthcheck"
}

# ignore when app restarts as data is being reloaded
# https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-processing-rules
resource "azurerm_monitor_alert_processing_rule_suppression" "suppress_nightly_downtime" {
  name                = "suppress-nightly-downtime"
  description         = "Suppresses alerts during the scheduled nightly downtime"
  resource_group_name = data.azurerm_resource_group.main.name
  scopes              = [module.healthcheck.metric_alert_id]
  schedule {
    time_zone = "Pacific Standard Time"
    recurrence {
      daily {
        start_time = "02:55:00"
        end_time   = "03:30:00"
      }
    }
  }
}
