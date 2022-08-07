# Represents the type for each parameter in the config file
param_types = {
    'book_author_font_size': float,
    'book_line_width': float,
    'book_text_line_spacing': float,
    'book_text_start_x': float,
    'book_tip_radius': float,
    'book_title_font_size': float,
    'canvas_size_x': int,
    'canvas_size_y': int,
    'category_default_color': str,
    'category_line_start_x': float,
    'category_line_length': float,
    'category_line_width': float,
    'category_start_y': float,
    'category_text_color': str,
    'category_text_font_size': float,
    'category_text_padding': float,
    'category_tip_radius': float,
    'category_vertical_spacing': float,
    'date_finished_start_x': float,
    'date_started_start_x': float,
    'date_text_anchor': str,
    'date_text_color': str,
    'date_text_font_size': float,
    'date_text_line_spacing': float,
    'date_text_start_y': float,
    'month_height': float,
    'month_line_start_x': float,
    'month_line_start_y': float,
    'month_text_color': str,
    'month_text_font_size': float,
    'month_text_start_x': float,
    'timeline_end_x': float,
    'timeline_line_color': str,
    'timeline_line_width': float,
    'timeline_start_x': float,
    'timeline_start_y': float,
}

'''
Represents the configuration parameters
'''
class Config:
    def __init__(self, params):
        for p in param_types.keys():
            if p not in params:
                print("Missing parameter '%s'." % p)
                exit(1)
            if(not isinstance(params[p], param_types[p])):
                print("Parameter '%s' should be of type %s." %(p, param_types[p].__name__))
                exit(1)
            setattr(self, p, params[p])