import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='12345678',
        host='127.0.0.1'
    )
    print('connect success')

    cursor = conn.cursor()

    sql = 'select * from rent'
    cursor.execute(sql)

    print(cursor.fetchall())

    cursor.close()
    conn.close()
except:
    print('Can`t establish connection to database')