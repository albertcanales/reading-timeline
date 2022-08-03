import pandas as pd
from collections import namedtuple
import calendar

ProcessedMonth = namedtuple("ProcessedMonth", "text text_y line_y")

class Processor:
    def __init__(self, data, config):
        self.months = self._process_months(data, config)
        self.books = self. _process_books(data, config)

    def _process_months(self, data, c):
        months_text = reversed(pd.date_range(data.get_min_date(), data.get_max_date(), freq='MS').strftime("%m/%y").tolist())
        i = 0
        months = []
        for m in months_text:
            text_y = c.month_line_start_y + c.month_height*i + c.month_height/2 + c.month_text_font_size/2
            line_y = c.month_line_start_y + c.month_height*(i+1)
            months.append(ProcessedMonth(m, text_y, line_y))
            i += 1
        return months

    def _process_books(self, data, c):
        return [ ProcessedBook(book, self.months, c) for book in data.books ]

class ProcessedBook:
    def __init__(self, book, months, c):
        self.title = book.title
        self.author = book.author
        self.start_y = self._get_y(book.start_date, months, c)
        self.finish_y = self._get_y(book.finish_date, months, c)

    def _get_y(self, date, months, c):
        month_y = self._get_processed_month(date.strftime("%m/%y"), months).line_y
        month_len = calendar.monthrange(date.year, date.month)[1]
        return month_y + (int(date.strftime("%d"))-1) / month_len * c.month_height

    def _get_processed_month(self, text, months):
        return [m for m in months if m.text == text][0]