class Data:
    def __init__(self, data):
        self.books = Books(data)

    def __str__(self):
        return str(self.books)

class Books:
    def __init__(self, data):
        try:
            if not isinstance(data['books'], list):
                print("The books variable must be a list.")
                exit(1)
            self.books = [Book(book) for book in data['books']]
        except TypeError:
            print("No books variable is found.")
            exit(1)
        # Check unique book dates
        start_dates = [ book.start_date for book in self.books]
        if len(start_dates) != len(set(start_dates)):
            print("Start dates must be unique.")
            exit(1)
        finish_dates = [ book.finish_date for book in self.books]
        if len(finish_dates) != len(set(finish_dates)):
            print("Finish dates must be unique.")
            exit(1)

    def __str__(self):
        return "Books:\n" + \
                '\n'.join([" - " + str(book) for book in self.books ])

    def get_min_date(self):
        return min([ book.start_date for book in self.books ])

    def get_max_date(self):
        return max([ book.finish_date for book in self.books ])

    def get_books_in_dates(self, min_date, max_date):
        return filter(lambda book: book.start_date >= min_date and book.finish_date < max_date, self.books)

class Book:
    def __init__(self, book):
        try:
            self.name = book['name']
            self.author = book['author']
            self.start_date = book['started']
            self.finish_date = book['finished']

            if self.finish_date < self.start_date:
                print("Book %s has been finished before started." % self.name)
                exit(1)
        except KeyError:
            print("This book is missing data: \n%s" %book)
            exit(1)

    def __str__(self):
        return "%s by %s, %s - %s" \
            %(self.name, self.author, self.start_date, self.finish_date)
