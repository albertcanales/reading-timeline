import datetime

'''
Represents the union of the YAML's data: books
'''
class Data:
    def __init__(self, data):
        try:
            if not isinstance(data['books'], list):
                print("The books variable must be a list.")
                exit(1)
        except TypeError:
            print("No books variable is found.")
            exit(1)
        self.books = [Book(book) for book in data['books']]
        self._check_books()

    def __str__(self):
        return "Books:\n" + \
            '\n'.join([" - " + str(book) for book in self.books ])

    # Returns the minimum date (start and finish) of the given books
    def get_min_date(self, books):
        return min([ book.start_date for book in books ])

    # Returns the maximum date (start and finish) of the given books
    def get_max_date(self, books):
        return max([ book.finish_date for book in books ])

    # Returns all books whose start and finish dates are inside of the given interval
    def get_books_in_dates(self, min_date, max_date):
        return filter(lambda book: book.start_date >= min_date and book.finish_date < max_date, self.books)

    # Error checking for books
    def _check_books(self):
        start_dates = [ book.start_date for book in self.books]
        if len(start_dates) != len(set(start_dates)):
            print("Start dates must be unique.")
            exit(1)
        finish_dates = [ book.finish_date for book in self.books]
        if len(finish_dates) != len(set(finish_dates)):
            print("Finish dates must be unique.")
            exit(1)

'''
Represents an element from the book YAML variable
'''
class Book:
    def __init__(self, book):

        # Required fields
        try:
            self.title = book['title']
            self.author = book['author']
            self.start_date = book['started']
            self.finish_date = book['finished']

        except KeyError:
            print("This book is missing data: \n%s" %book)
            exit(1)

        # Optional fields
        self.publication_year = None
        if 'publication_year' in book.keys():
            self.publication_year = book['publication_year']

        # Error handling
        if self.finish_date < self.start_date:
            print("Book %s has been finished before started." % self.title)
            exit(1)
        if self.publication_year is not None:
            if datetime.date(self.publication_year, 1, 1) > self.start_date:
                print("Book %s has been published after started." % self.title)
                exit(1)

    def __str__(self):
        s = "%s by %s" % (self.title, self.author)
        if self.publication_year is not None:
            s += " (%d)" % self.publication_year
        s += ", %s - %s" % (self.start_date, self.finish_date)
        return s
