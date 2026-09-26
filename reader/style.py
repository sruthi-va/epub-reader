def get_theme_colors(theme):
    themes = {
        "light": {
            "background": "#ffffff",
            "text": "#222222",
        },
        "sepia": {
            "background": "#f4ecd8",
            "text": "#433422",
        },
        "dark": {
            "background": "#181818",
            "text": "#e6e6e6",
        },
    }

    return themes.get(
        theme,
        themes["light"],
    )


def build_reader_css(settings):
    colors = get_theme_colors(settings.theme)

    return f"""
        body {{
            background-color: {colors["background"]};
            color: {colors["text"]};
            font-family: "{settings.font_family}";
            font-size: {settings.font_size}px;
            line-height: {settings.line_spacing};
            max-width: {settings.text_width}px;
            margin: 0 auto;
            padding: 60px 30px;
        }}

        p {{
            margin-bottom: 1em;
        }}

        img {{
            max-width: 100%;
            height: auto;
        }}

        h1, h2, h3, h4 {{
            margin-top: 1.5em;
            margin-bottom: 0.75em;
        }}
    """
def apply_reader_style(content, settings):
    css = build_reader_css(settings)

    style_tag = f"""
    <style>
    {css}
    </style>
    """

    if "</head>" in content:
        return content.replace(
            "</head>",
            style_tag + "</head>",
            1,
        )

    return f"""
    <html>
    <head>
        {style_tag}
    </head>
    <body>
        {content}
    </body>
    </html>
    """