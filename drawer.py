import math
import svgwrite
import cairo

def draw(path, c, p):
    dwg = svgwrite.Drawing(path, (c.canvas_size_x, p.canvas_size_y*c.canvas_zoom), viewBox="0 0 %d %d" %(c.canvas_size_x/c.canvas_zoom, p.canvas_size_y), style="background-color:%s" % c.canvas_background_color)
    dwg = draw_grid(dwg, c, p)
    for font in c.fonts:
        dwg.embed_font(name=font.name, filename=font.filename)
    for category in p.categories:
        dwg = draw_category(dwg, category, c, p)
    for book in p.books:
        dwg = draw_book(dwg, book, c)
    dwg.save(pretty=True)

def draw_grid(dwg, c, p):
    # Vertical lines
    dwg.add(dwg.line((c.timeline_start_x, c.timeline_start_y), (c.timeline_start_x, p.timeline_end_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))
    dwg.add(dwg.line((c.timeline_end_x, c.timeline_start_y), (c.timeline_end_x, p.timeline_end_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))

    # Month labels and lines
    dwg.add(dwg.line((c.month_line_start_x, c.month_line_start_y), (c.timeline_end_x, c.month_line_start_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))
    for month in p.months:
        dwg.add(dwg.text(month.text, insert=(c.month_text_start_x, month.text_y), font_style='italic', font_size=str(c.month_text_font_size)+'px', font_family=c.month_text_font, fill=c.month_text_color))
        dwg.add(dwg.line((c.month_line_start_x, month.line_y), (c.timeline_end_x, month.line_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))

    # Date labels
    dy = c.date_text_font_size * c.date_text_line_spacing

    text = dwg.text("", insert=(c.date_started_start_x, c.date_text_start_y), font_style='italic', font_size=str(c.date_text_font_size)+'px', font_family=c.date_text_font, fill=c.date_text_color, text_anchor=c.date_text_anchor)
    text.add(dwg.tspan('Date'))
    text.add(dwg.tspan('Started', x=[c.date_started_start_x], dy=[str(dy)+"px"]))
    dwg.add(text)

    text = dwg.text("", insert=(c.date_finished_start_x, c.date_text_start_y), font_style='italic', font_size=str(c.date_text_font_size)+'px', font_family=c.date_text_font, fill=c.date_text_color, text_anchor=c.date_text_anchor)
    text.add(dwg.tspan('Date'))
    text.add(dwg.tspan('Finished', x=[c.date_finished_start_x], dy=[str(dy)+"px"]))
    dwg.add(text)

    return dwg

def draw_category(dwg, category, c, p):
    # Line
    dwg.add(dwg.line((c.category_line_start_x, category.start_y), (p.category_line_end_x, category.start_y), stroke=category.color, stroke_width=c.category_line_width))

    # Circle
    dwg.add(dwg.circle((p.category_line_end_x, category.start_y), r=c.category_tip_radius, fill=category.color))

    # Category name
    dwg.add(dwg.text(category.name, insert=(p.category_text_start_x, category.start_y), font_size=str(c.category_text_font_size)+'px', fill=c.category_text_color, dominant_baseline='middle', font_family=c.category_text_font))

    return dwg

def textwidth(text, fontsize, family):
    surface = cairo.SVGSurface('undefined.svg', 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face(family)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    return width

def score_semicircle(svg, position, radius, color):
    args = {'x0': position[0],
            'y0': position[1] - radius,
            'x1': position[0],
            'y1': position[1] + radius,
            'radius': radius,
    }
    path = """M %(x0)f,%(y0)f
              A %(radius)f,%(radius)f 0 0,0 %(x1)f,%(y1)f
    """ % args
    return svg.path(d=path, fill=color)

def draw_score(dwg, x, y, book, c):
    n = 5
    s = 5
    padding = 2*c.category_tip_radius + 0.5
    outer_radius = c.book_tip_radius
    inner_radius = outer_radius-0.6
    for i in range(1, 6):
        dwg.add(dwg.circle((x, y), r=outer_radius, fill=book.color))
        if i > math.floor(s/2):
            dwg.add(dwg.circle((x, y), r=inner_radius, fill=c.canvas_background_color))
            if i <= math.ceil(s/2):
                dwg.add(score_semicircle(dwg, (x,y), (inner_radius+outer_radius)/2, book.color))
        x += padding

def draw_book(dwg, book, c):
    # Line
    dwg.add(dwg.line((c.timeline_start_x, book.start_y), (c.timeline_end_x, book.finish_y), stroke=book.color, stroke_width=c.book_line_width))

    # Circles
    dwg.add(dwg.circle((c.timeline_start_x, book.start_y), r=c.book_tip_radius, fill=book.color))
    dwg.add(dwg.circle((c.timeline_end_x, book.finish_y), r=c.book_tip_radius, fill=book.color))

    # Title and subtitle
    dy = c.book_title_font_size * c.book_text_line_spacing
    text = dwg.text("", insert=(c.book_text_start_x, book.finish_y), dominant_baseline="central", font_family=c.book_text_font)
    text.add(dwg.tspan(book.title, font_weight='bold', font_size=str(c.book_title_font_size)+'px'))
    text.add(dwg.tspan(book.subtitle, x=[c.book_text_start_x], dy=[str(dy)+"px"], font_size=str(c.book_author_font_size)+'px'))
    print(textwidth(book.subtitle, c.book_author_font_size, c.book_text_font))
    dwg.add(text)
    score_x = c.book_text_start_x + textwidth(book.subtitle, c.book_author_font_size, c.book_text_font)
    score_y = book.finish_y + dy
    draw_score(dwg, score_x, score_y, book, c)
    
    return dwg
