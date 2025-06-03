import psycopg2

class ConexionBD:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def conectar(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print("Error al conectar a la base de datos:", e)

    def cerrar(self):
        if self.conn:
            self.conn.close()
            print("Conexión cerrada.")

    def obtener_cursor(self):
        if self.conn:
            return self.conn.cursor()
        else:
            print("No hay conexión activa.")
            return None