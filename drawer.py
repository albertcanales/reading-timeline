import svgwrite

books = [
    {
        'title': "The Plot",
        'author': "Jean Hanff Korelitz",
        'start_y': 10.6 + 47.61,
        'finish_y': 10.6 + 21.97,
    },
]

def draw(path):
    dwg = svgwrite.Drawing(path, (600, 5100), viewBox="0 0 158.75 1349.3751")
    dwg = draw_grid(dwg)
    for book in books:
        dwg = draw_book(dwg, book)
    dwg.save(pretty=True)

def draw_grid(dwg):
    # Vertical lines
    dwg.add(dwg.line((15.875, 3), (15.875, 5100), stroke='#e5e5e5', stroke_width=0.264))
    dwg.add(dwg.line((42.33, 3), (42.33, 5100), stroke='#e5e5e5', stroke_width=0.264))

    # Horizontal lines
    for i in range(5):
        dwg.add(dwg.line((10.6, 10.6 + 6.75 + 53*i), (10.6+31.75, 10.6 + 6.75 + 53*i), stroke='#e5e5e5', stroke_width=0.264))

    # Month labels
    for i in range(4):
        label = str(12-i) + "/22"
        pos = (1.06, 10.6 + 6.75 + 53*i + 53/2 + 4.23/2)
        dwg.add(dwg.text(label, insert=pos, font_style='italic', font_size='4.23px', fill='#666666'))

    # Date labels
    dy = 3.7 * 1.5

    text = dwg.text("", insert=(14.58, 10.6 - 3.85), font_style='italic', font_size='3.7px', fill='#808080', text_anchor='end')
    text.add(dwg.tspan('Date'))
    text.add(dwg.tspan('Started', x=[14.58], dy=[str(dy)+"px"]))
    dwg.add(text)

    text = dwg.text("", insert=(41.09, 10.6 - 3.85), font_style='italic', font_size='3.7px', fill='#808080', text_anchor='end')
    text.add(dwg.tspan('Date'))
    text.add(dwg.tspan('Finished', x=[41.09], dy=[str(dy)+"px"]))
    dwg.add(text)

    return dwg

def draw_book(dwg, book):
    # Circles
    dwg.add(dwg.circle((15.875, book['start_y']), r=1.72, fill="#2a7fff"))
    dwg.add(dwg.circle((42.33, book['finish_y']), r=1.72, fill="#2a7fff"))

    # Line
    dwg.add(dwg.line((15.875, book['start_y']), (42.33, book['finish_y']), stroke='#2a7fff', stroke_width=0.53))

    # Title and author
    dy = 4.23 * 1.25
    text = dwg.text("", insert=(46, book['finish_y']), dominant_baseline="central")
    text.add(dwg.tspan(book['title'], font_weight='bold', font_size='4.23px'))
    text.add(dwg.tspan(book['author'], x=[46], dy=[str(dy)+"px"], font_size='3.7px'))
    dwg.add(text)

    return dwg

draw('test.svg')