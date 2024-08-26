import logging as log
import datetime
from colour import Color

"""
Represents the union of the YAML's data: books
"""


class Data:
    def __init__(self, data):
        # Optional fields
        self.categories = self._init_categories(data)
        self.from_date = data["from"] if "from" in data.keys() else None
        self.to_date = data["to"] if "to" in data.keys() else None

        self.books = self._init_books(data, self.categories)

    def __str__(self):
        s = "Categories:\n" + "\n".join(
            [" - " + str(category) for category in self.categories]
        )
        s += "\nBooks:\n" + "\n".join([" - " + str(book) for book in self.books])
        return s

    # Returns the minimum date of the given books
    def get_min_date(self, books):
        return min([book.start_date for book in books])

    # Returns the maximum date of the given books
    def get_max_date(self, books):
        return max([book.finish_date for book in books])

    # Returns all books whose start and finish dates are inside of the given interval
    def _get_books_in_dates(self, books, min_date, max_date):
        return [book for book in books if book.is_in_range(min_date, max_date)]

    # Sets the categories variable
    def _init_categories(self, data):
        if "categories" in data.keys():
            if not isinstance(data["categories"], list):
                log.error("The categories variable must be a list.")
                exit(1)
            categories = [Category(category) for category in data["categories"]]
            self._check_categories(categories)
            return categories
        log.warning("No categories variable found.")
        return []

    # Sets the books variable
    def _init_books(self, data, categories):
        try:
            if not isinstance(data["books"], list):
                log.error("The books variable must be a list.")
                exit(1)
        except TypeError:
            log.error("No books variable is found.")
            exit(1)
        books = []
        for book_data in data["books"]:
            book = Book(book_data, categories)
            if book.finish_date is not None:
                books.append(book)
        self._check_books(books)
        return self._get_books_in_dates(books, self.from_date, self.to_date)

    # Error checking for categories
    def _check_categories(self, categories):
        category_ids = [category.id for category in categories]
        if len(category_ids) != len(set(category_ids)):
            log.error("Category ids must be unique.")
            exit(1)

    # Error checking for books
    def _check_books(self, books):
        start_dates = [book.start_date for book in books]
        if len(start_dates) != len(set(start_dates)):
            log.warning("Unique start dates are recommended for visual clearance.")
        finish_dates = [book.finish_date for book in books]
        if len(finish_dates) != len(set(finish_dates)):
            log.warning("Unique finish dates are recommended for visual clearance.")


"""
Represents an element from the categories YAML variable
"""


class Category:
    def __init__(self, category):
        try:
            self.id = category["id"]
            self.name = category["name"]
            self.color = category["color"]

        except KeyError:
            log.error("This category is missing data: \n%s" % category)
            exit(1)

        # Error handling
        try:
            Color(self.color)
        except:
            log.error("Category '%s' has an invalid color." % (self.name))
            exit(1)

    def __str__(self):
        return "%s (%s)" % (self.name, self.color.upper())


"""
Represents an element from the books YAML variable
"""


class Book:
    def __init__(self, book, categories):
        # Required fields
        try:
            self.title = book["title"]
            self.author = book["author"]
            self.start_date = book["started"]

            self._check_date(self.title, self.start_date)

        except KeyError:
            log.error("This book is missing data: \n%s" % book)
            exit(1)

        # Finished date optional field
        self.finish_date = None
        if "finished" in book.keys():
            self.finish_date = book["finished"]
            self._check_date(self.title, self.finish_date)
        else:
            log.warning("Book %s without finish date is being ignored" % (self.title))

        # Other optional fields
        self.publication_year = None
        if "publication_year" in book.keys():
            self.publication_year = book["publication_year"]
        self.category = None
        if "category" in book.keys():
            self.category = self._get_category(book["category"], categories)
        self.score = None
        if "score" in book.keys():
            self.score = book["score"]
            self._check_score(self.title, self.score)
        self.link = None
        if "link" in book.keys():
            self.link = book["link"]

        # Error handling
        if self.finish_date is not None and self.finish_date < self.start_date:
            log.error("Book %s has been finished before started." % self.title)
            exit(1)
        if self.publication_year is not None:
            if datetime.date(self.publication_year, 1, 1) > self.start_date:
                log.error("Book %s has been published after started." % self.title)
                exit(1)

    def __str__(self):
        s = "%s by %s" % (self.title, self.author)
        if self.publication_year is not None:
            s += " (%d)" % self.publication_year
        s += ", %s - %s" % (self.start_date, self.finish_date)
        if self.category is not None:
            s += " [%s]" % self.category.name
        if self.link is not None:
            s += " {%s}" % self.link
        return s

    def is_in_range(self, from_date, to_date):
        return (from_date is None or from_date <= self.start_date) and (
            to_date is None or to_date >= self.finish_date
        )

    def _get_category(self, category_id, categories):
        for cat in categories:
            if cat.id == category_id:
                return cat
        log.warning("Category %s for book %s not defined" % (category_id, self.title))
        return None

    def _check_date(self, title, date):
        if not isinstance(date, datetime.date):
            log.error("Book %s has an invalid date '%s'." % (title, date))
            exit(1)

    def _check_score(self, title, score):
        if not isinstance(score, int):
            log.error("Book %s has an invalid score '%s'." % (title, score))
            exit(1)
        if score < 0 or score > 10:
            log.error(
                "Score from book %s must be between 0 and 10 (or not defined)."
                % (title)
            )
            exit(1)
