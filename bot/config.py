import os

_REQUIRED_FIELDS = [
    "TELEGRAM_API_ID",
    "TELEGRAM_API_HASH",
    "TELEGRAM_BOT_TOKEN",
    "VPRW_API_KEY",
    "VPRW_API_ENDPOINT",
    "BOT_CONTACT_USERNAME",
    "SENTRY_DSN",
    "DEPLOYMENT_ENVIRONMENT",
]


class Config:
    def __init__(self) -> None:
        self.__check_env_vars()

    @staticmethod
    def __check_env_vars():
        for field in _REQUIRED_FIELDS:
            if field not in os.environ:
                msg = f"Environment variable {field} is not set"
                raise ValueError(msg)

    @staticmethod
    def __get_env_var(name: str) -> str:
        if name not in os.environ:
            msg = f"Environment variable {name} is not set"
            raise ValueError(msg)
        return os.environ[name]

    def get_telegram_api_id(self) -> str:
        return self.__get_env_var("TELEGRAM_API_ID")

    def get_telegram_api_hash(self) -> str:
        return self.__get_env_var("TELEGRAM_API_HASH")

    def get_telegram_bot_token(self) -> str:
        return self.__get_env_var("TELEGRAM_BOT_TOKEN")

    def get_vprw_api_key(self) -> str:
        return self.__get_env_var("VPRW_API_KEY")

    def get_vprw_api_endpoint(self) -> str:
        return self.__get_env_var("VPRW_API_ENDPOINT")

    def get_bot_contact_username(self) -> str:
        return self.__get_env_var("BOT_CONTACT_USERNAME")

    def get_sentry_dsn(self) -> str:
        return self.__get_env_var("SENTRY_DSN")

    def get_deployment_release(self) -> str:
        with open("VERSION") as f:
            return f.read().strip()

    def get_deployment_environment(self) -> str:
        return self.__get_env_var("DEPLOYMENT_ENVIRONMENT")
