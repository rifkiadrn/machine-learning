import numpy as np
import cv2
import ssl
import os
from ars_backend.settings import PROJECT_ROOT
import requests
import operator
from urllib.request import urlopen
from bs4 import BeautifulSoup

class CountFace:
    class __CountFace:
        def __init__(self):
            self.CTX = ssl._create_unverified_context()
            self.FACE_CASCADE = cv2.CascadeClassifier(os.path.join(PROJECT_ROOT, '../machine_learning/haarcascade_frontalface_default.xml'))

        def count_faces(self, url):
            try:
                img = urlopen(url , context=self.CTX)
                image = np.asarray(bytearray(img.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = self.FACE_CASCADE.detectMultiScale(
                    grayImage,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                total_faces = faces.shape[0]
            except AttributeError:
                total_faces = 0
            except Exception as e:
                raise Exception("Something Unexected Has Happened")
            return total_faces

    instance = None

    def __init__(self):
        if not CountFace.instance:
            CountFace.instance = CountFace.__CountFace()

class Scrapper:
    class __Scrapper:
        def __init__(self):
            self.VERSION = "v2.10/"
            self.URL_OMDB = "https://www.omdbapi.com/?i="
            self.APIKEY = "&apikey=c0b86c96"
            self.ACCESS_TOKEN = "&access_token=EAAQDT6Swu7EBAF840IyPOZAPPPMWuDKiX5HlltdKZCg6xFwB16BZAMmVUtwj60VrEZCMesD6gJ0DDZCqXIDvekCZCP8G6mVgOlqqJveVKuEFoTlarjRMTh6SMQTGDBDeJG6VH8G9dFZCeYdUljqZAPk6fvg5fOlpRkcZD"
            self.URL = "https://graph.facebook.com/"
            self.GET_ID = "search?type=page&limit=1"
            self.GET_FAN_COUNT = "/?fields=fan_count"

        def get_id(self, name):
            name_encode = name.replace(" ", "+")
            endpoint = self.URL + self.VERSION + self.GET_ID + self.ACCESS_TOKEN + "&q=" + name_encode
            r = requests.get(endpoint)
            id = r.json()['data'][0]['id']
            return id

        def get_fan_count(self, id):
            endpoint = self.URL + self.VERSION + id + self.GET_FAN_COUNT + self.ACCESS_TOKEN
            r = requests.get(endpoint)
            fan_count = r.json()['fan_count']
            return fan_count

        def get_feature(self, movie_id, directors, actors):
            try:
                budget = self.get_budget(movie_id)
                budget = budget
                # num_of_critics = self.get_num_of_critics(movie_id)
                result_dir = {}
                result_act = {}
                for director in directors:
                    id_director = self.get_id(director)
                    fan_count_director = self.get_fan_count(id_director)
                    result_dir[director] = fan_count_director

                for actor in actors:
                    id_actor = self.get_id(actor)
                    fan_count_actor = self.get_fan_count(id_actor)
                    result_act[actor] = fan_count_actor

                sorted_dir = sorted(result_dir.items(), key=operator.itemgetter(1), reverse=True)
                sorted_act = sorted(result_act.items(), key=operator.itemgetter(1), reverse=True)
                # return (sorted_dir, sorted_act, budget, num_of_critics)
            except Exception as e:
                sorted_dir = []
                sorted_act = []
            finally:
                return (budget, sorted_dir, sorted_act)

        def get_budget(self,id):
            url = 'http://www.imdb.com/title/%s/?ref_=fn_al_nm_1a' % id
            page = urlopen(url)
            soup = BeautifulSoup(page.read(), "lxml")
            for h4 in soup.find_all('h4'):
                if "Budget:" in h4:
                    return h4.next_sibling.strip()
            return "$0"

        def get_num_of_critics(self, id):
            url = 'http://www.imdb.com/title/%s/?ref_=fn_al_nm_1a' % id
            page = urlopen(url)
            soup = BeautifulSoup(page.read(), "lxml")
            total = soup.select_one("a[href*=externalreviews?ref_=tt_ov_rt]").text
            return total

    instance = None

    def __init__(self):
        if not Scrapper.instance:
            Scrapper.instance = Scrapper.__Scrapper()
