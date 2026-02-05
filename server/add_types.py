import psycopg2

conn = psycopg2.connect(
    user = "postgres",
    password = 'DPwFoJyRoiopsUTaTtonokmRuYmkOULL',
    host = "mainline.proxy.rlwy.net",
    port = 42637,
    database = "railway"
)
cursor = conn.cursor()

file = open('server/types.txt', 'r', encoding='UTF-8').read().splitlines()

for type in file:
    cursor.execute(
        "INSERT INTO element_types (title, description) VALUES (%s, %s)",
        (f"{type}", "none")
    )
conn.commit()
