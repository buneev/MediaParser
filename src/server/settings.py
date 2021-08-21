import os

APM_ENABLED = bool(int(os.getenv("ELASTIC_APM_ENABLED", 0)))
