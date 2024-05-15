import tkinter as tk
from tkinter import messagebox
import grpc
import wishlist_pb2
import wishlist_pb2_grpc

class WishlistClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:8080')
        self.stub = wishlist_pb2_grpc.WishlistStub(self.channel)

    def add_film(self, title, director, year):
        try:
            film = wishlist_pb2.Film(title=title, director=director, year=int(year))
            response = self.stub.AddFilm(wishlist_pb2.AddFilmRequest(film=film))
            messagebox.showinfo("Success", f"Film added with ID: {response.id}")
        except grpc.RpcError as e:
            messagebox.showerror("Error", f"Failed to add film: {e.details()}")

    def get_film_by_title(self, title):
        try:
            response = self.stub.GetFilmByTitle(wishlist_pb2.GetFilmByTitleRequest(title=title))
            return response
        except grpc.RpcError as e:
            messagebox.showerror("Error", f"Failed to get film: {e.details()}")
            return None

    def update_film(self, title, director, year):
        try:
            film = wishlist_pb2.Film(title=title, director=director, year=int(year))
            self.stub.UpdateFilm(wishlist_pb2.UpdateFilmRequest(film=film))
            messagebox.showinfo("Success", "Film updated successfully")
        except grpc.RpcError as e:
            messagebox.showerror("Error", f"Failed to update film: {e.details()}")

    def delete_film_by_title(self, title):
        try:
            self.stub.DeleteFilmByTitle(wishlist_pb2.DeleteFilmByTitleRequest(title=title))
            messagebox.showinfo("Success", "Film deleted successfully")
        except grpc.RpcError as e:
            messagebox.showerror("Error", f"Failed to delete film: {e.details()}")

    def get_all_films(self):
        try:
            films = []
            for film in self.stub.GetAllFilms(wishlist_pb2.GetAllFilmsRequest()):
                films.append(film)
            return films
        except grpc.RpcError as e:
            messagebox.showerror("Error", f"Failed to get all films: {e.details()}")
            return []

def show_add_page():
    add_page = tk.Toplevel(root)
    add_page.title("Add Film")

    title_label = tk.Label(add_page, text="Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    title_entry = tk.Entry(add_page)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    director_label = tk.Label(add_page, text="Director:")
    director_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    director_entry = tk.Entry(add_page)
    director_entry.grid(row=1, column=1, padx=5, pady=5)

    year_label = tk.Label(add_page, text="Year:")
    year_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    year_entry = tk.Entry(add_page)
    year_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = tk.Button(add_page, text="Add Film", command=lambda: client.add_film(title_entry.get(), director_entry.get(), year_entry.get()))
    add_button.grid(row=3, column=0, columnspan=2, pady=5)

def show_search_page():
    search_page = tk.Toplevel(root)
    search_page.title("Search Film")

    search_label = tk.Label(search_page, text="Enter film title:")
    search_label.pack(pady=5)

    search_entry = tk.Entry(search_page)
    search_entry.pack(pady=5)

    search_button = tk.Button(search_page, text="Search", command=lambda: handle_search(search_entry.get()))
    search_button.pack(pady=5)

def handle_search(title):
    response = client.get_film_by_title(title)
    if response and response.id:
        messagebox.showinfo("Film Details", f"Title: {response.title}\nDirector: {response.director}\nYear: {response.year}")
    else:
        messagebox.showerror("Error", "Film not found")

client = WishlistClient()

root = tk.Tk()
root.title("gRPC Wishlist Client")

# Deklarasi variabel untuk halaman "Update Film"
update_title = tk.StringVar(root)
update_director = tk.StringVar(root)
update_year = tk.StringVar(root)

def show_update_page():
    update_page = tk.Toplevel(root)
    update_page.title("Update Film")

    search_frame = tk.Frame(update_page)
    search_frame.pack(pady=10)

    search_label = tk.Label(search_frame, text="Enter film title:")
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_film(search_entry.get(), update_page))
    search_button.pack(side=tk.LEFT, padx=5)

    update_frame = tk.Frame(update_page)
    update_frame.pack(pady=10)

    update_title_label = tk.Label(update_frame, text="Title:")
    update_title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    update_title_entry = tk.Entry(update_frame, textvariable=update_title)
    update_title_entry.grid(row=0, column=1, padx=5, pady=5)

    update_director_label = tk.Label(update_frame, text="Director:")
    update_director_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    update_director_entry = tk.Entry(update_frame, textvariable=update_director)
    update_director_entry.grid(row=1, column=1, padx=5, pady=5)

    update_year_label = tk.Label(update_frame, text="Year:")
    update_year_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    update_year_entry = tk.Entry(update_frame, textvariable=update_year)
    update_year_entry.grid(row=2, column=1, padx=5, pady=5)

    update_button = tk.Button(update_frame, text="Update Film", command=lambda: update_film(update_title.get(), update_director.get(), update_year.get()))
    update_button.grid(row=3, column=0, columnspan=2, pady=5)

def search_film(title, update_page):
    response = client.get_film_by_title(title)
    if response and response.id:
        update_title.set(response.title)
        update_director.set(response.director)
        update_year.set(response.year)
    else:
        messagebox.showerror("Error", "Film not found")

def update_film(new_title, new_director, new_year):
    client.update_film(new_title, new_director, new_year)

def show_delete_page():
    delete_page = tk.Toplevel(root)
    delete_page.title("Delete Film")

    delete_label = tk.Label(delete_page, text="Enter film title:")
    delete_label.pack(pady=5)

    delete_entry = tk.Entry(delete_page)
    delete_entry.pack(pady=5)

    delete_button = tk.Button(delete_page, text="Delete Film", command=lambda: client.delete_film_by_title(delete_entry.get()))
    delete_button.pack(pady=5)

def show_all_films_page():
    all_films_page = tk.Toplevel(root)
    all_films_page.title("All Films")

    films = client.get_all_films()

    if films:
        for film in films:
            film_label = tk.Label(all_films_page, text=f"ID: {film.id}, Title: {film.title}, Director: {film.director}, Year: {film.year}")
            film_label.pack(pady=2)
    else:
        no_film_label = tk.Label(all_films_page, text="No films available.")
        no_film_label.pack(pady=5)

add_button = tk.Button(root, text="Add Film", command=show_add_page)
add_button.pack(pady=5)

search_button = tk.Button(root, text="Search Film", command=show_search_page)
search_button.pack(pady=5)

update_button = tk.Button(root, text="Update Film", command=show_update_page)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Film", command=show_delete_page)
delete_button.pack(pady=5)

all_films_button = tk.Button(root, text="All Films", command=show_all_films_page)
all_films_button.pack(pady=5)

root.mainloop()
