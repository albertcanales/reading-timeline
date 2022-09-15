from utils import perror
from colour import Color
from collections import namedtuple

Font = namedtuple("Font", "name filename")

# Represents the type for each parameter in the config file
param_types = {
    'book_author_font_size': float,
    'book_line_width': float,
    'book_text_font': str,
    'book_text_line_spacing': float,
    'book_text_start_x': float,
    'book_tip_radius': float,
    'book_title_font_size': float,
    'canvas_padding_bottom': float,
    'canvas_size_x': float,
    'canvas_zoom': float,
    'category_default_color': Color,
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
                perror("Missing parameter '%s'." % p)
            if param_types[p] == Color:
                try:
                    Color(params[p])
                except ValueError:
                    perror("Parameter %s is not a valid color." %(p))
            elif not isinstance(params[p], param_types[p]):
                if param_types[p] != float or not isinstance(params[p], int):
                    perror("Parameter '%s' should be of type %s." %(p, param_types[p].__name__))
            setattr(self, p, params[p])

        # Fonts
        self.fonts = []

        if 'fonts' in params:
            if not isinstance(params['fonts'], list):
                perror("Variable 'fonts' must be a list.")
            for item in params['fonts']:
                if 'name' not in item:
                    perror("A font is missing name")
                if 'filename' not in item:
                    perror("A font is missing filename")
                font = Font(item['name'], item['filename'])
                try:
                    open(font.filename, 'r')
                except OSError:
                    perror("Font on '%s' cannot be read." % font.filename)
                self.fonts.append(font)

        # Check param fonts
        for font in [ self.month_text_font, self.date_text_font,
                        self.category_text_font, self.book_text_font ]:
            if font not in [ item.name for item in self.fonts ]:
                print(font)
                perror("Font not found in fonts variable.")
