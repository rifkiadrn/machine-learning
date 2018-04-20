import requests
import operator

VERSION = "v2.10/"
URL_OMDB = "https://www.omdbapi.com/?t="
APIKEY = "&apikey=c0b86c96"
ACCESS_TOKEN = "&access_token=EAACEdEose0cBANcX5knfbay6aENK6rHCkefECUpRUpmrSUY00e9m9bq6Uq4osIZBW4I7uoZCDwtaY4DseYrjbUkMmZBQ81EQpNfHuUENTumdFshuADPzVDmmASKd0xxngtxAM86oQZCtQ0qXtO0h8KhPaaAPHHLcCtTjVaPEdfWwF9KMVbKh0ZCZCnnMIv2shTyIIuN9isgAZDZD"
URL = "https://graph.facebook.com/"
GET_ID = "search?type=page&limit=1"
GET_FAN_COUNT = "/?fields=fan_count"

def get_id(name):
    name_encode = name.replace(" ", "+")
    endpoint = URL + VERSION + GET_ID + ACCESS_TOKEN + "&q=" + name_encode
    r = requests.get(endpoint)
    id = r.json()['data'][0]['id']
    return id

def get_fan_count(id):
    endpoint = URL + VERSION + id + GET_FAN_COUNT + ACCESS_TOKEN
    r = requests.get(endpoint)
    fan_count = r.json()['fan_count']
    return fan_count

def get_directors_and_actors_url_posters(movie_title):
    endpoint = URL_OMDB + movie_title + APIKEY
    print endpoint
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
    r = requests.get(endpoint, headers=headers)
    director = r.json()["Director"]
    directors = director.split(",")
    actor = r.json()["Actors"]
    actors = actor.split(",")
    poster = r.json()["Poster"]
    return (directors, actors, poster)

def get_fan_count_per_directors_actors(movie_title):
    movie_title_encode = movie_title.replace(" ", "+")
    directors, actors, poster = get_directors_and_actors_url_posters(movie_title_encode)
    
    result_dir = {}
    result_act = {}

    for director in directors:
        id_director = get_id(director)
        fan_count_director = get_fan_count(id_director)
        result_dir[director] = fan_count_director
    
    for actor in actors:
        id_actor = get_id(actor)
        fan_count_actor = get_fan_count(id_actor)
        result_act[actor] = fan_count_actor
    
    sorted_dir = sorted(result_dir.items(), key=operator.itemgetter(1), reverse=True)
    sorted_act = sorted(result_act.items(), key=operator.itemgetter(1), reverse=True)
    return (sorted_dir, sorted_act, poster)

def get_budget(id):
    

sorted_dir, sorted_act, poster = get_fan_count_per_directors_actors("Infinity war")
print(sorted_dir)
print(sorted_act)
print(poster)