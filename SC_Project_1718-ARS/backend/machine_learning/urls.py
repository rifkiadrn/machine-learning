from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'search$',
        SearchMovies.as_view(), name='search_movie'),
    url(r'movie_details/((?P<id>[\w\-]+)/$)$',
        MovieDetail.as_view(), name='movie_details'),
    url(r'predict/',
        PredictRating.as_view(), name='predict_rating'),
    url(r'history/$',
        HistoryView.as_view(), name='history')
]