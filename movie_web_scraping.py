import string
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re

#create a dataframe movie
movie = pd.DataFrame()

#function to scrape the link related to the movies
#param  movie: the movie dataframe
#       url: the webpage Domestic Yearly Box Office of each year
def scrape_infolink(movie, url):
    #scrape the provided webpage with BeautifulSoup
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    #create an array to keep all info links during the web scraping
    array = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/release/")}):
        array.append(link.get('href'))
    #create an attribute for the info link of each movie
    movie['link'] = None
    #loop through the array of info links, and reformat the full info link
    for i in range(len(array)):
        movie['link'][i] = array[i]
    movie['link'] = 'https://www.boxofficemojo.com'+ movie['link']
    return movie

#scrape the data between the years of 2010 and 2020 on Box Office MOJO
for i in range(2010,2020):
    url = 'https://www.boxofficemojo.com/year/'+str(i)
    temp = pd.read_html(url)[0]
    temp['Year'] = i
    temp_full = scrape_infolink(temp,url)
    movie = movie.append(temp_full)
movie.index = range(len(movie))

#create an attribute for the reformatted date
movie['Full Date'] = None
#mapping and reformatting the full date of the movie release
for i in range(len(movie)):
    movie['Full Date'][i] = movie['Release Date'][i]+", "+ str(movie['Year'][i

movie["Full Date"][movie["Full Date"] == "Feb 29, 2013"] = "Feb 28, 2013" #error in raw data: Feb 29, 2013 does not exist
movie['Full Date'] = pd.to_datetime(movie['Full Date'], format = "%b %d, %Y")
movie['Full Date'] = pd.to_datetime(movie['Full Date'], format = "%Y-%m-%d")
#movie
#movie.to_csv('movie_2010_2020_draft.csv', index = False)

#function to scrape the data of genre, budget, and runtime from the info link of a movie
def scrape_genre_budget_runtime(movie):
    for i in range(len(movie)):
        #go to the info link of each movie for scraping
        html_page2 = urllib2.urlopen(list(movie['link'])[i])
        soup2 = BeautifulSoup(html_page2)
        #locate the section in the html source codes with the info. of budget, genre, and runtime
        soup2 = soup2.find("div", class_="a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile")
        tag_budget = soup2.find_all("span", string = "Budget")
        tag_genre = soup2.find_all("span", string = "Genres")
        tag_runtime = soup2.find_all("span", string = "Running Time")

        #create a separator to locate specifically for each of the info. of budget, genre, and runtime
        separator = soup2.find_all("span")
        #inital the index for tracing the index located the relevant info
        index_genre = 0
        index_budget = 0
        index_runtime = 0
        #find the genre
        if (len(tag_genre) > 0):
            while(str(separator[index_genre]) != "<span>Genres</span>"):
                index_genre +=1
            #reformat the info. of genres in a more reader-friendly way
            movie['Genre'][i] = separator[index_genre + 1].text.strip().replace('\n    \n        ',',')
        #find the budget
        if (len(tag_budget) > 0):
            while(str(separator[index_budget]) != "<span>Budget</span>"):
                index_budget +=1
            #budget = soup2.find_all("span", class_="money")
            movie['Budget'][i] = separator[index_budget + 1].text
        #find the runtime
        if (len(tag_runtime) > 0):
            while(str(separator[index_runtime]) != "<span>Running Time</span>"):
                index_runtime +=1
            movie['Running Time'][i] = separator[index_runtime + 1].text
        #tracker to see the scraping process
        print ("#"+str(i)+" is done")
    return (movie)

movie_2010_2020 = scrape_genre_budget_runtime(movie)
#movie_2010_2020
#movie_2010_2020.to_csv('movie_2010_2020.csv', index = False)
