# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import ConnectionError
from .utils import *
import requests
import numpy as np
import time
import json
import math
from .models import *
from rest_framework import generics
from ars_backend.settings import PROJECT_ROOT
from .serializers import *
import pickle

CountFace = CountFace()
Scrapper = Scrapper()
DEFAULT_URL_SEARCH = "http://www.omdbapi.com/?apikey=c0b86c96&type=movie&s=%s&page=%d"
DEFAULT_URL_DETAIL = "http://www.omdbapi.com/?apikey=c0b86c96&i=%s"
MOVIE_DATA_URL = "http://localhost:8000/api/v1/movie_details/%s"
PICKLE_PATH = os.path.join(PROJECT_ROOT, 'finalized_model.pikle')

"""
    Done:
        -   Movies Search
        -   Movie Details

    Todo:
        -   Predict
        -   History
        -   Register & Login

"""
# Create your views here.
class SearchMovies(APIView):
    permission_classes = (AllowAny,)
    """
    get:
    Return desired movies selected by user
    """
    def get(self, request, format=None):
        try:
            # get data from requests
            data = request.query_params
            movies_name = data.get('m_name')
            #query is null
            if movies_name is None or (len(movies_name)) == 0 :
                raise ValueError('Title cannot be empty')
            #process given query
            movies_name = movies_name.replace(" ", "+")
            url = DEFAULT_URL_SEARCH % (movies_name,1)
            res = json.loads(requests.get(url).text)
            movie_lists = res['Search']
            return Response({'status': "success", 'data': {'movies' : movie_lists, 'total_movies' : len(movie_lists)}}, status=status.HTTP_200_OK)
        except ConnectionError:
            return Response({'status': "error", 'message': "Connection refused"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': "fail", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    permission_classes = (AllowAny,)
    """
    get:
    Return detail of the selected movie

    """
    def get(self, request, id, format=None):
        try:
            #get data from request
            data = request.query_params
            imdb_id = id
            #query null handler
            if imdb_id is None or len(imdb_id) == 0:
                raise ValueError('Id must be specified')
            url = DEFAULT_URL_DETAIL % imdb_id
            res = json.loads(requests.get(url).text)
            #image
            img_thumb_url = res['Poster']
            img_full_url = img_thumb_url[:len(img_thumb_url)-8] + ".jpg" if img_thumb_url != "N/A" else "N/A"
            #genre
            genres = self.list_processor(res['Genre'])
            #director
            director = self.list_processor(res['Director'])
            #Actor
            actors = self.list_processor(res["Actors"])
            #Imdb Vote
            num_user_votes = res['imdbVotes']
            imdb_ratings = res['imdbRating']
            title_year = res['Year']
            duration = res['Runtime'].split(" ")[0]
            plot = res['Plot']
            response = {
                "id": imdb_id, "images": {'thumbnail': img_thumb_url, 'full': img_full_url}, "plot": plot, "title": res['Title'],
                "genre": genres, 'director' : director, 'actors': actors, "num_user_votes": num_user_votes, "year": title_year,
                "duration": duration, "actual_rating": imdb_ratings
            }
            return Response({'status' : 'success', 'data': response}, status=status.HTTP_200_OK)
        except ConnectionError:
            return Response({'status': "error", 'message': "Connection refused"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'status': "fail", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'status': "error", "message": "Unexpected error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #return list of text
    def list_processor(self, text):
        list = text.split(",")
        lists = []
        for i in range(len(list)):
            lists.append(list[i].strip())
        return lists


class PredictRating(APIView):

    def post(self, request, format=None):
        try:
            movie_details = request.data
            #get needed data
            movie_id = movie_details["id"]
            img = movie_details["images"]['full']
            actors = movie_details['actors']
            director = movie_details["director"]
            duration = int(movie_details['duration']) if movie_details['duration'] != "N/A" else 0
            actual_rating = math.floor(float(movie_details["actual_rating"])) if movie_details["actual_rating"] != "N/A" else "N/A"
            #calc time
            start_time = time.time()
            face_count = CountFace.instance.count_faces(img) if img != "N/A" else 0
            budget, sorted_actor, sorted_dir = Scrapper.instance.get_feature(movie_id, actors, director)
            budget = int(budget[1:].replace(",", ""))

            #init var for actors and directors
            actor_likes_1 = 0
            actor_likes_2 = 0
            actor_likes_3 = 0
            director_likes = 0

            #preprocess data
            j = 0
            for i in sorted_actor:
                if j > 2:
                    break
                if j == 0:
                    actor_likes_1 = i[1]
                elif j == 1:
                    actor_likes_2 = i[1]
                elif j == 2:
                    actor_likes_3 = i[1]
                j += 1

            j = 0
            for i in sorted_dir:
                if j > 1:
                    break
                if j == 0:
                    director_likes = i[1]
                j += 1

            model = pickle.load(open(PICKLE_PATH, 'rb'))
            prediction = model.predict(np.array([[duration, director_likes, actor_likes_1, actor_likes_2, actor_likes_3, budget, face_count]]))
            elapsed_time = int(time.time() - start_time)

            self.add_to_history(movie_id, movie_details["title"], prediction[0],actual_rating, img)
            response = {"rating_predicted" : prediction[0], "actual_rating": actual_rating, "time_elapsed": elapsed_time}
            return Response({'status' : 'success', 'data': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': "fail", "message": request.data}, status=status.HTTP_400_BAD_REQUEST)


    def add_to_history(self, movie_id, movie_name, predicted_rating, actual_rating, image):
        h = History(movie_id=movie_id, movie_name=movie_name, movie_rating=predicted_rating, actual_rating=actual_rating, movie_thumbnail=image)
        h.save()


class HistoryView(generics.ListAPIView):
    model = History
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (AllowAny,)

