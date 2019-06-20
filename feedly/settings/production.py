from .base import *
import dj_database_url

DEBUG = os.environ.get('DEBUG')

DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')





# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

