{% if enhydris_major_version == 2 %}
from django.conf.urls import include, url
{% else %}
from django.urls import include, path
{% endif %}

from enhydris import urls as enhydris_urls
{% if use_enhydris_openhigis|default(False) -%}
from enhydris_openhigis import urls as enhydris_openhigis_urls
{%- endif %}


urlpatterns = [
    {% if use_enhydris_openhigis|default(False) -%}
    path("openhigis/", include(enhydris_openhigis_urls)),
    {%- endif %}
    {% if enhydris_major_version == 2 %}
    url("", include(enhydris_urls)),
    {% else %}
    path("", include(enhydris_urls)),
    {% endif %}
]
