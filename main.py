import books as bm
import borrow_return as br
import members as mm
import report as rg


def help():
    print(
        "\t1) add book\n\t2) add member\n\t3) view books\n\t4) borrow\n\t5) return\n\t6) view members\n\t7) help\n\t8) exit"
    )


bk = bm.Book()
lm = mm.LibraryMember()

while True:
    try:
        choice = int(input("Enter your command: "))

        if choice == 1:
            title = input("Enter title: ")
            quantity = int(input("Enter quantity: "))
            author = input("Enter author: ")
            genre = input("Enter genre: ")

            bk.add_book(title, author, genre, quantity)

        elif choice == 2:
            phone = input("Enter phone number: ")
            name = input("Enter member name: ")
            district = input("Enter district: ")

            lm.add_member(name, phone, district)

        elif choice == 3:
            rg.display_book_inventory(bk)

        elif choice == 4:
            member_id = input("Enter member id: ")
            isbn = input("Enter isbn: ")

            br.borrow(bk, lm, member_id, isbn)

        elif choice == 5:
            member_id = input("Enter member id: ")
            isbn = input("Enter isbn: ")
            br.return_bk(bk, lm, member_id, isbn)

        elif choice == 6:
            rg.members_reports()

        elif choice == 7:
            help()

        elif choice == 8:
            break

        else:
            print("Invalid command")
            continue
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
