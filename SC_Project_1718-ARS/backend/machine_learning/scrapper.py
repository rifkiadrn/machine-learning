import re
import time
import scrapy
import random
import json
import locale
import urllib.request
from bs4 import BeautifulSoup
from models import Movie

class MovieItem(scrapy.Item):
    movie_imdb_link = scrapy.Field()
    movie_title = scrapy.Field()
    title_year = scrapy.Field()
    genres = scrapy.Field()
    budget = scrapy.Field()
    color = scrapy.Field()
    duration = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    plot_keywords = scrapy.Field()
    storyline = scrapy.Field()
    aspect_ratio = scrapy.Field()
    content_rating = scrapy.Field()
    cast_info = scrapy.Field()
    director_info = scrapy.Field()
    num_facebook_like = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class ImdbSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ["imdb.com"]
    start_urls = ['https://www.imdb.com/title/tt4154756/']

    locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

    def extract_text(self, xpath, response):
        path = "{}/text()".format(xpath)
        return response.xpath(path).extract()

    def get_facebook_likes(self, entity_type, entity_id):
        # the 'entity_id' could be imdb movie id, or imdb people id
        if entity_type == "person_name_id":
            url = "https://en-gb.facebook.com/widgets/like.php?width=280&show_faces=1&layout=standard&href=http%3A%2F%2Fwww.imdb.com%2Fname%2F{}%2F&colorscheme=light".format(entity_id)
        elif entity_type == "movie_title_id":
            url = "https://en-gb.facebook.com/widgets/like.php?width=280&show_faces=1&layout=standard&href=http%3A%2F%2Fwww.imdb.com%2Ftitle%2F{}%2F&colorscheme=light".format(entity_id)
        else:
            url = None
        time.sleep(random.uniform(0, 0.25)) # randomly snooze a time within [0, 0.4] second
        try:
            content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(content, "lxml")
            sentence = soup.find_all(id="u_0_3")[0].text # get sentence like: "43K people like this"
            num_likes = sentence.split(" ")[0]
            if num_likes[-1:] == "k":
                num_likes = num_likes[:-1].replace(",", ".")
                num_likes = float(num_likes) * 1000
                num_likes = int(num_likes) 
        except Exception as e:
            num_likes = e
        return num_likes

    def get_movie_id_from_url(self, url):
        # sample imdb movie url: http://www.imdb.com/title/tt0068646/?ref_=nv_sr_1
        # we need to return "tt0068646"
        if url is None:
            return None
        return re.search("(tt[0-9]{7})", url).group()

    def get_person_name_id_from_url(self, url):
        # sample imdb person url: http://www.imdb.com/name/nm0000338/?ref_=tt_ov_dr
        # we need to return "nm0000338"
        if url is None:
            return None
        return re.search("(nm[0-9]{7})", url).group()

    def parse(self, response):
        item = MovieItem()
        try:
            movie_title = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0]
        except:
            movie_title = None
        item['movie_title'] = movie_title

        # ---------------------------------------------------------------------------------------------------
        try:
            title_year = response.xpath('//*[@id="titleYear"]/a/text()').extract()[0]
        except:
            title_year = None
        item['title_year'] = title_year

        # ---------------------------------------------------------------------------------------------------
        try:
            genres = response.xpath('//div[@itemprop="genre"]//a/text()').extract()
        except:
            genres = None
        item['genres'] = genres

        # ---------------------------------------------------------------------------------------------------
        try:
            country = response.xpath('//div[@id="titleDetails"]/div/a[contains(@href, "country")]/text()').extract()
        except:
            country = None
        item['country'] = country

        # ---------------------------------------------------------------------------------------------------
        try:
            language = response.xpath('//div[@id="titleDetails"]/div/a[contains(@href, "language")]/text()').extract()
        except:
            language = None
        item['language'] = language

        # ---------------------------------------------------------------------------------------------------
        try:
            plot_keywords = response.xpath('//a/span[@itemprop="keywords"]/text()').extract()
        except:
            plot_keywords = None
        item['plot_keywords'] = plot_keywords

        # ---------------------------------------------------------------------------------------------------
        try:
            storyline = response.xpath('//div[@id="titleStoryLine"]/div[@itemprop="description"]/p/text()').extract()[0]
        except:
            storyline = None
        item['storyline'] = storyline

        # ---------------------------------------------------------------------------------------------------
        try:
            color = response.xpath('//a[contains(@href, "colors=")]/text()').extract()
        except:
            color = None
        item['color'] = color

        # ---------------------------------------------------------------------------------------------------
        try:
            budget = response.xpath('//h4[contains(text(), "Budget:")]/following-sibling::node()/descendant-or-self::text()').extract()
        except:
            budget = None
        item['budget'] = budget

        # ---------------------------------------------------------------------------------------------------
        try:
            duration = response.xpath('//time[@itemprop="duration"]/text()').extract()
        except:
            duration = None
        item['duration'] = duration

        # ---------------------------------------------------------------------------------------------------
        try:
            aspect_ratio = response.xpath('//h4[contains(text(), "Aspect Ratio:")]/following-sibling::node()/descendant-or-self::text()').extract()
            # preprocess movie aspect ratio.
            ratio = ""
            for s in aspect_ratio:
                s = s.strip()
                if len(s) != 0:
                    ratio = s
                    break
            aspect_ratio = ratio
        except:
            aspect_ratio = None
        
        item['aspect_ratio'] = aspect_ratio

        # ---------------------------------------------------------------------------------------------------
        try:
            content_rating = response.xpath('//meta[@itemprop="contentRating"]/following-sibling::node()/descendant-or-self::text()').extract()
        except:
            content_rating = None
        item['content_rating'] = content_rating

        # ---------------------------------------------------------------------------------------------------
        # (1) get names and links of all cast members

        base_url = "http://www.imdb.com"

        try:
            # extract all ODD table rows from the cast list
            cast_name_list_from_odd_rows = response.xpath('//table[@class="cast_list"]/tr[@class="odd"]/td[@class="itemprop"]/a/span[@class="itemprop"]/text()').extract()
            cast_name_href_list_from_odd_rows = response.xpath('//table[@class="cast_list"]/tr[@class="odd"]/td[@class="itemprop"]/a/@href').extract()
            links_from_odd_rows = [base_url + e for e in cast_name_href_list_from_odd_rows]
            # pairs_for_odd_rows = zip(cast_name_list_from_odd_rows, links_from_odd_rows)

            # extract all EVEN table rows from the cast list
            cast_name_list_from_even_rows = response.xpath('//table[@class="cast_list"]/tr[@class="even"]/td[@class="itemprop"]/a/span[@class="itemprop"]/text()').extract()
            cast_name_href_list_from_even_rows = response.xpath('//table[@class="cast_list"]/tr[@class="even"]/td[@class="itemprop"]/a/@href').extract()
            links_from_even_rows = [base_url + e for e in cast_name_href_list_from_even_rows]
            # pairs_for_even_rows = zip(cast_name_list_from_even_rows, links_from_even_rows)

            cast_name_all = cast_name_list_from_odd_rows + cast_name_list_from_even_rows
            links_from_all = links_from_odd_rows + links_from_even_rows
            # combine the two lists
            cast_name_link_pairs = zip(cast_name_all, links_from_all)
            # convert list of pairs to dictionary

            cast_info = []
            for (name, link) in cast_name_link_pairs:
                actor = {}
                actor["actor_name"] = name
                actor["actor_link"] = link

                name_id = self.get_person_name_id_from_url(link)
                actor["actor_facebook_likes"] = self.get_facebook_likes(entity_type="person_name_id", entity_id=name_id)

                cast_info.append(actor)
        except:
            cast_info = None
        item['cast_info'] = cast_info
        sorted_casts_by_popularity = sorted(cast_info, key=lambda k: parse_facebook_likes_number(k['actor_facebook_likes']), reverse=True)
        top_k = 3
        # let's extract top k actors
        for k in range(top_k):
            _key_of_actor_name = "actor_{}_name".format(k+1)
            _key_of_facebook_likes = "actor_{}_facebook_likes".format(k+1)
            if k < len(sorted_casts_by_popularity):
                item[_key_of_actor_name] = sorted_casts_by_popularity[k]['actor_name'].encode('utf-8')
                item[_key_of_facebook_likes] = parse_facebook_likes_number(sorted_casts_by_popularity[k]['actor_facebook_likes'])
            else:
                item[_key_of_actor_name] = None
                item[_key_of_facebook_likes] = None

        # ---------------------------------------------------------------------------------------------------
        # (2) get names and links of directors
        try:
            director_name = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()[0]

            director_partial_link = response.xpath('//span[@itemprop="director"]/a/@href').extract()[0]
            director_full_link = base_url + director_partial_link


            director_info = {}
            director_info["director_name"] = director_name
            director_info["director_link"] = director_full_link

            name_id = self.get_person_name_id_from_url(director_full_link)
            director_info["director_facebook_likes"] = self.get_facebook_likes(entity_type="person_name_id", entity_id=name_id)
        except:
            director_info = None
        item['director_info'] = director_info

        # ---------------------------------------------------------------------------------------------------
        movie_id = self.get_movie_id_from_url(response.url)
        num_facebook_like = self.get_facebook_likes(entity_type="movie_title_id", entity_id=movie_id)
        item['num_facebook_like'] = num_facebook_like
        item['movie_id'] = movie_id

        # ---------------------------------------------------------------------------------------------------
        try:
            poster_image_url = response.xpath('//div[@class="poster"]/a/img/@src').extract()[0]

            # a sample image url looks like this:
            #   http://ia.media-imdb.com/images/M/MV5BMTY5NzY5NTY2NF5BMl5BanBnXkFtZTcwNTg3NzIxNA@@._V1_UX182_CR0,0,182,268_AL_.jpg
            # we need to remove trailing characters "UX182_CR0,0,182,268_AL_" to get larger poster with this like:
            #   http://ia.media-imdb.com/images/M/MV5BMTY5NzY5NTY2NF5BMl5BanBnXkFtZTcwNTg3NzIxNA@@._V1_.jpg
            poster_image_url = [ poster_image_url.split("_V1_")[0] + "_V1_.jpg" ]

        except:
            poster_image_url = None
        item['image_urls'] = poster_image_url

        # ---------------------------------------------------------------------------------------------------
        yield item
        m = Movie(movie_name=item['movie_title'], movie_thumbnail=item['image_urls'], movie_id=item['movie_id'],
                    plot=item['storyline'], genre=item['genres'], director_name=item['director_info']["director_name"], director_fbl=item['director_info']["director_facebook_likes"],
                    year=item['title_year'], duration=item['duration'], actor_1_name=item['actor_1_name'], actor_1_fbl=item['actor_1_facebook_likes'], 
                    actor_2_name=item['actor_2_name'], actor_2_fbl=item['actor_2_facebook_likes'], actor_3_name=item['actor_3_name'], actor_3_fbl=item['actor_3_facebook_likes'])
        m.save()