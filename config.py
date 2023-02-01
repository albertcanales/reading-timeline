import logging as log
from colour import Color
from collections import namedtuple

Font = namedtuple("Font", "name filename")

# Represents the type for each parameter in the config file
param_types = {
    'book_author_font_size': float,
    'book_line_width': float,
    'book_score_outer_radius': float,
    'book_score_inner_radius': float,
    'book_score_padding': float,
    'book_score_color': Color,
    'book_score_colored': bool,
    'book_text_font': str,
    'book_text_line_spacing': float,
    'book_text_color': Color,
    'book_text_start_x': float,
    'book_tip_radius': float,
    'book_title_font_size': float,
    'canvas_background_color': Color,
    'canvas_padding_bottom': float,
    'canvas_size_x': float,
    'canvas_zoom': float,
    'category_default_color': Color,
    'category_hide_unused': bool,
    'category_line_length': float,
    'category_line_start_x': float,
    'category_line_width': float,
    'category_start_y': float,
    'category_text_color': Color,
    'category_text_font': str,
    'category_text_font_size': float,
    'category_text_padding': float,
    'category_tip_radius': float,
    'category_vertical_spacing': float,
    'date_finished_start_x': float,
    'date_started_start_x': float,
    'date_text_anchor': str,
    'date_text_color': Color,
    'date_text_font': str,
    'date_text_font_size': float,
    'date_text_line_spacing': float,
    'date_text_start_y': float,
    'month_height': float,
    'month_line_start_x': float,
    'month_line_start_y': float,
    'month_text_color': Color,
    'month_text_font': str,
    'month_text_font_size': float,
    'month_text_start_x': float,
    'reverse_timeline': bool,
    'timeline_end_x': float,
    'timeline_line_color': Color,
    'timeline_line_width': float,
    'timeline_start_x': float,
    'timeline_start_y': float,
}

'''
Represents the configuration parameters
'''
class Config:
    def __init__(self, params):
        # Params
        for p in param_types.keys():
            if p not in params:
                log.error("Missing parameter '%s'." % p)
                exit(1)
            if param_types[p] == Color:
                try:
                    Color(params[p])
                except ValueError:
                    log.error("Parameter %s is not a valid color." %(p))
                    exit(1)
            elif not isinstance(params[p], param_types[p]):
                if param_types[p] != float or not isinstance(params[p], int):
                    log.error("Parameter '%s' should be of type %s." %(p, param_types[p].__name__))
                    exit(1)
            setattr(self, p, params[p])

        # Fonts
        self.fonts = []

        if 'fonts' in params:
            if not isinstance(params['fonts'], list):
                log.error("Variable 'fonts' must be a list.")
                exit(1)
            for item in params['fonts']:
                if 'name' not in item:
                    log.error("A font is missing name")
                    exit(1)
                if 'filename' not in item:
                    log.error("A font is missing filename")
                    exit(1)
                font = Font(item['name'], item['filename'])
                try:
                    open(font.filename, 'r')
                except OSError:
                    log.error("Font on '%s' cannot be read." % font.filename)
                    exit(1)
                self.fonts.append(font)

        # Check param fonts
        for font in [ self.month_text_font, self.date_text_font,
                        self.category_text_font, self.book_text_font ]:
            if font not in [ item.name for item in self.fonts ]:
                print(font)
                log.error("Font not found in fonts variable.")
                exit(1)
