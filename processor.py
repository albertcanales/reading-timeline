import pandas as pd
from collections import namedtuple
import calendar

ProcessedMonth = namedtuple("ProcessedMonth", "text text_y line_y")
ProcessedBook = namedtuple("ProcessedBook", "title subtitle start_y finish_y")

'''
Represents all the configuration parameters and objects that require some processing before drawn
'''
class Processor:
    def __init__(self, data, config):

        self._process_months(data, config)
        self._process_books(data, config)
        self._process_other(data, config)


    # Sets the ProcessedMonth list of the object
    def _process_months(self, data, c):
        min_date, max_date = data.get_min_date(data.books), data.get_max_date(data.books)
        months_text = pd.date_range(min_date, max_date, freq='MS').strftime("%m/%y").tolist()[::-1]
        if int(min_date.strftime('%d')) > 1:
            months_text = months_text + [ min_date.strftime("%m/%y") ]
        i = 0
        self.months = []
        for m in months_text:
            text_y = c.month_line_start_y + c.month_height*i + c.month_height/2 + c.month_text_font_size/2
            line_y = c.month_line_start_y + c.month_height*(i+1)
            self.months.append(ProcessedMonth(m, text_y, line_y))
            i += 1

    # Sets the ProcessedMonth list of the object
    def _process_books(self, data, c):
        self.books = []
        for book in data.books:
            subtitle = book.author
            if book.publication_year is not None:
                subtitle += " (%d)" % book.publication_year
            start_y = self._get_y(book.start_date, c)
            finish_y = self._get_y(book.finish_date, c)
            self.books.append(ProcessedBook(book.title, subtitle, start_y, finish_y))


    # Sets the rest of parameters that require processing
    def _process_other(self, data, c):
        self.timeline_end_y = c.month_line_start_y + len(self.months) * c.month_height

    # Used by _process_books, to get the tip's y coordinate from its date
    def _get_y(self, date, c):
        month_y = self._get_processed_month(date.strftime("%m/%y")).line_y - c.month_height
        month_len = calendar.monthrange(date.year, date.month)[1]
        return month_y + (1 - (int(date.strftime("%d"))-1) / month_len) * c.month_height

    # Used by _process_books, to get the corresponding ProcessedMonth from a given already formatted date
    def _get_processed_month(self, text):
        month = [m for m in self.months if m.text == text]
        assert month, "No ProcessedMonth found for date %s" % text
        return month[0]
