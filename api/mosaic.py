# -*- coding: utf-8 -*-

import uuid
from cStringIO import StringIO
from PIL import Image

from octopus import TornadoOctopus


def _download_url_list(image_url_list):
    '''Downloads the image sources of images listed on `image_url_list`
    '''

    images = []

    otto = TornadoOctopus(
        concurrency=50, auto_start=True, cache=True, expiration_in_seconds=60
    )

    def handle_url_response(url, response):
        if 'Not found' == response.text:
            print url
        else:
            images.append(response.text)

    for url in image_url_list:
        otto.enqueue(url, handle_url_response)

    otto.wait(0)

    return images


def create_image_mosaic(image_url_list, width=1260, height=800):
    '''Download and manipulates the images of `image_url_list`
    to creates a mosaic with them
    '''

    images = _download_url_list(image_url_list)

    out_img = Image.new('RGB', (width, height))
    x, y = 0, 0

    for i, img in enumerate(images):
        thumb = Image.open(StringIO(img))
        out_img.paste(thumb, (y * thumb.size[0], x * thumb.size[1]))
        if (i + 1) % (width / thumb.size[0]) == 0:
            x += 1
            y = 0
        else:
            y += 1

    image_location = 'static/mosaics/%s.png' % uuid.uuid4()
    out_img.save(image_location)
    return image_location
