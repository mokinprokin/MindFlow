import json
import keyring
import logging
from src.config import settings
from ..schemas.token import TokenBase
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from keyring.errors import PasswordDeleteError
from google.auth.transport.requests import Request


logger = logging.getLogger(__name__)


class TokenService:
    SERVICE_NAME = "my_tracking_app"
    TOKEN_KEY = "google_token"

    @classmethod
    def get_credentials(cls) -> TokenBase:
        raw_token = keyring.get_password(cls.SERVICE_NAME, cls.TOKEN_KEY)

        if not raw_token:
            logger.info("Токен не найден. Запуск авторизации...")
            raw_token = cls._generate_and_store_tokens()

        try:
            creds = Credentials.from_authorized_user_info(
                json.loads(raw_token), settings.SCOPES
            )
            if creds.expired and creds.refresh_token:
                logger.info("Срок действия токена истек. Обновление...")
                creds.refresh(Request())
                keyring.set_password(cls.SERVICE_NAME, cls.TOKEN_KEY, creds.to_json())

            return TokenBase.model_validate_json(creds.to_json())

        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Ошибка при обработке токена: {e}. Сброс авторизации.")
            cls.delete_credentials()
            return cls.get_credentials()

    @classmethod
    def _generate_and_store_tokens(cls) -> str:
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": settings.CLIENT_ID,
                    "client_secret": settings.CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": settings.TOKEN_URI,
                }
            },
            scopes=settings.SCOPES,
        )

        creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
        token_json = creds.to_json()
        keyring.set_password(cls.SERVICE_NAME, cls.TOKEN_KEY, token_json)
        return token_json

    @classmethod
    def delete_credentials(cls):
        try:
            keyring.delete_password(cls.SERVICE_NAME, cls.TOKEN_KEY)
            logger.info(
                f"Ключ '{cls.SERVICE_NAME}' успешно удален из системного хранилища."
            )
        except PasswordDeleteError:
            logger.warning(f"Ключ '{cls.SERVICE_NAME}' не найден или уже удален.")

    @classmethod
    def get_google_credentials(cls) -> dict:
        token_data = cls.get_credentials()
        return {
            "user_creds": {
                "access_token": token_data.token,
                "refresh_token": token_data.refresh_token,
            },
            "client_creds": {
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
                "scopes": settings.SCOPES,
            },
        }
