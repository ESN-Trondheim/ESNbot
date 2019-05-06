"""
A set of functions to help command_watermark()
"""

from PIL import Image

def get_overlay_color(argument):
    """
    Determines the color the user wants the watermark overlay to be.
    Returns a string containing said color.
    Returns "color" if no valid color can be found in `argument`.
    """
    if argument:
        if "black" in argument:
            return "black"
        elif "white" in argument:
            return "white"
    return "color"

def get_overlay_position(argument):
    """
    Determines the position the user wants the watermark overlay to be in.
    Returns a string containing the shorthand version of the four valied positions.
    Returns "br" if no valid position can be found in `argument`.
    """
    if argument:
        if "tl" in argument:
            return "tl"
        elif "tr" in argument:
            return "tr"
        elif "bl" in argument:
            return "bl"
    return "br"

def new_overlay_size(start, overlay):
    """
    Determines an appropriate size for the `overlay`, given the image in `start`.
    Currently the overlay will be 1/5 of the width, or 1/25 of the total size.
    Returns a tuple containing the new dimensions.
    """
    overlay_new_width = int(start.size[0] / 5)
    factor = overlay_new_width / overlay.size[0]
    overlay_new_height = int(overlay.size[1] * factor)
    return (overlay_new_width, overlay_new_height)

def valid_overlay_positions(start, overlay):
    """
    Determines the coordinates for all four possible `overlay` positions,
    one for each corner of the `start` image.
    The coordinates are the starting point (top left corner) of the `overlay`.
    Returns a dictionary with shorthand keys and tuples for all the coordinate-pairs.

    """
    position = {
        'tl': (0, 0),
        'tr': (start.size[0] - overlay.size[0], 0),
        'bl': (0, start.size[1] - overlay.size[1]),
        'br': (start.size[0] - overlay.size[0], start.size[1] - overlay.size[1])
    }
    return position

def watermark(start_img, argument, filename):
    """
    Watermarks `start_img` with the logo and position specified in `argument`, if any is specified.
    Default is colors and bottom left corner.
    Then saves the resulting image to `filename` in the same folder the script runs from.
    """
    overlay_img = Image.open("logo-" + get_overlay_color(argument) + ".png")
    overlay_img = overlay_img.resize(new_overlay_size(start_img, overlay_img), Image.ANTIALIAS)

    valid_positions = valid_overlay_positions(start_img, overlay_img)
    selected_position = valid_positions.get(get_overlay_position(argument))

    """if argument:
        position = positions.get(argument[0]) or positions['br'] #bottom right is default
    else:
        position = positions['br'] #bottom right is default"""

    start_img.paste(overlay_img, selected_position, overlay_img)
    start_img.save(filename)