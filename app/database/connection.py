# import cx_Oracle
import oracledb
# from .models.user import User, UserInDB

oracle_config = {
    "host": "54.38.215.111",
    "port": 1521,
    "service_name": "cirrus",
    "user": "cirrus",
    "password": "Cir^Pnq$6A",
}

def create_connection():
    connection = oracledb.connect(
        user=oracle_config["user"],
        password=oracle_config["password"],
        dsn=f"{oracle_config['host']}:{oracle_config['port']}/{oracle_config['service_name']}",
    )
    return connection

# oracle_dsn = cx_Oracle.makedsn(
#     host="54.38.215.111",
#     port=1521,
#     service_name="cirrus",
# )

# oracle_connection = cx_Oracle.connect(
#     user="cirrus",
#     password="Cir^Pnq$6A",
#     dsn=oracle_dsn,
#     encoding="UTF-8"
# )
# cursor = oracle_connection.cursor()

# def get_user(username: str):
#     cursor.execute("SELECT * FROM users WHERE username = :1", (username,))
#     user_data = cursor.fetchone()
#     if user_data:
#         return UserInDB(**dict(user_data))

# def create_user(user: User):
#     hashed_password = hash_password(user.password)
#     cursor.execute(
#         "INSERT INTO users (username, email, hashed_password) VALUES (:1, :2, :3)",
#         (user.username, user.email, hashed_password),
#     )
#     oracle_connection.commit()
#     return UserInDB(**user.dict(), hashed_password=hashed_password)
