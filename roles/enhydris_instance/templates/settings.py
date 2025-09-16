{% if enhydris_version >= '2.2' %}
from enhydris_project.settings import *
{% else %}
from enhydris.settings import *
{% endif %}

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['{{ site_domain }}']
ADMINS = (
{% for admin in admins %}
    ('{{ admin.name }}', '{{ admin.email }}'),
{% endfor %}
)
MANAGERS = ADMINS

DATABASES =  {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ dbname|default(enhydris_instance_name) }}',
        'USER': '{{ dbuser|default(enhydris_instance_name) }}',
        'PASSWORD': '{{ dbpasswd|default(secret_key) }}',
        'HOST': '{{ dbhost|default("localhost") }}',
        'PORT': 5432,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/cache/enhydris/{{ dbname|default(enhydris_instance_name) }}/django_cache',
    },
}

{% if enhydris_version < '3' %}
ENHYDRIS_TIMESERIES_DATA_DIR = '{{ enhydris_timeseries_data_dir | default("/var/opt/enhydris/" ~ enhydris_instance_name ~ "/timeseries_data") }}'
{% endif %}

TIME_ZONE = '{{ time_zone }}'
SITE_ID = {{ site_id }}
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("el", "Ελληνικά"),
]
PARLER_LANGUAGES = {
    SITE_ID: [{"code": LANGUAGE_CODE}, {"code": "el"}],
    "default": {"fallbacks": ["en"], "hide_untranslated": True},
}

MEDIA_ROOT = '{{ media_root | default("/var/opt/enhydris/" ~ enhydris_instance_name ~ "/media/") }}'
MEDIA_URL = '/{{ site_base_url | default("") }}media/'
STATIC_ROOT = '/var/cache/enhydris/{{ enhydris_instance_name }}/static/'
STATIC_URL = '/{{ site_base_url | default("") }}static/'
FILE_UPLOAD_PERMISSIONS = 0o644

ROOT_URLCONF = 'urls'

SECRET_KEY = '{{ secret_key }}'

# Options for django-registration
ACCOUNT_ACTIVATION_DAYS = {{ account_activation_days }}
REGISTRATION_OPEN = {{ registration_open }}

EMAIL_BACKEND = "django_sendmail_backend.backends.EmailBackend"
DEFAULT_FROM_EMAIL = '{{ default_from_email }}'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# This is necessary because the station admin form is very complicated.
# It should be removed if the inline object become different views.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

ENHYDRIS_USERS_CAN_ADD_CONTENT = {{ enhydris_users_can_add_content }}
{% if enhydris_version >= '3' %}
ENHYDRIS_AUTHENTICATION_REQUIRED = {{ enhydris_authentication_required }}
ENHYDRIS_DEFAULT_PUBLICLY_AVAILABLE = {{ enhydris_default_publicly_available }}
ENHYDRIS_ENABLE_TIMESERIES_DATA_VIEWERS = {{ enhydris_enable_timeseries_data_viewers }}
{% else %}
ENHYDRIS_TSDATA_AVAILABLE_FOR_ANONYMOUS_USERS = {{ enhydris_tsdata_available_for_anonymous_users|default("False") }}
ENHYDRIS_SITE_CONTENT_IS_FREE = {{ enhydris_site_content_is_free|default("False") }}
{% endif %}
ENHYDRIS_WGS84_NAME = '{{ enhydris_wgs84_name|default("WGS84") }}'
ENHYDRIS_SITES_FOR_NEW_STATIONS = {{ enhydris_sites_for_new_stations|default("set()") }}
ENHYDRIS_TS_GRAPH_CACHE_DIR = '/tmp/enhydris-timeseries-graphs-{{ enhydris_instance_name }}'

# Custom template
{% if skinrepo is defined %}
TEMPLATES[0]['DIRS'] = ['/etc/opt/enhydris/{{ enhydris_instance_name }}/skin/templates']
LOCALE_PATHS = ['/etc/opt/enhydris/{{ enhydris_instance_name }}/skin/locale']
STATICFILES_DIRS = ['/etc/opt/enhydris/{{ enhydris_instance_name }}/skin/static']
{% endif %}

{% if enhydris_map_base_layers|default(False) -%}
ENHYDRIS_MAP_BASE_LAYERS = {
    {% for layer in enhydris_map_base_layers|dict2items -%}
    r"""{{ layer.key }}""": r"""{{ layer.value }}""",
    {% endfor -%}
}
{%- endif %}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_SCHEME', 'https')
SESSION_COOKIE_SECURE = {{ session_cookie_secure | default("True") }}
{% if site_base_url | default(False) -%}
FORCE_SCRIPT_NAME = '/{{ site_base_url }}'
{%- endif %}

CELERY_TASK_DEFAULT_QUEUE = "{{ dbname|default(enhydris_instance_name) }}"

ENHYDRIS_SYNOPTIC_ROOT = '/var/cache/enhydris/{{ enhydris_instance_name }}/synoptic/'
ENHYDRIS_SYNOPTIC_URL = '/{{ site_base_url | default("") }}synoptic/'
ENHYDRIS_SYNOPTIC_STATION_LINK_TARGET = '{{ enhydris_synoptic_station_link_target }}'

{% if use_enhydris_openhigis|default(False) -%}
# Enhydris-openhigis
INSTALLED_APPS.insert(0, 'enhydris_openhigis')
ENHYDRIS_OWS_URL = '{{ enhydris_openhigis_ows_url }}'
MIDDLEWARE.append("enhydris_openhigis.middleware.OpenHiGISMiddleware")
{%- endif %}

{% if enhydris_aggregator -%}
# Enhydris-aggregator.  Install it immediately before enhydris.hcore, so
# that it can override its templates.
INSTALLED_APPS.insert(INSTALLED_APPS.index('enhydris.hcore'),
                        'enhydris_aggregator')
ENHYDRIS_AGGREGATOR = {
    'SOURCE_DATABASES': [
        {% for source_db in enhydris_aggregator.source_databases -%}
        {
            'URL': '{{ source_db.url }}',
            'ID_OFFSET': {{ source_db.id_offset }},
        },
        {% endfor %}
    ],
}
{%- endif %}

{% if extra_settings|default(False) -%}
{{ extra_settings }}
{%- endif %}
