"""
A script to automate the creation of cover photos for Facebook
TODO default to an image if no image is suppplied
"""

from PIL import Image, ImageDraw, ImageFont

ESN_COLORS = {
    "cyan": {
        "name": "cyan",
        "rgb": (0, 174, 239) #00aeef
    },
    "magenta": {
        "name": "magenta",
        "rgb": (236, 0, 140) #ec008c
    },
    "green": {
        "name": "green",
        "rgb": (122, 193, 67) #7ac143
    },
    "orange": {
        "name": "orange",
        "rgb": (244, 123, 32) #f47b20
    },
    "blue": { # proper name is dark blue
        "name": "dark blue",
        "rgb": (46, 49, 146) #2e3192
    }
}
DIMENSIONS = (1568, 588)
ASPECT_RATIO = DIMENSIONS[0] / DIMENSIONS[1]
DEFAULT_BACKGROUND = "default_background.png"
LOGOS = {
    "regular": Image.open("overlay_regular.png"),
    "buddy": Image.open("overlay_buddy.png")
}
FONTS = { #Fonts to be used for overlayed text
    "title": ImageFont.truetype("Kelson Sans Bold.otf", 90),
    "subtitle": ImageFont.truetype("Kelson Sans Bold.otf", 50)
}
V_OFFFSETS = { # Vertical offsets of text to be overlayed
    "regular": {
        "title": - 6,
        "titleonly": - 6 + 25, # Offset a bit more when only title
        "subtitle": 90,
        "subtitle2": 152
    },
    "buddy": {
        "title": - 6 + 44,
        "titleonly": - 6 + 25 + 42, # Offset a bit more when only title
        "subtitle": 90 + 46,
        "subtitle2": 152 + 46
    }
}

def create_color_overlay(background, color):
    img = Image.new(background.mode, DIMENSIONS, color["rgb"])
    return img

def blend_color(background, color):
    overlay = create_color_overlay(background, color)
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
    draw.text(((background.size[0] - width) / 2, (background.size[1] - height) / 2 + offset), text, font=font)

def get_color(argument):
    if argument:
        args = (" ").join(argument).split("\"")[0] # Only care about what's before titles
        # if "all" in args:
        #     pass
        for color_key in ESN_COLORS:
            if color_key in args:
                return color_key
    return "blue"

def get_title(argument):
    title = "Title"
    subtitle = ""
    subtitle2 = ""
    if argument:
        # for index, word in enumerate(argument):
        #     if word.startswith("“"):
        #         argument[index] = word.replace("“", "\"")
        #     elif word.endswith("”"):
        #         argument[index] = word.replace("”", "\"")
        argument = " ".join(argument)
        # I think the below is clearer than above, though it might not cover weird edge cases.
        # I still think this is better.
        argument = argument.replace("“", "\"")
        argument = argument.replace("”", "\"")
        # https://stackoverflow.com/questions/2076343/extract-string-from-between-quotations
        # Extracts every other item from the list, starting at index 1.
        # Example:
        # >>> foo = 'cyan "Title is here" not title "Subtitle" "Second subtitle"'
        # >>> foo_split = foo.split("\"")
        # >>> foo_split
        # ['cyan ', 'Title is here', ' not title ', 'Subtitle', ' ', 'Second subtitle', '']
        # >>> foo_split[1::2]
        # ['Title is here', 'Subtitle', 'Second subtitle']
        # Should always work if the number of quotes is even, even if
        # the titles/subtitles don't come directly after each other.
        # Still returns something if the number of quotes is odd,
        # but may not return what the user is expecting. This is an input error from the user.
        titles = argument.split("\"")[1::2]
        print(titles)
        try:
            title = titles[0]
        except IndexError:
            pass
        try:
            subtitle = titles[1]
        except IndexError:
            pass
        try:
            subtitle2 = titles[2]
        except IndexError:
            pass
    return title, subtitle, subtitle2

def create_coverphoto(background, filename, argument):
    buddy = False
    if "buddy" in argument:
    # Should it be
    # if "buddy" in (" ").join(argument).split("\"")[0]:
    # ? Does it matter?
        buddy = True

    color = get_color(argument)
    color = ESN_COLORS.get(color, ESN_COLORS["blue"])

    title, subtitle, subtitle2 = get_title(argument)
    background = resize_background(background)
    logos = "buddy" if buddy else "regular"
    cover = overlay_images(blend_color(background, color), LOGOS[logos])
    if subtitle or subtitle2:
        overlay_text(cover, title, FONTS["title"], V_OFFFSETS[logos]["title"])
        overlay_text(cover, subtitle, FONTS["subtitle"], V_OFFFSETS[logos]["subtitle"])
        overlay_text(cover, subtitle2, FONTS["subtitle"], V_OFFFSETS[logos]["subtitle2"])
    else:
        overlay_text(cover, title, FONTS["title"], V_OFFFSETS[logos]["titleonly"])
    cover.save(filename, quality=95) #quality only affects jpg images

def open_background_img(filename):
    try:
        background = Image.open(filename)
        ext = filename.split(".")[-1]
    except OSError:
        background = Image.open(DEFAULT_BACKGROUND)
        ext = DEFAULT_BACKGROUND.split(".")[-1]
    return background, ext

def resize_background(background):
    if background.size == DIMENSIONS:
        return background
    if background.size[0] < DIMENSIONS[0] / 1.33 or background.size[1] < DIMENSIONS[1] / 1.33:
        print("Resolution is low. You will get a better result if you have an image with higher resolution.")
    background_aspect_ratio = background.size[0] / background.size[1]
    # TODO the following could probably be a function instead of two almost identical blocks of code
    if background_aspect_ratio <= ASPECT_RATIO: # background is taller
        print("bg aspect <= aspect ratio")
        print(background_aspect_ratio)
        resize_ratio = background.size[0] / DIMENSIONS[0]
        new_height = int(background.size[1] / resize_ratio)
        print(background.size)
        background = background.resize((DIMENSIONS[0], new_height), Image.ANTIALIAS)
        print(background.size)
        if background.size[1] > DIMENSIONS[1]:
            padding = (background.size[1] - DIMENSIONS[1]) / 2
            coords = (0, padding, DIMENSIONS[0], background.size[1] - padding)
            background = background.crop(coords)
            print(background.size)
    else: # background is wider
        print("bg aspect > aspect ratio")
        resize_ratio = background.size[1] / DIMENSIONS[1]
        new_width = int(background.size[0] / resize_ratio)
        print(background.size)
        background = background.resize((new_width, DIMENSIONS[1]), Image.ANTIALIAS)
        print(background.size)
        if background.size[0] > DIMENSIONS[0]:
            padding = (background.size[0] - DIMENSIONS[0]) / 2
            coords = (padding, 0, background.size[0] - padding, DIMENSIONS[1])
            background = background.crop(coords)
            print(background.size)
    return background
