"""
A script to automate the creation of cover photos for Facebook
TODO default to an image if no image is suppplied
"""

import pathlib
from PIL import Image, ImageDraw, ImageFont
from common import resize_background, ESN_COLORS, get_color, get_title


FACEBOOK_DIMENSIONS = (1568, 588)
ESN_ACTIVITIES_DIMENSIONS = (1920, 460)

DEFAULT_BACKGROUND = pathlib.Path.cwd().joinpath(
    "assets", "default_background.png")
LOGOS = {
    "regular": Image.open(pathlib.Path.cwd().joinpath("esnbot", "assets", "overlay_regular.png")),
    "activities": Image.open(pathlib.Path.cwd().joinpath("esnbot", "assets", "overlay_activities.png")),
    "buddy": Image.open(pathlib.Path.cwd().joinpath("esnbot", "assets", "overlay_buddy.png"))
}
FONTS = {  # Fonts to be used for overlayed text. Converting path to str, truetype doesn't accept path object
    "title": ImageFont.truetype(str(pathlib.Path.cwd().joinpath("esnbot", "assets", "Kelson Sans Bold.otf")), 90),
    "subtitle": ImageFont.truetype(str(pathlib.Path.cwd().joinpath("esnbot", "assets", "Kelson Sans Bold.otf")), 50)
}
V_OFFFSETS = {  # Vertical offsets of text to be overlayed
    "regular": {
        "title": - 6,
        "titleonly": - 6 + 25,  # Offset a bit more when only title
        "subtitle": 90,
        "subtitle2": 152
    },
    "buddy": {
        "title": - 6 + 44,
        "titleonly": - 6 + 25 + 42,  # Offset a bit more when only title
        "subtitle": 90 + 46,
        "subtitle2": 152 + 46
    },
    "activities": {
        "title": - 6,
        "titleonly": - 6 + 25,  # Offset a bit more when only title
        "subtitle": 70 + 46,
        "subtitle2": 132 + 46
    }
}


def create_color_overlay(background, color, dimensions):
    img = Image.new(background.mode, dimensions, color["rgb"])
    return img


def blend_color(background, color, dimensions):
    overlay = create_color_overlay(background, color, dimensions)
    blended_img = Image.blend(background, overlay, 0.60)
    return blended_img


def overlay_images(background, overlay):
    # TODO figure out this mess. I think it's actually most simple to just switch mode. alpha_composite requires both images to have an alpha channel
    background = background.convert(mode="RGB")
    # background.mode = "RGB" # necessary to get proper antialiasing on overlay when background is png/rgba
    background.paste(overlay, (0, 0), overlay)
    # background = Image.alpha_composite(background, overlay) # this is simpler, and works just as good
    return background


def overlay_text(background, text, font, offset):
    draw = ImageDraw.Draw(background)
    width, height = draw.textsize(text, font)
    draw.text(((background.size[0] - width) / 2,
              (background.size[1] - height) / 2 + offset), text, font=font)


def create_coverphoto(background, filename, argument):

    buddy = False  # Turn off buddy overlay - it's against visual identity guidelines
    dimensions = ESN_ACTIVITIES_DIMENSIONS if "activities" in argument else FACEBOOK_DIMENSIONS
    color = get_color(argument)
    color = ESN_COLORS.get(color, ESN_COLORS["blue"])

    title, subtitle, subtitle2 = get_title(argument)
    background = resize_background(background, dimensions)
    logos = "activities" if "activities" in argument else "regular"
    cover = overlay_images(blend_color(
        background, color, dimensions), LOGOS[logos])
    if subtitle or subtitle2:
        overlay_text(cover, title, FONTS["title"], V_OFFFSETS[logos]["title"])
        overlay_text(cover, subtitle,
                     FONTS["subtitle"], V_OFFFSETS[logos]["subtitle"])
        overlay_text(cover, subtitle2,
                     FONTS["subtitle"], V_OFFFSETS[logos]["subtitle2"])
    else:
        overlay_text(cover, title, FONTS["title"],
                     V_OFFFSETS[logos]["titleonly"])
    cover.save(filename, quality=95)  # quality only affects jpg images


def open_background_img(filename):
    try:
        background = Image.open(filename)
        ext = filename.split(".")[-1]
    except OSError:
        background = Image.open(DEFAULT_BACKGROUND)
        ext = background.format
    return background, ext
