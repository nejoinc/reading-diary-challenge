from datetime import datetime

class Note:
    def __init__(self, text: str, page: int, date: datetime):
        self.text: str = text
        self.page: int = page
        self.date: datetime = date

    def __str__(self) -> str:
        return f"{self.date} - page {self.page}: {self.text}"

class Book:
    EXCELLENT: int = 3
    GOOD: int = 2
    BAD: int = 1
    UNRATED: int = -1

    def __init__(self, isbn: str, title: str, author: str, pages: int):
        self.isbn: str = isbn
        self.title: str = title
        self.author: str = author
        self.pages: int = pages
        self.rating: int = Book.UNRATED
        self.notes: list[Note] = []

    def add_note(self, text: str, page: int, date: datetime) -> bool:
        if page > self.pages:
            return False
        else:
            self.notes.append(Note(text, page, date))
            return True

    def set_rating(self, rating: int) -> bool:
        if rating not in (self.EXCELLENT, self.GOOD, self.BAD):
            return False
        else:
            self.rating: int = rating
            return True

    def get_notes_of_page(self, page: int) -> list[Note]:
        notes_of_page: list[Note] = []

        for note in self.notes:
            if note.page == page:
                notes_of_page.append(note)

        return notes_of_page

    def page_with_most_notes(self) -> int:
        notes_of_page = {}

        for note in self.notes:
            if note.page not in notes_of_page:
                notes_of_page[note.page] = 1
            else:
                notes_of_page[note.page] += 1

        if not notes_of_page:
            return -1

        max_page = None
        max_count = -1

        for page, count in notes_of_page.items():
            if count > max_count:
                max_count = count
                max_page = page

        return max_page

    def __str__(self) -> str:
        texto = "unrated"
        if self.rating == self.EXCELLENT:
            texto = "excellent"
        elif self.rating == self.GOOD:
            texto = "good"
        elif self.rating == self.BAD:
            texto = "bad"
        elif self.rating == self.UNRATED:
            texto = "unrated"

        return f"ISBN: {self.isbn}\nTitle: {self.title}\nAuthor: {self.author}\nPages: {self.pages}\nRating: {texto}"








