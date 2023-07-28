#!/path/to/python/interpreter
import psycopg2

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="host",
        port="port",
        database="database",
        user="username",
        password="password"
    )
    stmt = "UPDATE afiliaciones_afiliacion SET facturado = false;"
    cursor = conn.cursor()
    cursor.execute(stmt)
    conn.commit()