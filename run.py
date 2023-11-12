from skimage import io
import math
from decimal import Decimal
import click
import os
import logging
import sys


def crop_image(
    path,
    *,
    top: int,
    left: int,
    right: int,
    bottom: int,
    h_padding: int,
    ratio: Decimal,
):
    # pillow_heif has to be installed
    import pillow_heif

    assert top < bottom
    assert left < right

    img = io.imread(path)
    logging.info("shape %s", img.shape)

    width, height = right - left, bottom - top

    # eq: (width + 2*h_padding) / (height + 2*v_padding) = ratio
    v_padding = ((width + 2 * h_padding) / ratio - height) / 2
    v_padding = int(v_padding)

    result_width = Decimal(width + 2 * h_padding)
    result_height = Decimal(height + 2 * v_padding)
    assert math.isclose(result_width / result_height, ratio, rel_tol=1e-3), (
        result_width,
        result_height,
        ratio,
    )

    logging.info("h_padding %s, v_padding %s", h_padding, v_padding)

    result = img[
        top - v_padding : bottom + v_padding,
        left - h_padding : right + h_padding,
    ]

    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join("cropped", f"{name}.png")
    io.imsave(output_path, result)


@click.command
@click.option("--roi-top", type=int)
@click.option("--roi-bottom", type=int)
@click.option("--roi-left", type=int)
@click.option("--roi-right", type=int)
@click.option("--h-padding", type=int)
@click.option("--ratio", nargs=2, type=int)
@click.argument("paths", nargs=-1)
def main(
    paths, roi_top, roi_left, roi_right, roi_bottom, h_padding, ratio: tuple[int, int]
):
    logging.basicConfig(level=logging.DEBUG)
    for path in paths:
        logging.info("cropping %s", path)
        crop_image(
            path,
            left=roi_left,
            right=roi_right,
            bottom=roi_bottom,
            top=roi_top,
            h_padding=h_padding,
            ratio=Decimal(ratio[0]) / Decimal(ratio[1]),
        )


if __name__ == "__main__":
    main()
