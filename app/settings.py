# DATABASE_USER = os.environ.get("DATABASE_USER")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

# this is a free postgreSQL database,
#  for the sake of this quick project, I didn,t save the login in an enviroment project
DATABASE_USER = "zhkojnfg"
DATABASE_PASSWORD = "mDkMdVxhChPNsNYDcIZX_jPCLLkdsPGg"

DATABASE_URL = (
    f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@mahmud.db.elephantsql.com/zhkojnfg"
)
