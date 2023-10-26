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
# the Terraform resource doesn't support time windows, so need to drop down to an ARM template instead
# https://github.com/hashicorp/terraform-provider-azurerm/issues/16726
resource "azurerm_resource_group_template_deployment" "suppress_nightly_downtime" {
  name                = "suppress-nightly-downtime"
  resource_group_name = data.azurerm_resource_group.main.name
  deployment_mode     = "Incremental"
  parameters_content = jsonencode({
    "metricAlertID" = {
      value = module.healthcheck.metric_alert_id
    }
  })
  # https://learn.microsoft.com/en-us/azure/templates/microsoft.alertsmanagement/actionrules?tabs=json&pivots=deployment-language-arm-template
  template_content = file("${path.module}/suppress.arm.json")
}
