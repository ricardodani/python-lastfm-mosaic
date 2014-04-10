from django.test import TestCase

from lastfm import create_image_mosaic, get_user_top_albums_images


class APITest(TestCase):
    def test_api(self):
    # available periods: overall | 7day | 1month | 3month | 6month | 12month
        create_image_mosaic(
            get_user_top_albums_images('ricardodani', '6month'))
