from django.conf.urls import url
from ubafer_app.views import conference_details

urlpatterns = [
    url(r'api/', conference_details),
]