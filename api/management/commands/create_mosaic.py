# -*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand

from api.lastfm import create_image_mosaic, get_user_top_albums_images


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-u', '--user', dest='user', action='store', type='string',
            help='Last.fm username to connect'),

        make_option(
            '-p', '--period', dest='period', action='store', default='6month',
            type='string',
            help='Last.fm period of data: 1month, 3month, 6month, year, overall'),

        make_option(
            '-l', '--limit', dest='limit', action='store', default=50,
            type='int', help='Limit of images to fetch'),

        make_option(
            '-t', '--thumbsize', dest='thumb_size', action='store',
            default='large', type='string',
            help='Thumb sizes: small, medium, large, extralarge'),

        make_option(
            '-W', '--width', dest='width', action='store',
            default=1260, type='int', help='Width of resultant image mosaic'),

        make_option(
            '-H', '--height', dest='height', action='store',
            default=630, type='int', help="Height of resultant image mosaic"),

        #make_option(
            #'--service', dest='service', action='store', default='lastfm',
            #type='string'),
        )

    def handle(self, *args, **options):

        if options['user']:
            images_urls = get_user_top_albums_images(options['user'],
                                                     options['period'],
                                                     options['limit'],
                                                     options['thumb_size'])
            return create_image_mosaic(images_urls,
                                       options['width'],
                                       options['height'])
        else:
            print 'You must to provide a username: \n' \
                  './manage.py -u <username>'
