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

OVERLAYS = {
  "fade": Image.open("fade.png"),
  "star": Image.open("star.png")
}

V_OFFSET = {
  "header": 125,
  "bottomtext": 1000,
  "image": 950
}

FONTS = { # Fonts to be used for overlayed text
    "title": ImageFont.truetype("Kelson Sans Bold.otf", 90),
    "subtitle": ImageFont.truetype("Kelson Sans Bold.otf", 50)
}

LINE_SPACING = {
    "header": 125,
    "subtitle": 85
}


DIMENSIONS = (1080, 1920)

DEFAULT_BACKGROUND = "default_background.png"

def resize_background(background, dimensions):
    if background.size == dimensions:
        return background
    if background.size[0] < dimensions[0] / 1.33 or background.size[1] < dimensions[1] / 1.33:
        print("Resolution is low. You will get a better result if you have an image with higher resolution.")
    background_aspect_ratio = background.size[0] / background.size[1]
    # TODO the following could probably be a function instead of two almost identical blocks of code
    aspect_ratio = dimensions[0] / dimensions[1]
    if background_aspect_ratio <= aspect_ratio: # background is taller
        print("bg aspect <= aspect ratio")
        print(background_aspect_ratio)
        resize_ratio = background.size[0] / dimensions[0]
        new_height = int(background.size[1] / resize_ratio)
        print(background.size)
        background = background.resize((dimensions[0], new_height), Image.ANTIALIAS)
        print(background.size)
        if background.size[1] > dimensions[1]:
            padding = (background.size[1] - dimensions[1]) / 2
            coords = (0, padding, dimensions[0], background.size[1] - padding)
            background = background.crop(coords)
            print(background.size)
    else: # background is wider
        print("bg aspect > aspect ratio")
        resize_ratio = background.size[1] / dimensions[1]
        new_width = int(background.size[0] / resize_ratio)
        print(background.size)
        background = background.resize((new_width, dimensions[1]), Image.ANTIALIAS)
        print(background.size)
        if background.size[0] > dimensions[0]:
            padding = (background.size[0] - dimensions[0]) / 2
            coords = (padding, 0, background.size[0] - padding, dimensions[1])
            background = background.crop(coords)
            print(background.size)
    return background

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

def create_story(background, color, header, toptext, bottomtext):
    img = Image.new("RGBA", DIMENSIONS, 0)

    # Paste image
    
    # resize background, keep aspect
    background = resize_background(background, (1080, 1920 - V_OFFSET["image"]))
    background = background.convert("RGBA")


    img.paste(background, (0, V_OFFSET["image"]), background)

    # Paste faded color overlay
    color_overlay = blend_color(color, DIMENSIONS)
    img.paste(color_overlay, (0, 0), color_overlay)

    # Paste ESN star
    img.paste(OVERLAYS["star"], (0, 0), OVERLAYS["star"])
    
    # Draw header and save position of next line
    next_position = draw_text(img, V_OFFSET["header"], header, FONTS["title"], LINE_SPACING["header"])
    # Draw subtitle
    draw_text(img, next_position, toptext, FONTS["subtitle"])
    # Draw text under ESN star
    draw_text(img, V_OFFSET["bottomtext"], bottomtext, FONTS["subtitle"])

    img.save("test.png")

img = Image.open("stock.jpg")
#create_story(img, ESN_COLORS["green"], "join us this\nwednesday\nfor\nbuddy kickoff", "", "We will see you there")
#create_story(img, ESN_COLORS["magenta"], "Summary", "What: Buddy kickoff\nWhere: Høgskoleparken\nFood: Hot dogs in lompe\nWhen: Wednesday at 19.00\n Ticket: free, no sign up needed", "We will see you there")
create_story(img, ESN_COLORS["magenta"], "join us this\nwednesday\nfor\nbuddy kickoff", "", "We will see you there")