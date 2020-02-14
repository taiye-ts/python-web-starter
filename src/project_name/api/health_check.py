from falcon import Request, Response
from project_name.domain.health_check_service import HealthCheckService


class HealthCheckResource:

    def __init__(self):
        self.service = HealthCheckService()

    def on_get(self, request: Request, response: Response):
        status = self.service.get_status()
        response.media = status.to_dict()
