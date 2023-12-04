from error_handling import NotExist, TooManyBook
import json
from datetime import date, timedelta, datetime
from read_write import read_data, write_data

File_NAME = "borrow.json"


def update_file(isbn, member_id, borrow=False):
    jsn = read_data(File_NAME)

    """
        {
            member_id : [
                    {
                        isbn: {
                            'date': date
                            'due': date
                        }
                    }
            ]
        }
    
        """

    if member_id in jsn:
        flag = False

        qty = jsn[member_id]
        print(jsn)

        if borrow and len(qty) >= 3:
            raise Exception("Too Many Book Borrowed! ")

        for x in jsn[member_id]:
            if isbn in x:
                flag = True
                if borrow:
                    print("Cannot take same book")
                    return 0
                else:
                    due = datetime.strptime(x[isbn]["due"], "%y%m%d")

                    if due > date.today():
                        print("No Fine")
                    else:
                        extra_days = (date.today() - x["due"]).days
                        fine = extra_days * 10
                        print(f"Please pay a fine of {fine}")

                    jsn[member_id].remove(x)
                    write_data(jsn, File_NAME)
                    return 1

        if borrow and not flag:
            jsn[member_id].append(
                {
                    isbn: {
                        "date": str(date.today()),
                        "due": str(date.today() + timedelta(days=15)),
                    }
                }
            )
            write_data(jsn, File_NAME)
            return 1

        else:
            raise Exception("Doesn't exist!")

    else:
        if borrow:
            jsn[member_id] = []
            jsn[member_id].append(
                {
                    isbn: {
                        "date": str(date.today()),
                        "due": str(date.today() + timedelta(days=15)),
                    }
                }
            )
            write_data(jsn, File_NAME)
            return 1

        else:
            raise Exception("Doesn't Exist!")


def borrow(Book, library, member_id, isbn):
    if member_id not in library.members_list and isbn not in Book.book_inventory:
        raise Exception("Doesn't Exist!")

    res = update_file(isbn, member_id, borrow=True)

    if res:
        if Book.book_inventory[isbn]["quantity"] > 0:
            Book.book_inventory[isbn]["quantity"] -= 1
            write_data(Book.book_inventory, "books.json")

        else:
            raise Exception("Book out of stock!")
    else:
        raise Exception("Failed to borrow book!")


def return_bk(Book, library, member_id, isbn):
    if member_id not in library.members_list and isbn not in Book.book_inventory:
        raise Exception("Doesn't Exist!")

    res = update_file(isbn, member_id, borrow=False)

    if res:
        Book.book_inventory[isbn]["quantity"] += 1
        write_data(Book.book_inventory, "books.json")

    else:
        raise Exception("Failed to return book!")
