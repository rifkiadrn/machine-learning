from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'training$',
        TrainingModel.as_view(), name='train_movie'),
    ]