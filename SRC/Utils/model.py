from pydantic_settings import BaseSettings ,SettingsConfigDict
class Setting(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    db_url:str
    app_pass:str
    api_key:str
    redis_url:str
    SMTP_Server:str
    Port:int
    Login:str
    smtp_key:str
setting=Setting()