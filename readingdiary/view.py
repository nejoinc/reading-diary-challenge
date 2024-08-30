import sys

from readingdiary.model import ReadingDiary


class UIConsole:
    
    ENTER_ISBN: str = 'Enter ISBN: '
    BOOK_NOT_FOUND: str = 'Book not found'
    
    def __init__(self):
        self.diary = ReadingDiary()
        self.options = {
            '1': self.add_book,
            '2': self.add_note,
            '3': self.rate_book,
            '4': self.search_book_by_isbn,
            '5': self.get_notes_of_page,
            '6': self.page_with_most_notes,
            '7': self.book_with_most_notes,
            '0': self.exit
        }
    
    def print_menu(self):
        print("====================================")
        print('Reading Diary App Menu')
        print('1. Add book')
        print('2. Add note')
        print('3. Rate book')
        print('4. Search book by ISBN')
        print('5. Get notes of page')
        print('6. Page with most notes')
        print('7. Book with most notes')
        print('0. Exit')
        print("====================================")
    
    def run(self):
        while True:
            self.print_menu()
            option = input('Enter option: ')
            action = self.options.get(option)
            if action:
                action()
            else:
                print('Invalid option')    
    
    def add_book(self):
        print(">>> Add book ========================")
        isbn = input(UIConsole.ENTER_ISBN)
        title = input('Enter title: ')
        author = input('Enter author: ')
        pages = int(input('Enter pages: '))
        if self.diary.add_book(isbn, title, author, pages):
            print('Book added successfully')
        else:
            print('Book already exists')
    
    def add_note(self):
        print(">>> Add note ========================")
        isbn = input(UIConsole.ENTER_ISBN)
        book = self.diary.search_by_isbn(isbn)
        if not book:
            print(UIConsole.BOOK_NOT_FOUND)
            return
        text = input('Enter text: ')
        page = int(input('Enter page: '))
        date = input('Enter date (YYYY-MM-DD): ')
        if book.add_note(text, page, date):
            print('Note added successfully')
        else:
            print('Invalid page')
        
    def rate_book(self):
        print(">>> Rate book ========================")
        isbn = input(UIConsole.ENTER_ISBN)
        book = self.diary.search_by_isbn(isbn)
        if not book:
            print(UIConsole.BOOK_NOT_FOUND)
            return
        rating = int(input('Enter rating (1-BAD, 2-GOOD, 3-EXCELLENT): '))
        if book.set_rating(rating):
            print('Book rated successfully')
        else:
            print('Invalid rating')
    
    def search_book_by_isbn(self):
        print(">>> Search book by ISBN ========================")
        isbn = input(UIConsole.ENTER_ISBN)
        book = self.diary.search_by_isbn(isbn)
        if book:
            print(book)
        else:
            print(UIConsole.BOOK_NOT_FOUND)
    
    def get_notes_of_page(self):
        print(">>> Get notes of page ========================")
        isbn = input(UIConsole.ENTER_ISBN)
        book = self.diary.search_by_isbn(isbn)
        if not book:
            print(UIConsole.BOOK_NOT_FOUND)
            return
        page = int(input('Enter page: '))
        notes = book.get_notes_of_page(page)
        if notes:
            for note in notes:
                print(note)
        else:
            print('No notes found')
    
    def page_with_most_notes(self):
        print(">>> Page with most notes ========================")
        isbn = input(UIConsole.ENTER_ISBN)
        book = self.diary.search_by_isbn(isbn)
        if not book:
            print(UIConsole.BOOK_NOT_FOUND)
            return
        print(f'Page with most notes: {book.page_with_most_notes()}')
    
    def book_with_most_notes(self):
        print(">>> Book with most notes ========================")
        book = self.diary.book_with_most_notes()
        print(book)
    
    def exit(self):
        print("\nGoodbye!")
        sys.exit(0)
