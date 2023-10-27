from PIL import Image, ImageDraw, ImageFont
from common import resize_background, get_title, get_color

ESN_COLORS = {
    "cyan": {
        "name": "cyan",
        "rgb": (0, 174, 239)  # 00aeef
    },
    "magenta": {
        "name": "magenta",
        "rgb": (236, 0, 140)  # ec008c
    },
    "green": {
        "name": "green",
        "rgb": (122, 193, 67)  # 7ac143
    },
    "orange": {
        "name": "orange",
        "rgb": (244, 123, 32)  # f47b20
    },
    "blue": {  # proper name is dark blue
        "name": "dark blue",
        "rgb": (46, 49, 146)  # 2e3192
    }
}

OVERLAYS = {
    "fade": Image.open("fade.png"),
    "star": Image.open("star.png")
}

V_OFFSET = {
    "header": 125,
    "bottomtext": 1000,
    "image": 950
}

FONTS = {  # Fonts to be used for overlayed text
    "title": ImageFont.truetype("Kelson Sans Bold.otf", 90),
    "subtitle": ImageFont.truetype("Lato-Regular.ttf", 55)
}

LINE_SPACING = {
    "header": 125,
    "subtitle": 85
}


DIMENSIONS = (1080, 1920)

DEFAULT_BACKGROUND = "default_background.png"


def create_color_overlay(color, dimensions):
    img = Image.new("RGBA", dimensions, color["rgb"])
    return img


def blend_color(color, dimensions):
    color = create_color_overlay(color, dimensions)
    alpha = OVERLAYS["fade"].getchannel('A')
    color.putalpha(alpha)
    return color


def get_hcentered(y):
    return ((DIMENSIONS[0]) / 2, y)

# returns the y value of the first new line after the text


def draw_text(image, y_position, text, font, line_spacing=LINE_SPACING["subtitle"]):
    if text == "":
        return y_position
    text = text.upper()
    lines = text.split("\n")

    draw = ImageDraw.Draw(image)

    y = 0
    for i, line in enumerate(lines):
        y = y_position + i * line_spacing
        xy = get_hcentered(y)
        dims = draw.textbbox(xy, line, font=font, anchor="mm", align="center")
        text_x, text_y = dims[0], dims[1]
        draw.text((text_x, text_y), line, font=font)

    return y + line_spacing


def parse_arguments(argument):
    color = get_color(argument)
    color = ESN_COLORS.get(color, ESN_COLORS["blue"])

    title, subtitle, subtitle2 = get_title(argument)
    return color, title, subtitle, subtitle2


def generate_story(background, color, header, toptext, bottomtext):
    img = Image.new("RGBA", DIMENSIONS, 0)

    # Paste image

    # resize background, keep aspect
    background = resize_background(
        background, (1080, 1920 - V_OFFSET["image"]))
    background = background.convert("RGBA")

    img.paste(background, (0, V_OFFSET["image"]), background)

    # Paste faded color overlay
    color_overlay = blend_color(color, DIMENSIONS)
    img = Image.alpha_composite(img, color_overlay)
    # img.paste(color_overlay, (0, 0), color_overlay)

    # Paste ESN star
    img = Image.alpha_composite(img, OVERLAYS["star"])

    # Draw header and save position of next line
    next_position = draw_text(
        img, V_OFFSET["header"], header, FONTS["title"], LINE_SPACING["header"])
    # Draw subtitle
    draw_text(img, next_position, toptext, FONTS["subtitle"])
    # Draw text under ESN star
    draw_text(img, V_OFFSET["bottomtext"], bottomtext, FONTS["subtitle"])

    header_in_filename = header.replace(" ", "_").replace("\n", "_").lower()
    filename = f"ig_story_{header_in_filename}.png"
    img.save(filename)
    return filename


def create_story(background_image, argument):
    color, header, toptext, bottomtext = parse_arguments(argument)
    header = header.replace("::", "\n")
    toptext = toptext.replace("::", "\n")
    bottomtext = bottomtext.replace("::", "\n")
    return generate_story(background_image, color, header, toptext, bottomtext)
