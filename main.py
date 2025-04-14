from pyconfparser import ConfigFactory

from src.app.streamlit_app import StreamlitApp
from src.service.meetings_service import MeetingsService

if __name__ == "__main__":
    config = ConfigFactory.get_conf(r"notebooks/conf/config.json")
    service: MeetingsService = MeetingsService(
        gemini_api_secret=config.gemini_api_key, model_type=config.model_type, prompt=config.prompt
    )
    app = StreamlitApp(service=service)
    app.run()
