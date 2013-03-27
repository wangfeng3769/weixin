DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'leyingke',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            },
        },
#    'lykcbk': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': '',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#        'OPTIONS': {
#            #'init_command': 'SET storage_engine=INNODB',
#        },
#        },
    }
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '',
        'TIMEOUT': 3600,
        'OPTIONS': {
            'DB': 4,
            'MAX_ENTRIES': 10000,
            },
        },
    }
REDIS_HOST = ''
REDIS_PORT = 6379
MEDIA_ROOT = ''
