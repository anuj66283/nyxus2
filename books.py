from error_handling import AlreadyExists
from read_write import read_data, write_data, create_unique

FILE_NAME = 'books.json'

class Book:
    book_inventory = read_data(FILE_NAME)

    @classmethod
    def add_book(cls, title, author, genre, quantity):
        if not cls.book_inventory:
            cls.book_inventory = read_data(FILE_NAME)

        isbn = create_unique(title, author, genre)

        if isbn in cls.book_inventory:
            raise AlreadyExists

        rslt = {
            'title': title,
            'author': author,
            'genre': genre,
            'quantity': quantity
        }

        cls.book_inventory[isbn] = rslt

        write_data(cls.book_inventory, FILE_NAME)

        print("Added successfully")