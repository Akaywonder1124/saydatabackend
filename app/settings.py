# DATABASE_USER = os.environ.get("DATABASE_USER")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

DATABASE_USER = "admin"
DATABASE_PASSWORD = "Olayemi04"

DATABASE_URL = (
    f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:5432/saydatadb"
)
