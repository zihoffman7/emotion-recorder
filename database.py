from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector, time
from json import dumps

forms = {
    "general-level": "General mood",
    "agitation-level": "Agitation",
    "anger-level": "Anger",
    "anxious-level": "Anxiousness",
    "confidence-level": "Confidence",
    "depression-level": "Depression",
    "joy-level": "Joy",
    "melancholic-level": "Melancholic",
    "motivation-level": "Motivation",
    "optimism-level": "Optimism",
    "selfworth-level": "Self-worth"
}

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="chart",
    auth_plugin="mysql_native_password",
    charset="utf8mb4"
)

cursor = db.cursor(buffered=True)

with open("schema.sql") as f:
    sql = f.read()
cursor.execute(sql, multi=True)
db.commit()

def create_account(username, password):
    if not account_name_exists(username):
        cursor.execute("INSERT INTO users VALUES (%s, %s)", (username, generate_password_hash(password)))
        db.commit()
        return True
    return False

def account_name_exists(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
    if cursor.fetchone():
        return True
    return False

def account_credentials_exist(username, password):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
    user = cursor.fetchone()
    if user:
        if check_password_hash(user[1], password):
            return True
    return False

def log_form(username, category, value, time):
    cursor.execute("INSERT INTO logs VALUES (%s, %s, %s, %s)", (username, category, value, time))
    db.commit()

def retrieve_logs(username, start_date=0, end_date=2147483647):
    cursor.execute(f"SELECT * FROM logs WHERE username = '{username}' AND _time BETWEEN {start_date} AND {end_date};")
    return cursor.fetchall()

def format_logs(logs):
    summary, general = {}, {}
    count = 0
    for i in logs:
        if i[1] in forms.keys() and i[1] != "general-level":
            if i[1].split("-")[0].capitalize() in summary.keys():
                summary[forms[i[1]]] += int(i[2]) - 1
            else:
                summary[forms[i[1]]] = int(i[2]) - 1
        elif i[1] == "general-level":
            if forms["general-level"] in general:
                general[forms["general-level"]] += int(i[2])
            else:
                general[forms["general-level"]] = int(i[2])
            count += 1
    return dumps(summary), count, general

def earliest_log(username):
    cursor.execute(f"SELECT _time FROM logs WHERE username = '{username}'")
    return min([i[0] for i in cursor.fetchall()])

def clear_logs(username):
    cursor.execute(f"DELETE FROM logs WHERE username = '{username}'")
    db.commit()
