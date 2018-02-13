#!/usr/bin/env python3


from requests import get
from bs4 import BeautifulSoup
from dateutil.relativedelta import *
import datetime
import time
import json

from movie import Movie


class Scraper(object):
    """
    A scraper will scrape an IMDb webpage to collect movie titles, genres, and descriptions. 
    
    """
    def __init__(self):
        """
        Initializes a Scraper object.
        
        movies: a list that stores Movie objects
        
        """  
        self.movies = []
        
    def parse_html(self, url):
        """
        Requests the content of the webpage using a get request and stores the response. 
        Uses a BeautifulSoup object to help parse the html in response.text. 
        Finds all the div elements that have information about movies (class = "list_item").
        
        url: string, the url to collect data from
        return: a ResultSet of div elements with a class "list_item"
        
        """
        #get english movies only
        headers = {"Accept-Language": "en-US, en; q=0.5"}
        
        while True:
            try:
                response = get(url, headers = headers)
                break
            except ConnectionError as e:
                print(e)

        data = response.text

        soup = BeautifulSoup(data, "html.parser")

        movies_set = soup.find_all("div", class_ = "list_item")
        
        return movies_set
    
    def scrape(self, movies_set):
        """
        Gathers the required data from each movie in movies_set and creates
        a new Movie object. Stores the Movie object in self.movies.
        
        movies_set: a ResultSet of div elements that contain information about movies
        
        """
        for movie in movies_set:
    
            #get the movie title (without the release year)
            movie_title = movie.h4.a.text[1:-7]
            
            #get the genres of the movie
            movie_genres = movie.p.find_all("span", itemprop = "genre")
            
            #extract the text of the span elements and store them in a new list
            movie_genres_text = []
            for genre in movie_genres:
                movie_genres_text.append(genre.text)
            
            
            #get the description
            movie_description = movie.find("div", itemprop = "description").text[:-20]
            
            self.movies.append(Movie(movie_title, movie_genres_text, movie_description))
        
    def get_movies(self):
        """
        return: a list of Movie objects
        
        """
        return self.movies
    
    
class InTheatersScraper(Scraper):
    """
    An "in theaters" webpage scraper will scrape movie data from the "in theaters" movies webpage.
    
    """
    
    def __init__(self):
        """
        Initializes an InTheaterseScraper object.
        
        url: string, the url to collect data from
        
        """
        super(InTheatersScraper, self).__init__()
        self.url = "http://www.imdb.com/movies-in-theaters/?ref_=cs_inth"
        
    def run_scrape(self):
        """
        Calls the parent class scrape method with a movies_set object returned by parse_html.
        """
        movies_set = self.parse_html(self.url)
        self.scrape(movies_set)
    
    
class ComingSoonScraper(Scraper):
    """
    A "coming soon" webpage scraper will scrape movie data from multiple IMDb webpages that display "coming soon" movies.
    These webpages share a url but have different url parameters.
    
    """
    def __init__(self, month_range = 1):
        """
        Initializes a ComingSoonScraper object.
        
        urls: a list of urls to collect data from
        month_range: int, how many months after the current month to collect data for
        
        """
        super(ComingSoonScraper, self).__init__()
        self.urls =  []
        self.month_range = month_range
        
        if month_range > 5:
            self.month_range = 5
            
    
    def createUrlList(self):
        """
        Creates a list of urls to collect data from. The month parameter of the
        "coming soon movies" url is changed for each url. The number of urls is 
        determined by the specified month range. 
        
        """
        #get the url for the current month and year
        current_month = datetime.datetime.today().strftime("%m")
        current_year = datetime.datetime.today().strftime("%Y")
        
        current_month_url = "http://www.imdb.com/movies-coming-soon/"+ current_year + "-" + current_month +"/?ref_=cs_dt_nx"
        self.urls.append(current_month_url)
        
        
        #add the urls for the next months
        i = 0
        current = datetime.datetime.today()
        while i < self.month_range:
            time.sleep(3)
            next_month = current + relativedelta(months=1)
            next_month_month = next_month.strftime("%m") 
            next_month_year = next_month.strftime("%Y")
            
            next_month_url = "http://www.imdb.com/movies-coming-soon/"+ next_month_year + "-" + next_month_month +"/?ref_=cs_dt_nx"
        
            self.urls.append(next_month_url)
            
            current = next_month
            
            i += 1
        
        
    
    def run_scrape(self):
        """
        For each of the urls in self.urls, parses the html and collects movie data using
        parent class scrape method.
        
        """
        self.createUrlList()
        for i in self.urls:
            movies_set = self.parse_html(i)
            self.scrape(movies_set)
            
    

def main():
    """
    Creates an instance of InTheatersScraper and ComingSoonScraper and calls their scrape methods to 
    create a movies object list. Appends a string of all the movie objects to a new
    list called div_elems. div_elems is converted into a json object and printed.

    """
    in_theaters = InTheatersScraper()
    coming_soon = ComingSoonScraper()
    
    in_theaters.run_scrape()
    coming_soon.run_scrape()
    
    movies = set(in_theaters.get_movies() + coming_soon.get_movies())
    

    div_elems = []
    
    for movie in movies:
        div_elems.append(movie.__str__().encode("utf-8"))
    
    print(json.dumps(div_elems))
        


main()
