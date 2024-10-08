from calendar import monthrange
from math import ceil
from pandas import date_range
from pydantic import BaseModel
import cairo
import logging as log

"""
Represents all the parameters and objects that require some processing before drawn
"""


class Processor:
    def __init__(self, data, params):
        self._process_months(data, params)
        self._process_categories(data, params)
        self._process_books(data, params)
        self._process_other(data, params)

    # Sets the ProcessedMonth list of the object
    def _process_months(self, data, prms):
        min_date, max_date = data.get_min_date(data.books), data.get_max_date(
            data.books
        )
        months_text = (
            date_range(min_date, max_date, freq="MS").strftime("%m/%y").tolist()
        )
        if int(min_date.strftime("%d")) > 1:
            months_text = [min_date.strftime("%m/%y")] + months_text
        if prms.reverse_timeline:
            months_text = months_text[::-1]
        i = 0
        self.months = []
        for m in months_text:
            text_y = (
                prms.month_line_start_y
                + prms.month_height * i
                + prms.month_height / 2
                + prms.month_text_font_size / 2
            )
            line_y = prms.month_line_start_y + prms.month_height * (i + 1)
            self.months.append(ProcessedMonth(text=m, text_y=text_y, line_y=line_y))
            i += 1

    # Sets the ProcesseCategory list of the object
    def _process_categories(self, data, prms):
        y = prms.category_start_y
        self.categories = []
        used_categories = {book.category for book in data.books}
        line_start_x = prms.category_start_x
        category_counter = 0
        for category in data.categories:
            if not prms.category_hide_unused or category in used_categories:
                line_end_x = line_start_x + prms.category_line_length
                text_start_x = line_end_x + prms.category_text_padding
                self.categories.append(
                    ProcessedCategory(
                        name=category.name,
                        color=category.color,
                        start_y=y,
                        line_start_x=line_start_x,
                        line_end_x=line_end_x,
                        text_start_x=text_start_x,
                    )
                )
                y += prms.category_vertical_spacing
                category_counter += 1
                if category_counter % prms.category_max_rows == 0:
                    line_start_x += prms.category_column_width
                    y = prms.category_start_y

    # Sets the ProcessedBook list of the object
    def _process_books(self, data, prms):
        self.books = [ProcessedBook(book, self.months, prms) for book in data.books]
        self._check_book_collisions(prms)

    # Sets the rest of parameters that require processing
    def _process_other(self, data, prms):
        self.timeline_end_y = (
            prms.month_line_start_y + len(self.months) * prms.month_height
        )
        self.canvas_size_y = (
            self.timeline_end_y + prms.canvas_padding_bottom * prms.canvas_zoom
        )

    def _check_book_collisions(self, prms):
        # Find minimum separation between starting tips
        min_y = self._get_min_separation(lambda x: x.start_y)

        if min_y < 2 * prms.book_tip_radius:
            new_min_y = 2 * prms.book_tip_radius * prms.month_height / min_y
            log.warning(
                (
                    "Book tips are colliding. To prevent it, you may:\n"
                    + " - Increase month_height to at least %.2f\n"
                    + " - Decrease book_tip_radius to at most %.2f\n"
                    + " - Change the dates further apart"
                )
                % (ceil(new_min_y * 100) / 100.0, min_y / 2)
            )

        # Find minimum separation between book labels
        min_y = self._get_min_separation(lambda x: x.finish_y)
        text_height = (
            prms.book_title_font_size * prms.book_text_line_spacing
            + prms.book_author_font_size
        )

        if min_y < text_height:
            new_min_y = text_height * prms.month_height / min_y
            log.warning(
                (
                    "Book labels are colliding. To prevent it, you may:\n"
                    + " - Increase month_height to at least %.2f\n"
                    + " - Decrease title or subtitle font size\n"
                    + " - Change the dates further apart"
                )
                % (ceil(new_min_y * 100) / 100.0)
            )

    def _get_min_separation(self, map):
        books = sorted(self.books, key=map)
        min_y = float("inf")
        i = 1
        while i < len(self.books):
            y = abs(map(books[i]) - map(books[i - 1]))
            if y > 0:
                min_y = min(min_y, y)
            i += 1
        return min_y


class ProcessedMonth(BaseModel):
    text: str
    text_y: float
    line_y: float


class ProcessedCategory(BaseModel):
    name: str
    color: str
    start_y: float
    line_start_x: float
    line_end_x: float
    text_start_x: float


class ProcessedBook:
    def __init__(self, book, months, prms):
        self.title = book.title
        self.subtitle = self._get_subtitle(book)
        self.start_y = self._get_y(book.start_date, months, prms)
        self.finish_y = self._get_y(book.finish_date, months, prms)
        self.color = prms.category_default_color
        if book.category is not None:
            self.color = book.category.color
        self.score = None
        if book.score is not None:
            self.score = book.score / 2
            self.score_x = prms.book_text_start_x + self._get_textwidth(
                self.subtitle, prms.book_author_font_size, prms.book_text_font
            )
            self.score_color = (
                self.color if prms.book_score_colored else prms.book_score_color
            )
        self.link = book.link

    # Returns the subtitle text for a given book
    def _get_subtitle(self, book):
        subtitle = book.author
        if book.publication_year is not None:
            subtitle += " (%d)" % book.publication_year
        return subtitle

    # Returns the tip's y-coordinate for a given date
    def _get_y(self, date, months, prms):
        month_y = (
            self._get_processed_month(date.strftime("%m/%y"), months).line_y
            - prms.month_height
        )
        month_len = monthrange(date.year, date.month)[1]
        month_prop = (int(date.strftime("%d")) - 1) / month_len
        if prms.reverse_timeline:
            month_prop = 1 - month_prop
        return month_y + month_prop * prms.month_height

    # Returns the corresponding ProcessedMonth from a given date (already formatted)
    def _get_processed_month(self, text, months):
        month = [m for m in months if m.text == text]
        assert month, "No ProcessedMonth found for date %s" % text
        return month[0]

    # Returns the width of the subtitle text, aproximate
    def _get_textwidth(self, text, fontsize, family):
        surface = cairo.SVGSurface("undefined.svg", 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face(family)
        cr.set_font_size(fontsize)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
        return width
