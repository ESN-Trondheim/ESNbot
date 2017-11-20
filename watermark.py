"""
A set of functions to help command_watermark()
"""

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
