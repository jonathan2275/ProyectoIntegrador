import mysql.connector

# Este se ejecuta aqui mismo


class baseDatos:

    def __init__ (self):
        self.conn = mysql.connector.connect(db="proyectoi",
                        user="root123@mysqlproyecto",
                        host="mysqlproyecto.mysql.database.azure.com",
                        passwd="jonathan123@",
                        port=3306)
        self.cur = self.conn.cursor()

    def consulta(self,sql):
        self.cur.execute(sql)
        row = self.cur.fetchall()
        return row

    def insertar(self, sql):
        self.cur.execute(sql)
        self.conn.commit()



    def cerrar(self):
        self.conn.close()
