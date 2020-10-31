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

def generate_lenny_gif(face_img, colour):
    frames = []
    duration = []
    structure = np.ones((3,3))

    face = face_img#.convert('RGB') # Chop of alpha channel
    base_intensity = 0

    # Make a red mask of the face for blending
    blend_arr = np.array(face)
    blanks = blend_arr[:, :, 3] == 0
    blend_arr[blend_arr[:, :, 3] != 0] = np.array([255, 0, 0, 255])
    blend = Image.fromarray(blend_arr)

    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        converted_frame = frame.convert()
        im = frame.convert('1')
        height_adjust = int(im.height*0.15)
        roi = 1 - np.array(im.crop((0, height_adjust, im.width, im.height))) # Cut off top 15% and invert

        # Do morphological opening/closing, had some speckles and such that were messing with bbox
        opened = binary_opening(binary_closing(roi), structure=structure)
        im_opened = Image.fromarray(opened)

        l, u, r, b = im_opened.getbbox()
        u += height_adjust
        b += height_adjust

        width = r - l
        height = b - u
        centre = (l + width // 2, u + height // 2)

        if colour:
            region = np.array(converted_frame.crop((l, u, r, b)))
            intensity = region[(region.sum(axis=2) != 1020)][:, 0].mean()
            if i == 0:
                base_intensity = intensity

            alpha = (intensity - base_intensity) / (350 - base_intensity)

            adjusted_face = Image.blend(face, blend, alpha)
        else:
            adjusted_face = face.copy()

        adjusted_face.thumbnail((width, height))

        adjusted_ul = (centre[0] - adjusted_face.width // 2, centre[1] - adjusted_face.height // 2)

        converted_frame.paste(adjusted_face, adjusted_ul, adjusted_face)
        frames.append(converted_frame)
        duration.append(frame.info['duration'])

    return (frames, duration)
