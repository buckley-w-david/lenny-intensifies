import numpy as np
from PIL import Image, ImageSequence
from scipy.ndimage import binary_opening, binary_closing

import lenny_intensifies


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

_gif_file = pkg_resources.open_binary(lenny_intensifies, 'lenny.gif')
gif = Image.open(_gif_file)

def generate_lenny_gif(face_img):
    frames = []
    duration = []
    structure = np.ones((3,3))

    face = face_img

    for frame in ImageSequence.Iterator(gif):
        converted_frame = frame.convert()
        im = frame.convert('1')
        height_adjust = int(im.height*0.15)
        roi = 1 - np.array(im.crop((0, height_adjust, im.width, im.height))) # Cut off top 15% and invert

        # Do morphological opening/closing, had some speckles and such that were messing with bbox
        opened = binary_opening(binary_closing(roi), structure=structure)
        im_opened = Image.fromarray(opened)

        l, u, r, b = im_opened.getbbox()
        width = r - l
        height = b - u
        centre = (l + width // 2, u + height // 2 + height_adjust)

        adjusted_face = face.copy()
        adjusted_face.thumbnail((width, height))

        adjusted_ul = (centre[0] - adjusted_face.width // 2, centre[1] - adjusted_face.height // 2)

        converted_frame.paste(adjusted_face, adjusted_ul)
        frames.append(converted_frame)
        duration.append(frame.info['duration'])

    return (frames, duration)
