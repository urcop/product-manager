from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
DB_NAME = env.str("DB_NAME")
DB_PORT = env.str("DB_PORT")
DB_PASS = env.str("DB_PASS")
