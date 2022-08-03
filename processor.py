import pandas as pd
from collections import namedtuple

ProcessedMonth = namedtuple("ProcessedMonth", "text text_y line_y")

class Processor:
    def __init__(self, data, config):
        self.months = self._process_months(data, config)


    def _process_months(self, data, c):
        months_text = pd.date_range(data.books.get_min_date(), data.books.get_max_date(), freq='MS').strftime("%m/%y").tolist()
        i = 0
        months = []
        for m in months_text:
            text_y = c.month_line_start_y + c.month_height*i + c.month_height/2 + c.month_text_font_size/2
            line_y = c.month_line_start_y + c.month_height*(i+1)
            months.append(ProcessedMonth(m, text_y, line_y))
            i += 1
        return months