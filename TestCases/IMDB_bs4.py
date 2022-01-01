import bs4
from packages import requests
import csv
import time
from Library import ConfigReader
import configparser

#importing the required drivers
genre_length=ConfigReader.readConfigData('Details','genre_num')
genres=[]
for i in range(int(genre_length)):
    gen = "genre"+str(i)
    genres.append(ConfigReader.readConfigData('Genre', gen))

#taking advantage of the url to get different types of content
filename="../output/IMDB_bs4.csv"
csv_file= open(filename,'w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['name','from','to','rating','tv_or_movie','genre','runtime','votes'])
#creating their respective files to store data

for genre in genres:
    #taking no of pages to scrape
    start=1
    pages=20
    for i in range(pages):
        payload={'genres':genre,'start':start}
        url="https://www.imdb.com/search/title/"
        #each page has 50 titles so 50*i
        while True:
            try:
                page=requests.get(url,params=payload,timeout=5)
                break
            except:
                time.sleep(5)
        soup=bs4.BeautifulSoup(page.text,'lxml')
        body=soup.find('div',class_='article')
        articles=body.find_all('div',class_='lister-item mode-advanced')
        start=start+len(articles)
        #now getting the url and parsing it


        for article in articles:
            #this for loop gets all the titles
            name=article.find('h3',class_='lister-item-header') # getting the name of the movie

            #here for rating i am using try except as some titles have no rating
            try:
                rating=article.find('div',class_='ratings-bar').div['data-value']
            except:
                rating="None"
            try:
                runtime=article.find('span',class_='runtime').text
            except:
                runtime="None"
            try:
                votes=article.find('span',attrs={"name":"nv"}).text
            except:
                votes="None"
            #so what i have done above is when we take year here it is like (yyyy-yyyy) or (yyyy) or (yyyy-) or null
            #so get that to yyyy,yyyy i have done array operations
            year=name.find('span',class_='lister-item-year text-muted unbold').text
            year_len=len(year)
            if(year==""):
                a="None"
                b="None"
                tv_movie="Movie"
            else:
                y=year[1:year_len-1]
                if(y[0]=="I"):
                    y=y[4:year_len]
                if(len(y)==4):
                    tv_movie="Movie"
                else:
                    tv_movie="TV"
                if(len(y)==9):
                    a=y[0:4]
                    b=y[5:9]
                else:
                    a=y[0:4]
                    b="None"
            print(name.a.text,rating,votes)
            csv_writer.writerow([name.a.text,a,b,rating,tv_movie,genre,runtime,votes])
csv_file.close()
