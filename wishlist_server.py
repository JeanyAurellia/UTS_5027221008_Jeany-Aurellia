import grpc
import wishlist_pb2
import wishlist_pb2_grpc
import mysql.connector
from concurrent import futures

class WishlistServicer(wishlist_pb2_grpc.WishlistServicer):
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            database="wishlist_db"
        )

    def AddFilm(self, request, context):
        cursor = self.db.cursor()
        try:
            query = "INSERT INTO films (title, director, year) VALUES (%s, %s, %s)"
            values = (request.film.title, request.film.director, request.film.year)
            cursor.execute(query, values)
            self.db.commit()
            film_id = cursor.lastrowid
            cursor.close()
            return wishlist_pb2.Film(id=film_id, title=request.film.title, director=request.film.director, year=request.film.year)
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return wishlist_pb2.Film()

    def GetFilmByTitle(self, request, context):
        cursor = self.db.cursor()
        try:
            query = "SELECT id, title, director, year FROM films WHERE title = %s"
            cursor.execute(query, (request.title,))
            film_data = cursor.fetchone()
            cursor.close()
            if film_data:
                return wishlist_pb2.Film(id=film_data[0], title=film_data[1], director=film_data[2], year=film_data[3])
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Film not found")
                return wishlist_pb2.Film()
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return wishlist_pb2.Film()

    def GetAllFilms(self, request, context):
        cursor = self.db.cursor()
        try:
            query = "SELECT id, title, director, year FROM films"
            cursor.execute(query)
            for film_data in cursor.fetchall():
                yield wishlist_pb2.Film(id=film_data[0], title=film_data[1], director=film_data[2], year=film_data[3])
            cursor.close()
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")

    def UpdateFilm(self, request, context):
        cursor = self.db.cursor()
        try:
            query = "UPDATE films SET director = %s, year = %s WHERE title = %s"
            values = (request.film.director, request.film.year, request.film.title)
            cursor.execute(query, values)
            self.db.commit()
            cursor.close()
            return wishlist_pb2.Empty()
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return wishlist_pb2.Empty()

    def DeleteFilmByTitle(self, request, context):
        cursor = self.db.cursor()
        try:
            query = "DELETE FROM films WHERE title = %s"
            cursor.execute(query, (request.title,))
            self.db.commit()
            cursor.close()
            return wishlist_pb2.Empty()
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return wishlist_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wishlist_pb2_grpc.add_WishlistServicer_to_server(WishlistServicer(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    print("Server gRPC berjalan pada port 8080")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
