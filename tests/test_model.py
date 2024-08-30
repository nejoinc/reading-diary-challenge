from datetime import datetime
import inspect

import pytest

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

@pytest.fixture
def note():
    return Note("This is a note", 1, datetime(2021, 1, 1))

@pytest.fixture
def book_without_notes():
    return Book("1234", "Test Book", "Author X", 100)

@pytest.fixture
def book_with_notes():
    book = Book("1234", "Test Book", "Author X", 100)
    book.add_note("Note 1", 1, datetime(2021, 1, 1))
    book.add_note("Note 2", 2, datetime(2021, 1, 2))
    book.add_note("Note 3", 1, datetime(2021, 1, 3))
    return book

@pytest.fixture
def empty_diary():
    return ReadingDiary()

@pytest.fixture
def diary_with_books():
    diary = ReadingDiary()
    diary.add_book("1234", "Test Book", "Author X", 100)
    diary.add_book("5678", "Another Book", "Author Y", 200)
    return diary

# Test Note class
@pytest.mark.skipif(not note_defined, reason="Note class not defined")
@pytest.mark.parametrize("attr_name, attr_type", [
    ("text", str),
    ("page", int),
    ("date", datetime)
])
def test_class_note_has_attribute(note, attr_name, attr_type):
    assert hasattr(note, attr_name)
    assert isinstance(getattr(note, attr_name), attr_type)

@pytest.mark.skipif(not note_defined, reason="Note class not defined")
@pytest.mark.parametrize("text, page, date", [
    ("This is a note", 1, datetime(2021, 1, 1)),
    ("Another note", 2, datetime(2021, 1, 2))
])
def test_note_class_initializes_attributes(text, page, date):
    note = Note(text, page, date)
    assert note.text == text
    assert note.page == page
    assert note.date == date

@pytest.mark.skipif(not note_defined, reason="Note class not defined")
def test_note_class_str_method(note):
    assert str(note) == "2021-01-01 00:00:00 - page 1: This is a note"

# Test Book class
@pytest.mark.skipif(not book_defined, reason="Book class not defined")
@pytest.mark.parametrize("const_name, const_value", [
    ("EXCELLENT", 3),
    ("GOOD", 2),
    ("BAD", 1),
    ("UNRATED", -1)
])
def test_book_class_has_constants(const_name, const_value):
    assert hasattr(Book, const_name)
    assert getattr(Book, const_name) == const_value

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
@pytest.mark.parametrize("attr_name, attr_type", [
    ("isbn", str),
    ("title", str),
    ("author", str),
    ("pages", int),
    ("rating", int),
    ("notes", list)
])
def test_class_book_has_attributes(book_without_notes, attr_name, attr_type):
    assert hasattr(book_without_notes, attr_name)
    assert isinstance(getattr(book_without_notes, attr_name), attr_type)

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
@pytest.mark.parametrize("isbn, title, author, pages", [
    ("1234", "Test Book", "Author X", 100),
    ("5678", "Another Book", "Author Y", 200),
    ("9012", "Third Book", "Author Z", 300)
])
def test_book_class_initializes_attributes(isbn, title, author, pages):
    book = Book(isbn, title, author, pages)
    assert book.isbn == isbn
    assert book.title == title
    assert book.author == author
    assert book.pages == pages
    assert book.rating == Book.UNRATED
    assert book.notes == []

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
@pytest.mark.parametrize("method_name, signature", [
    ("add_note", '(text: str, page: int, date: datetime.datetime) -> bool'),
    ("set_rating", '(rating: int) -> bool'),
    ("get_notes_of_page", '(page: int) -> list[readingdiary.model.Note]'),
    ("page_with_most_notes", '() -> int'),
    ("__str__", '() -> str')
])
def test_class_book_has_methods(book_without_notes, method_name, signature):
    assert hasattr(book_without_notes, method_name)
    method = getattr(book_without_notes, method_name)
    assert callable(method)
    assert str(inspect.signature(method)) == signature

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_add_note_method_adds_note_to_book(book_without_notes):
    book_without_notes.add_note("This is a note", 1, datetime(2021, 1, 1))
    book_without_notes.add_note("Another note", 2, datetime(2021, 1, 2))
    assert len(book_without_notes.notes) == 2

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_add_note_method_returns_false_when_page_out_of_range(book_without_notes):
    assert not book_without_notes.add_note("This is a note", 101, datetime(2021, 1, 1))

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_add_note_method_returns_true_when_note_added(book_without_notes):
    assert book_without_notes.add_note("This is a note", 1, datetime(2021, 1, 1))

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
@pytest.mark.parametrize("rating", [1, 2, 3])
def test_class_book_set_rating_method_sets_rating_and_returns_true(book_without_notes, rating):
    assert book_without_notes.set_rating(rating)
    assert book_without_notes.rating == rating

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_set_rating_method_returns_false_when_rating_out_of_range(book_without_notes):
    assert not book_without_notes.set_rating(0)
    assert not book_without_notes.set_rating(4)

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_get_notes_of_page_method_returns_notes_of_given_page(book_with_notes):
    notes = book_with_notes.get_notes_of_page(1)
    assert len(notes) == 2
    assert notes[0].text == "Note 1"

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_get_notes_of_page_method_returns_empty_list_when_no_notes(book_without_notes):
    assert book_without_notes.get_notes_of_page(1) == []

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_page_with_most_notes_method_returns_page_with_most_notes(book_with_notes):
    assert book_with_notes.page_with_most_notes() == 1

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_page_with_most_notes_method_returns_minus_one_when_no_notes(book_without_notes):
    assert book_without_notes.page_with_most_notes() == -1

@pytest.mark.skipif(not book_defined, reason="Book class not defined")
def test_class_book_str_method(book_without_notes):
    assert str(book_without_notes) == "ISBN: 1234\nTitle: Test Book\nAuthor: Author X\nPages: 100\nRating: unrated"
    
# Test ReadingDiary class
@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("attr_name, attr_type", [
    ("books", dict)
])
def test_class_reading_diary_has_attributes(empty_diary, attr_name, attr_type):
    assert hasattr(empty_diary, attr_name)
    assert isinstance(getattr(empty_diary, attr_name), attr_type)

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_initializes_empty_books_dict(empty_diary):
    assert empty_diary.books == {}

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("method_name, signature", [
    ("add_book", '(isbn: str, title: str, author: str, pages: int) -> bool'),
    ("search_by_isbn", '(isbn: str) -> readingdiary.model.Book | None'),
    ("add_note_to_book", '(isbn: str, text: str, page: int, date: datetime.datetime) -> bool'),
    ("rate_book", '(isbn: str, rating: int) -> bool'),
    ("book_with_most_notes", '() -> readingdiary.model.Book | None')
])
def test_class_reading_diary_has_methods(empty_diary, method_name, signature):
    assert hasattr(empty_diary, method_name)
    method = getattr(empty_diary, method_name)
    assert callable(method)
    assert str(inspect.signature(method)) == signature

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("isbn, title, author, pages", [
    ("1234", "Test Book", "Author X", 100),
    ("5678", "Another Book", "Author Y", 200),
    ("9012", "Third Book", "Author Z", 300)
])
def test_class_reading_diary_add_book_method_adds_book_to_books_dict(empty_diary, isbn, title, author, pages):
    empty_diary.add_book(isbn, title, author, pages)
    assert isbn in empty_diary.books
    assert isinstance(empty_diary.books[isbn], Book)

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("isbn, title, author, pages", [
    ("1234", "Test Book", "Author X", 100),
    ("5678", "Another Book", "Author Y", 200),
])
def test_class_reading_diary_add_book_method_returns_false_when_isbn_already_exists(diary_with_books, isbn, title, author, pages):
    assert not diary_with_books.add_book(isbn, title, author, pages)
    
@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("isbn", ["1234", "5678"])
def test_class_reading_diary_search_by_isbn_method_returns_book(diary_with_books, isbn):
    assert diary_with_books.search_by_isbn(isbn).isbn == isbn

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_search_by_isbn_method_returns_none_when_isbn_not_found(diary_with_books):
    assert diary_with_books.search_by_isbn("9999") is None

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("isbn, text, page, date", [
    ("1234", "This is a note", 1, datetime(2021, 1, 1)),
    ("5678", "Another note", 2, datetime(2021, 1, 2)
)])
def test_class_reading_diary_add_note_to_book_method_adds_note_to_book_and_returns_true(diary_with_books, isbn, text, page, date):
    assert diary_with_books.add_note_to_book(isbn, text, page, date)
    assert len(diary_with_books.books[isbn].notes) == 1
    

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_add_note_to_book_method_returns_false_when_isbn_not_found(diary_with_books):
    assert not diary_with_books.add_note_to_book("9999", "This is a note", 1, datetime(2021, 1, 1))

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("isbn", ["1234", "5678"])
def test_class_reading_diary_rate_book_method_rates_book_and_returns_true(diary_with_books, isbn):
    assert diary_with_books.rate_book(isbn, 3)
    assert diary_with_books.books[isbn].rating == 3

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_rate_book_method_returns_false_when_isbn_not_found(diary_with_books):
    assert not diary_with_books.rate_book("9999", 3)

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
@pytest.mark.parametrize("isbn, rating", [
    ("1234", 0),
    ("5678", 4)
])
def test_class_reading_diary_rate_book_method_returns_false_when_rating_out_of_range(diary_with_books, isbn, rating):
    assert not diary_with_books.rate_book(isbn, rating)

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_book_with_most_notes_method_returns_book_with_most_notes(diary_with_books):
    diary_with_books.add_note_to_book("1234", "Note 1", 1, datetime(2021, 1, 1))
    diary_with_books.add_note_to_book("1234", "Note 2", 1, datetime(2021, 1, 2))
    diary_with_books.add_note_to_book("1234", "Note 3", 2, datetime(2021, 1, 3))
    assert diary_with_books.book_with_most_notes().isbn == "1234"

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_book_with_most_notes_method_returns_none_when_no_books(empty_diary):
    assert empty_diary.book_with_most_notes() is None

@pytest.mark.skipif(not reading_diary_defined, reason="ReadingDiary class not defined")
def test_class_reading_diary_book_with_most_notes_method_returns_none_when_no_notes(diary_with_books):
    assert diary_with_books.book_with_most_notes() is None