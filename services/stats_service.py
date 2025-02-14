from .api_service import ApiService as api


class StatsService:

    @classmethod
    def get_users(cls):
        return api.get(endpoint='users')
