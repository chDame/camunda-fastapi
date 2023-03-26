from pydantic import BaseSettings

class Settings(BaseSettings):
    """Service settings."""
    cluster_id: str
    client_id: str
    client_secret: str

    class Config:
        """Meta configuration"""
        env_file = ".env"