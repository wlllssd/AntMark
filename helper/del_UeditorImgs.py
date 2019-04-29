import django
from django.conf import settings
import os
import fnmatch

import sys
sys.path.append('..')


def load_setting():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'AntMark.settings'
    django.setup()

def main():
    load_setting()
    from commodity.models import Commodity
    img_folder = os.path.join(settings.MEDIA_ROOT, 'ueditorImages')

    patterns = ['*.jpg', '*.png', '*.gif']
    imgs_del = 0
    imgs_count = 0

    for root, dirs, files in os.walk(img_folder):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                if Commodity.objects.filter(body__contains = filename).count() == 0:
                    img_path = os.path.join(root, filename)
                    print('del: ', img_path)
                    os.remove(img_path)
                    imgs_del += 1
                imgs_count += 1
    print('has %s images, delete %s images'%(imgs_count, imgs_del))

if __name__ == '__main__':
    main()