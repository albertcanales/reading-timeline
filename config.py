param_types = {
    'book_author_font_size': float,
    'book_line_color': str,
    'book_line_width': float,
    'book_tip_color': str,
    'book_tip_radius': float,
    'book_title_font_size': float,
    'book_text_line_spacing': float,
    'book_text_start_x': float,
    'timeline_end_x': float,
    'timeline_start_x': float,
}

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