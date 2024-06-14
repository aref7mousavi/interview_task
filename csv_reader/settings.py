from backend.default_settings import *

AGWEB_URL = os.environ.get("AGWEB_URL", config("AGWEB_URL", ''))