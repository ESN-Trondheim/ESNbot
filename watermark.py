"""
A set of functions to help command_watermark()
"""

import zipfile
import os
from PIL import Image
import PIL.ImageOps

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

def calculate_ratio(start, overlay):
    """
    Calculates the ratio to be used when resizing the logo and white background.
    Also need the ratio to maintain proper aspect ratio of the logo.
    """
    factor = 5 if start.size[0] > start.size[1] else 3.75
    overlay_new_width = int(start.size[0] / factor)
    ratio = overlay_new_width / overlay.size[0]
    return ratio

def new_overlay_size(overlay, ratio):
    """
    Determines an appropriate size for the `overlay`, given the image in `start`.
    Currently the overlay will be 1/5 of the width, or 1/25 of the total size.
    Returns a tuple containing the new dimensions.
    """
    overlay_new_width = int(overlay.size[0] * ratio)
    overlay_new_height = int(overlay.size[1] * ratio)
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

def invert_bg(background):
    """
    Inverts the colors of the background for the logo. Only meant to be used if the user
    wants a white logo, as that won't be visible on a white background.
    """
    if background.mode == "RGBA":
        r, g, b, a = background.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted = PIL.ImageOps.invert(rgb_image)
        r, g, b = inverted.split()
        background = Image.merge("RGBA", (r, g, b, a))
    else:
        background = PIL.ImageOps.invert(background)
    return background

def watermark(start_img, argument, filename):
    """
    Watermarks `start_img` with the logo and position specified in `argument`, if any is specified.
    Default is colors and bottom right corner.
    Then saves the resulting image to `filename` in the same folder the script runs from.
    """
    white_bg = Image.open("bg.png")
    # Must calculate ratio from white background, the size looks best that way.
    ratio = calculate_ratio(start_img, white_bg)
    logo = Image.open("logo-" + get_overlay_color(argument) + ".png")
    if get_overlay_color(argument) == "white":
        white_bg = invert_bg(white_bg)

    white_bg = white_bg.resize(new_overlay_size(white_bg, ratio), Image.ANTIALIAS)
    logo = logo.resize(new_overlay_size(logo, ratio), Image.ANTIALIAS)

    valid_pos_white = valid_overlay_positions(start_img, white_bg)
    valid_pos_logo = valid_overlay_positions(start_img, logo)

    # Transpose the background if another corner that bottom right is selected.
    if get_overlay_position(argument) == "tl":
        white_bg = white_bg.transpose(Image.ROTATE_180)
    elif get_overlay_position(argument) == "tr":
        white_bg = white_bg.transpose(Image.FLIP_TOP_BOTTOM)
    elif get_overlay_position(argument) == "bl":
        white_bg = white_bg.transpose(Image.FLIP_LEFT_RIGHT)

    selected_pos_white = valid_pos_white.get(get_overlay_position(argument))
    selected_pos_logo = valid_pos_logo.get(get_overlay_position(argument))

    """if argument:
        position = positions.get(argument[0]) or positions['br'] #bottom right is default
    else:
        position = positions['br'] #bottom right is default"""

    start_img.paste(white_bg, selected_pos_white, white_bg)
    start_img.paste(logo, selected_pos_logo, logo)
    start_img.save(filename)

def extract(filename, path):
    """
    Extracts all files from a zip archive to `path`
    """
    with zipfile.ZipFile(filename) as myfile:
        myfile.extractall(path=path)

def compress(filename, path):
    """
    Compresses files found in `path` to a zip archive named `filename`
    The zip archive will have the same folder structure.
    """
    with zipfile.ZipFile(filename, mode="w") as my_zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                # To compress the images exactly as received, instead of adding all pictures to
                # path(watermarked_images). Not necessary to add an extra folder.
                # Now it will be saved as watermarked/files
                # instead of watermarked/watermarked_images/files
                arcname = os.path.join(root, file).replace(path + os.sep, "")
                print(arcname, flush=True)
                my_zip_file.write(os.path.join(root, file), arcname=arcname)

def watermark_folder(argument, path):
    """
    Watermarks all image files in folder specified in `path`
    with the options specifed in `argument`.

    :Returns:
    bool `supported_files`. True if all files were valid image files, False if not.
    """
    supported_files = True
    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                img = Image.open(os.path.join(root, file))
            except OSError:
                print("Could not open " + os.path.join(root, file), flush=True)
                os.remove(os.path.join(root, file))
                supported_files = False
                continue
            # print(os.path.join(root, file), flush=True)
            watermark(img, argument, os.path.join(root, file))
    return supported_files

def watermark_zip(argument, filename):
    """
    Extracts all files from zip archive `filename` to a directory.
    Then watermarks all image files found in the archive and
    compresses the new images to a new zip archive also named `filename`.
    The directory created earlier is then deleted.

    :Returns:
    bool `supported_files`. True if all files were valid image files, False if not.
    """
    path = "watermarked_images"
    extract(filename, path)
    os.remove(filename)
    print("Images extracted", flush=True)
    supported_files = watermark_folder(argument, path)
    compress(filename, path)
    delete_directory(path)
    return supported_files

def delete_directory(path):
    """
    Deletes a directory at `path` and all of its contents.
    """
    for root, dirs, files in os.walk(path, topdown=False):
        # topdown=False is necessary to delete files/folders in the proper order.
        for file in files:
            os.remove(os.path.join(root, file))
        for dir_name in dirs:
            os.rmdir(os.path.join(root, dir_name))
    os.rmdir(path)
    # shutil.rmtree(path) # This may actually be a lot better
