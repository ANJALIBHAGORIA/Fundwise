import os
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgres://user:pass@localhost:5432/fundwise")
