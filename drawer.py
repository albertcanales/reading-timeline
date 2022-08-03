import svgwrite

books = [
    {
        'title': "The Plot",
        'author': "Jean Hanff Korelitz",
        'start_y': 10.6 + 47.61,
        'finish_y': 10.6 + 21.97,
    },
]

def draw(path, c, p):
    dwg = svgwrite.Drawing(path, (c.canvas_size_x, c.canvas_size_y), viewBox="0 0 158.75 1349.3751")
    dwg = draw_grid(dwg, c, p)
    for book in books:
        dwg = draw_book(dwg, book, c)
    dwg.save(pretty=True)

def draw_grid(dwg, c, p):
    # Vertical lines
    dwg.add(dwg.line((c.timeline_start_x, c.timeline_start_y), (c.timeline_start_x, c.canvas_size_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))
    dwg.add(dwg.line((c.timeline_end_x, c.timeline_start_y), (c.timeline_end_x, c.canvas_size_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))

    # Month labels and lines
    dwg.add(dwg.line((c.month_line_start_x, c.month_line_start_y), (c.timeline_end_x, c.month_line_start_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))
    for month in p.months:
        dwg.add(dwg.text(month.text, insert=(c.month_text_start_x, month.text_y), font_style='italic', font_size=str(c.month_text_font_size)+'px', fill=c.month_text_color))
        dwg.add(dwg.line((c.month_line_start_x, month.line_y), (c.timeline_end_x, month.line_y), stroke=c.timeline_line_color, stroke_width=c.timeline_line_width))

    # Date labels
    dy = c.date_text_font_size * c.date_text_line_spacing

    text = dwg.text("", insert=(c.date_started_start_x, c.date_text_start_y), font_style='italic', font_size=str(c.date_text_font_size)+'px', fill=c.date_text_color, text_anchor=c.date_text_anchor)
    text.add(dwg.tspan('Date'))
    text.add(dwg.tspan('Started', x=[c.date_started_start_x], dy=[str(dy)+"px"]))
    dwg.add(text)

    text = dwg.text("", insert=(c.date_finished_start_x, c.date_text_start_y), font_style='italic', font_size=str(c.date_text_font_size)+'px', fill=c.date_text_color, text_anchor=c.date_text_anchor)
    text.add(dwg.tspan('Date'))
    text.add(dwg.tspan('Finished', x=[c.date_finished_start_x], dy=[str(dy)+"px"]))
    dwg.add(text)

    return dwg

def draw_book(dwg, book, c):
    # Line
    dwg.add(dwg.line((c.timeline_start_x, book['start_y']), (c.timeline_end_x, book['finish_y']), stroke=c.book_line_color, stroke_width=c.book_line_width))

    # Circles
    dwg.add(dwg.circle((c.timeline_start_x, book['start_y']), r=c.book_tip_radius, fill=c.book_tip_color))
    dwg.add(dwg.circle((c.timeline_end_x, book['finish_y']), r=c.book_tip_radius, fill=c.book_tip_color))

    # Title and author
    dy = c.book_title_font_size * c.book_text_line_spacing
    text = dwg.text("", insert=(c.book_text_start_x, book['finish_y']), dominant_baseline="central")
    text.add(dwg.tspan(book['title'], font_weight='bold', font_size=str(c.book_title_font_size)+'px'))
    text.add(dwg.tspan(book['author'], x=[c.book_text_start_x], dy=[str(dy)+"px"], font_size=str(c.book_author_font_size)+'px'))
    dwg.add(text)

    return dwg
