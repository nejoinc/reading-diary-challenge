import unittest
from datetime import datetime
import inspect

import readingdiary.model

module_members = [member[0] for member in inspect.getmembers(readingdiary.model)]
note_defined = 'Note' in module_members
book_defined = 'Book' in module_members
reading_diary_defined = 'ReadingDiary' in module_members

if note_defined:
    from readingdiary.model import Note

if book_defined:
    from readingdiary.model import Book

if reading_diary_defined:
    from readingdiary.model import ReadingDiary

class TestModel(unittest.TestCase):

    def setUp(self):
        if note_defined:
            self.note = Note("This is a note", 1, datetime(2021, 1, 1))
        if book_defined:
            self.book_without_notes = Book("1234", "Test Book", "Author X", 100)
            self.book_with_notes = Book("1234", "Test Book", "Author X", 100)
            self.book_with_notes.add_note("Note 1", 1, datetime(2021, 1, 1))
            self.book_with_notes.add_note("Note 2", 2, datetime(2021, 1, 2))
            self.book_with_notes.add_note("Note 3", 1, datetime(2021, 1, 3))
        if reading_diary_defined:
            self.empty_diary = ReadingDiary()
            self.diary_with_books = ReadingDiary()
            self.diary_with_books.add_book("1234", "Test Book", "Author X", 100)
            self.diary_with_books.add_book("5678", "Another Book", "Author Y", 200)

    @unittest.skipUnless(note_defined, "Note class not defined")
    def test_class_note_has_attribute(self):
        for attr_name, attr_type in [("text", str), ("page", int), ("date", datetime)]:
            with self.subTest(attr_name=attr_name):
                self.assertTrue(hasattr(self.note, attr_name))
                self.assertIsInstance(getattr(self.note, attr_name), attr_type)

    @unittest.skipUnless(note_defined, "Note class not defined")
    def test_note_class_initializes_attributes(self):
        for text, page, date in [("This is a note", 1, datetime(2021, 1, 1)), ("Another note", 2, datetime(2021, 1, 2))]:
            with self.subTest(text=text, page=page, date=date):
                note = Note(text, page, date)
                self.assertEqual(note.text, text)
                self.assertEqual(note.page, page)
                self.assertEqual(note.date, date)

    @unittest.skipUnless(note_defined, "Note class not defined")
    def test_note_class_str_method(self):
        self.assertEqual(str(self.note), "2021-01-01 00:00:00 - page 1: This is a note")

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_book_class_has_constants(self):
        for const_name, const_value in [("EXCELLENT", 3), ("GOOD", 2), ("BAD", 1), ("UNRATED", -1)]:
            with self.subTest(const_name=const_name):
                self.assertTrue(hasattr(Book, const_name))
                self.assertEqual(getattr(Book, const_name), const_value)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_has_attributes(self):
        for attr_name, attr_type in [("isbn", str), ("title", str), ("author", str), ("pages", int), ("rating", int), ("notes", list)]:
            with self.subTest(attr_name=attr_name):
                self.assertTrue(hasattr(self.book_without_notes, attr_name))
                self.assertIsInstance(getattr(self.book_without_notes, attr_name), attr_type)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_book_class_initializes_attributes(self):
        for isbn, title, author, pages in [("1234", "Test Book", "Author X", 100), ("5678", "Another Book", "Author Y", 200), ("9012", "Third Book", "Author Z", 300)]:
            with self.subTest(isbn=isbn, title=title, author=author, pages=pages):
                book = Book(isbn, title, author, pages)
                self.assertEqual(book.isbn, isbn)
                self.assertEqual(book.title, title)
                self.assertEqual(book.author, author)
                self.assertEqual(book.pages, pages)
                self.assertEqual(book.rating, Book.UNRATED)
                self.assertEqual(book.notes, [])

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_has_methods(self):
        for method_name, signature in [("add_note", '(text: str, page: int, date: datetime.datetime) -> bool'), ("set_rating", '(rating: int) -> bool'), ("get_notes_of_page", '(page: int) -> list[readingdiary.model.Note]'), ("page_with_most_notes", '() -> int'), ("__str__", '() -> str')]:
            with self.subTest(method_name=method_name):
                self.assertTrue(hasattr(self.book_without_notes, method_name))
                method = getattr(self.book_without_notes, method_name)
                self.assertTrue(callable(method))
                self.assertEqual(str(inspect.signature(method)), signature)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_add_note_method_adds_note_to_book(self):
        self.book_without_notes.add_note("This is a note", 1, datetime(2021, 1, 1))
        self.book_without_notes.add_note("Another note", 2, datetime(2021, 1, 2))
        self.assertEqual(len(self.book_without_notes.notes), 2)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_add_note_method_returns_false_when_page_out_of_range(self):
        self.assertFalse(self.book_without_notes.add_note("This is a note", 101, datetime(2021, 1, 1)))

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_add_note_method_returns_true_when_note_added(self):
        self.assertTrue(self.book_without_notes.add_note("This is a note", 1, datetime(2021, 1, 1)))

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_set_rating_method_sets_rating_and_returns_true(self):
        for rating in [1, 2, 3]:
            with self.subTest(rating=rating):
                self.assertTrue(self.book_without_notes.set_rating(rating))
                self.assertEqual(self.book_without_notes.rating, rating)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_set_rating_method_returns_false_when_rating_out_of_range(self):
        self.assertFalse(self.book_without_notes.set_rating(0))
        self.assertFalse(self.book_without_notes.set_rating(4))

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_get_notes_of_page_method_returns_notes_of_given_page(self):
        notes = self.book_with_notes.get_notes_of_page(1)
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, "Note 1")

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_get_notes_of_page_method_returns_empty_list_when_no_notes(self):
        self.assertEqual(self.book_without_notes.get_notes_of_page(1), [])

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_page_with_most_notes_method_returns_page_with_most_notes(self):
        self.assertEqual(self.book_with_notes.page_with_most_notes(), 1)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_page_with_most_notes_method_returns_minus_one_when_no_notes(self):
        self.assertEqual(self.book_without_notes.page_with_most_notes(), -1)

    @unittest.skipUnless(book_defined, "Book class not defined")
    def test_class_book_str_method(self):
        self.assertEqual(str(self.book_without_notes), "ISBN: 1234\nTitle: Test Book\nAuthor: Author X\nPages: 100\nRating: unrated")

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_has_attributes(self):
        for attr_name, attr_type in [("books", dict)]:
            with self.subTest(attr_name=attr_name):
                self.assertTrue(hasattr(self.empty_diary, attr_name))
                self.assertIsInstance(getattr(self.empty_diary, attr_name), attr_type)

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_initializes_empty_books_dict(self):
        self.assertEqual(self.empty_diary.books, {})

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_has_methods(self):
        for method_name, signature in [("add_book", '(isbn: str, title: str, author: str, pages: int) -> bool'), ("search_by_isbn", '(isbn: str) -> readingdiary.model.Book | None'), ("add_note_to_book", '(isbn: str, text: str, page: int, date: datetime.datetime) -> bool'), ("rate_book", '(isbn: str, rating: int) -> bool'), ("book_with_most_notes", '() -> readingdiary.model.Book | None')]:
            with self.subTest(method_name=method_name):
                self.assertTrue(hasattr(self.empty_diary, method_name))
                method = getattr(self.empty_diary, method_name)
                self.assertTrue(callable(method))
                self.assertEqual(str(inspect.signature(method)), signature)

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_add_book_method_adds_book_to_books_dict(self):
        for isbn, title, author, pages in [("1234", "Test Book", "Author X", 100), ("5678", "Another Book", "Author Y", 200), ("9012", "Third Book", "Author Z", 300)]:
            with self.subTest(isbn=isbn, title=title, author=author, pages=pages):
                self.empty_diary.add_book(isbn, title, author, pages)
                self.assertIn(isbn, self.empty_diary.books)
                self.assertIsInstance(self.empty_diary.books[isbn], Book)

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_add_book_method_returns_false_when_isbn_already_exists(self):
        for isbn, title, author, pages in [("1234", "Test Book", "Author X", 100), ("5678", "Another Book", "Author Y", 200)]:
            with self.subTest(isbn=isbn):
                self.assertFalse(self.diary_with_books.add_book(isbn, title, author, pages))

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_search_by_isbn_method_returns_book(self):
        for isbn in ["1234", "5678"]:
            with self.subTest(isbn=isbn):
                self.assertEqual(self.diary_with_books.search_by_isbn(isbn).isbn, isbn)

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_search_by_isbn_method_returns_none_when_isbn_not_found(self):
        self.assertIsNone(self.diary_with_books.search_by_isbn("9999"))

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_add_note_to_book_method_adds_note_to_book_and_returns_true(self):
        for isbn, text, page, date in [("1234", "This is a note", 1, datetime(2021, 1, 1)), ("5678", "Another note", 2, datetime(2021, 1, 2))]:
            with self.subTest(isbn=isbn, text=text, page=page, date=date):
                self.assertTrue(self.diary_with_books.add_note_to_book(isbn, text, page, date))
                self.assertEqual(len(self.diary_with_books.books[isbn].notes), 1)

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_add_note_to_book_method_returns_false_when_isbn_not_found(self):
        self.assertFalse(self.diary_with_books.add_note_to_book("9999", "This is a note", 1, datetime(2021, 1, 1)))

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_rate_book_method_rates_book_and_returns_true(self):
        for isbn in ["1234", "5678"]:
            with self.subTest(isbn=isbn):
                self.assertTrue(self.diary_with_books.rate_book(isbn, 3))
                self.assertEqual(self.diary_with_books.books[isbn].rating, 3)

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_rate_book_method_returns_false_when_isbn_not_found(self):
        self.assertFalse(self.diary_with_books.rate_book("9999", 3))

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_rate_book_method_returns_false_when_rating_out_of_range(self):
        for isbn, rating in [("1234", 0), ("5678", 4)]:
            with self.subTest(isbn=isbn, rating=rating):
                self.assertFalse(self.diary_with_books.rate_book(isbn, rating))

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_book_with_most_notes_method_returns_book_with_most_notes(self):
        self.diary_with_books.add_note_to_book("1234", "Note 1", 1, datetime(2021, 1, 1))
        self.diary_with_books.add_note_to_book("1234", "Note 2", 1, datetime(2021, 1, 2))
        self.diary_with_books.add_note_to_book("1234", "Note 3", 2, datetime(2021, 1, 3))
        self.assertEqual(self.diary_with_books.book_with_most_notes().isbn, "1234")

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_book_with_most_notes_method_returns_none_when_no_books(self):
        self.assertIsNone(self.empty_diary.book_with_most_notes())

    @unittest.skipUnless(reading_diary_defined, "ReadingDiary class not defined")
    def test_class_reading_diary_book_with_most_notes_method_returns_none_when_no_notes(self):
        self.assertIsNone(self.diary_with_books.book_with_most_notes())

if __name__ == '__main__':
    unittest.main()