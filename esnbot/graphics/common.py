from PIL import Image

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


def resize_background(background, dimensions):
    if background.size == dimensions:
        return background
    if background.size[0] < dimensions[0] / 1.33 or background.size[1] < dimensions[1] / 1.33:
        print("Resolution is low. You will get a better result if you have an image with higher resolution.")
    background_aspect_ratio = background.size[0] / background.size[1]
    # TODO the following could probably be a function instead of two almost identical blocks of code
    aspect_ratio = dimensions[0] / dimensions[1]
    if background_aspect_ratio <= aspect_ratio:  # background is taller
        print("bg aspect <= aspect ratio")
        print(background_aspect_ratio)
        resize_ratio = background.size[0] / dimensions[0]
        new_height = int(background.size[1] / resize_ratio)
        print(background.size)
        background = background.resize(
            (dimensions[0], new_height), Image.ANTIALIAS)
        print(background.size)
        if background.size[1] > dimensions[1]:
            padding = (background.size[1] - dimensions[1]) / 2
            coords = (0, padding, dimensions[0], background.size[1] - padding)
            background = background.crop(coords)
            print(background.size)
    else:  # background is wider
        print("bg aspect > aspect ratio")
        resize_ratio = background.size[1] / dimensions[1]
        new_width = int(background.size[0] / resize_ratio)
        print(background.size)
        background = background.resize(
            (new_width, dimensions[1]), Image.ANTIALIAS)
        print(background.size)
        if background.size[0] > dimensions[0]:
            padding = (background.size[0] - dimensions[0]) / 2
            coords = (padding, 0, background.size[0] - padding, dimensions[1])
            background = background.crop(coords)
            print(background.size)
    return background


def get_color(argument):
    if argument:
        # Only care about what's before titles
        args = (" ").join(argument).split("\"")[0]
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
        argument = argument.replace("«", "\"")
        argument = argument.replace("»", "\"")
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
