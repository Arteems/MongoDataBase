from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Желательно вместо str использовать SecretStr
    # для конфиденциальных данных, например, токена бота
    token: SecretStr
    BASE_URL: str = "http://localhost:8000"
    BASE_CODEWARS_URL: str = "https://www.codewars.com/api/v1/users"
    MONGO_URL: str = "mongodb://localhost:27017/"

    # Начиная со второй версии pydantic, настройки класса настроек задаются
    # через model_config
    # В данном случае будет использоваться файла .env, который будет прочитан
    # с кодировкой UTF-8
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# При импорте файла сразу создастся
# и провалидируется объект конфига,
# который можно далее импортировать из разных мест
settings = Settings()
