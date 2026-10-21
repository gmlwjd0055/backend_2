#서버의 환경 설정 파일 : DB 접속 주소, 토큰 시크릿 등 환경변수로 설정된 값 불러오는 파일

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    #env 파일이 없을 때 사용하는 기본 key 값(실제x)
    SECRET_KEY: str = "dslfjgkreobdgsregwdsbcxbilcjxkesfarglrwhkedkgsj"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///db.sqlite3"
    KAKAO_REST_API_KEY: str = ""
    KAKAO_CLIENT_SECRET: str = ""
    #KAKAO_REDIRECT_URI: str = "http://localhost:5173/login/kakao/callback"
    KAKAO_REDIRECT_URI: str = "http://www.hhon.kro.kr/login/kakao/callback"
    AUTH_COOKIE_DOMAIN: str | None = "hhon.kro.kr"
    PORTONE_API_SECRET: str = ""
    PORTONE_STORE_ID: str = ""
    PORTONE_CHANNEL_KEY: str = ""
    PORTONE_API_BASE_URL: str = "https://api.portone.io"

settings = Settings()
