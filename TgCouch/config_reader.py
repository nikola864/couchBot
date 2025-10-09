from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: int

    class Config:
        env_prefix = ""

config = Settings()




#from pydantic_settings import SettingsConfigDict, BaseSettings
#from pydantic import SecretStr
#import os

#class Settings(BaseSettings):
#   bot_token: SecretStr
#    admin_id: int

#    model_config = SettingsConfigDict(
#        env_file=os.path.join(os.path.dirname(__file__), '.env'),  # <-- указывает путь к .env в той же папке, где config_reader.py
#        env_file_encoding='utf-8'
#    )

#config = Settings()