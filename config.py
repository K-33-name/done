import os

class Config:
    SECRET_KEY = "set_secret"

    if os.getenv("MYSQLHOST"):  
        # 🚀 Railway (production)
        DB_HOST = os.getenv("MYSQLHOST")
        DB_USER = os.getenv("MYSQLUSER")
        DB_PASSWORD = os.getenv("MYSQLPASSWORD")
        DB_NAME = os.getenv("MYSQLDATABASE")
        DB_PORT = int(os.getenv("MYSQLPORT", 3306))
    else:
        # 💻 Local (XAMPP)
        DB_HOST = "localhost"
        DB_USER = "root"
        DB_PASSWORD = ""   # default XAMPP
        DB_NAME = "setdb"
        DB_PORT = 3306