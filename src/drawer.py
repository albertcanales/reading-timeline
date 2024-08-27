import svgwrite


def draw(path, prms, proc):
    dwg = svgwrite.Drawing(
        path,
        (prms.canvas_size_x, proc.canvas_size_y * prms.canvas_zoom),
        viewBox="0 0 %d %d"
        % (prms.canvas_size_x / prms.canvas_zoom, proc.canvas_size_y),
        style="background-color:%s" % prms.canvas_background_color,
    )
    dwg = draw_grid(dwg, prms, proc)
    for font in prms.fonts:
        dwg.embed_font(name=font.name, filename=font.filename)
    for category in proc.categories:
        dwg = draw_category(dwg, category, prms, proc)
    for book in proc.books:
        dwg = draw_book(dwg, book, prms)
    dwg.save(pretty=True)


def draw_grid(dwg, prms, proc):
    # Vertical lines
    dwg.add(
        dwg.line(
            (prms.timeline_start_x, prms.timeline_start_y),
            (prms.timeline_start_x, proc.timeline_end_y),
            stroke=prms.timeline_line_color,
            stroke_width=prms.timeline_line_width,
        )
    )
    dwg.add(
        dwg.line(
            (prms.timeline_end_x, prms.timeline_start_y),
            (prms.timeline_end_x, proc.timeline_end_y),
            stroke=prms.timeline_line_color,
            stroke_width=prms.timeline_line_width,
        )
    )

    # Month labels and lines
    dwg.add(
        dwg.line(
            (prms.month_line_start_x, prms.month_line_start_y),
            (prms.timeline_end_x, prms.month_line_start_y),
            stroke=prms.timeline_line_color,
            stroke_width=prms.timeline_line_width,
        )
    )
    for month in proc.months:
        dwg.add(
            dwg.text(
                month.text,
                insert=(prms.month_text_start_x, month.text_y),
                font_style="italic",
                font_size=str(prms.month_text_font_size) + "px",
                font_family=prms.month_text_font,
                fill=prms.month_text_color,
            )
        )
        dwg.add(
            dwg.line(
                (prms.month_line_start_x, month.line_y),
                (prms.timeline_end_x, month.line_y),
                stroke=prms.timeline_line_color,
                stroke_width=prms.timeline_line_width,
            )
        )

    # Date labels
    dy = prms.date_text_font_size * prms.date_text_line_spacing

    text = dwg.text(
        "",
        insert=(prms.date_started_start_x, prms.date_text_start_y),
        font_style="italic",
        font_size=str(prms.date_text_font_size) + "px",
        font_family=prms.date_text_font,
        fill=prms.date_text_color,
        text_anchor=prms.date_text_anchor,
    )
    text.add(dwg.tspan("Date"))
    text.add(dwg.tspan("Started", x=[prms.date_started_start_x], dy=[str(dy) + "px"]))
    dwg.add(text)

    text = dwg.text(
        "",
        insert=(prms.date_finished_start_x, prms.date_text_start_y),
        font_style="italic",
        font_size=str(prms.date_text_font_size) + "px",
        font_family=prms.date_text_font,
        fill=prms.date_text_color,
        text_anchor=prms.date_text_anchor,
    )
    text.add(dwg.tspan("Date"))
    text.add(dwg.tspan("Finished", x=[prms.date_finished_start_x], dy=[str(dy) + "px"]))
    dwg.add(text)

    return dwg


def draw_category(dwg, category, prms, proc):
    # Line
    dwg.add(
        dwg.line(
            (prms.category_line_start_x, category.start_y),
            (proc.category_line_end_x, category.start_y),
            stroke=category.color,
            stroke_width=prms.category_line_width,
        )
    )

    # Circle
    dwg.add(
        dwg.circle(
            (proc.category_line_end_x, category.start_y),
            r=prms.category_tip_radius,
            fill=category.color,
        )
    )

    # Category name
    dwg.add(
        dwg.text(
            category.name,
            insert=(proc.category_text_start_x, category.start_y),
            font_size=str(prms.category_text_font_size) + "px",
            fill=prms.category_text_color,
            dominant_baseline="middle",
            font_family=prms.category_text_font,
        )
    )

    return dwg


# Helper function to draw half points on scores
def score_semicircle(dwg, position, radius, color):
    args = {
        "x0": position[0],
        "y0": position[1] - radius,
        "x1": position[0],
        "y1": position[1] + radius,
        "radius": radius,
    }
    path = (
        """M %(x0)f,%(y0)f
              A %(radius)f,%(radius)f 0 0,0 %(x1)f,%(y1)f
    """
        % args
    )
    return dwg.path(d=path, fill=color)


def draw_score(dwg, x, y, book, prms):
    padding = 2 * prms.category_tip_radius + prms.book_score_padding
    for i in range(1, 6):
        dwg.add(
            dwg.circle((x, y), r=prms.book_score_outer_radius, fill=book.score_color)
        )
        if i > book.score:
            dwg.add(
                dwg.circle(
                    (x, y),
                    r=prms.book_score_inner_radius,
                    fill=prms.canvas_background_color,
                )
            )
            if i < book.score + 1:
                radius = (
                    prms.book_score_outer_radius + prms.book_score_inner_radius
                ) / 2
                dwg.add(score_semicircle(dwg, (x, y), radius, book.score_color))
        x += padding


def draw_book(dwg, book, prms):
    # Line
    dwg.add(
        dwg.line(
            (prms.timeline_start_x, book.start_y),
            (prms.timeline_end_x, book.finish_y),
            stroke=book.color,
            stroke_width=prms.book_line_width,
        )
    )

    # Circles
    dwg.add(
        dwg.circle(
            (prms.timeline_start_x, book.start_y),
            r=prms.book_tip_radius,
            fill=book.color,
        )
    )
    dwg.add(
        dwg.circle(
            (prms.timeline_end_x, book.finish_y),
            r=prms.book_tip_radius,
            fill=book.color,
        )
    )

    # Title and subtitle
    dy = prms.book_title_font_size * prms.book_text_line_spacing
    style = "italic" if book.link is not None else "normal"
    text = dwg.text(
        "",
        insert=(prms.book_text_start_x, book.finish_y),
        dominant_baseline="central",
        font_family=prms.book_text_font,
        fill=prms.book_text_color,
        font_style=style,
    )
    text.add(
        dwg.tspan(
            book.title,
            font_weight="bold",
            font_size=str(prms.book_title_font_size) + "px",
        )
    )
    text.add(
        dwg.tspan(
            book.subtitle,
            x=[prms.book_text_start_x],
            dy=[str(dy) + "px"],
            font_size=str(prms.book_author_font_size) + "px",
        )
    )

    # Link
    if book.link is not None:
        link = dwg.add(dwg.a(book.link))
        link.add(text)
    else:
        dwg.add(text)

    # Score
    if book.score is not None:
        draw_score(dwg, book.score_x, book.finish_y + dy, book, prms)

    return dwg
