from project_name.api.health_check import PingResource

urls = (
    ('/health/ping', PingResource),
)
