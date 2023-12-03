import json

def display_book_inventory(book):
    for x in book.book_inventory:
        print(f'isbn: {x} name: {book.book_inventory[x]["title"]} quantity: {book.book_inventory[x]["quantity"]}')
    
def members_reports():
    with open('members.json', 'r') as f:
        jsn = json.load(f)
    
    for x in jsn:
        print(f'id: {x} name: {jsn[x]["name"]} phone: {jsn[x]["phone"]}')