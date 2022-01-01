import bs4
from packages import requests
import csv
import time
from Library import ConfigReader
import configparser

genre_length=ConfigReader.readConfigData('Details','genre_num')
genres=[]
for i in range(int(genre_length)):
    gen = "genre"+str(i)
    genres.append(ConfigReader.readConfigData('Genre', gen))

filename="../output/popular_IMDB_bs4.csv"
csv_file= open(filename,'w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['name','from','to','rating','tv_or_movie','duration','genre','votes','reviews','critics','creators','stars','popularity_rank','popularity_UP_down','country'])
#creating their respective files to store data

url=ConfigReader.readConfigData('Details','Application_URL')

for genre in genres:
    #taking no of pages to scrape
    start=1
    pages=1
    for i in range(pages):
        payload={'genres':genre,'start':start}
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

            #to get some aditional info we geting the link of title and parsing it
            link=article.find('h3',class_='lister-item-header').a['href']
            l="https://www.imdb.com"+link+"?ref_=adv_li_tt"
            while True:
                try:
                    p=requests.get(l,timeout=5)
                    break
                except:
                    time.sleep(5)
            soup1=bs4.BeautifulSoup(p.text,'lxml')

            #taking the no of votes used to get the rating
            try:
                votes=soup1.find('div',class_='imdbRating').a.text
            except:
                votes="None"
            try:
                duration=soup1.find('time').text
            except:
                duration="None"
            psw=soup1.find('div',class_='plot_summary_wrapper')
            credit_summary_items=psw.find_all('div',class_='credit_summary_item')
            try:
                cs=credit_summary_items[0].find_all('a')
                creators=[]
                for c in cs:
                    creators.append(c.text)
            except:
                creators="None"
            try:
                ss=credit_summary_items[1].find_all('a')
                stars=[]
                for s in ss:
                    stars.append(s.text)
                stars.pop()
            except:
                stars="None"

            rew=psw.find_all('span',class_='subText')
            if(len(rew)==2):
                rc=rew[0].find_all('a')
                try:
                    reviews=rc[0].text
                except:
                    reviews="None"
                try:
                    critics=rc[1].text
                except:
                    critics="None"
                popularity=rew[1].text
                try:
                    up_down=rew[1].find('span',class_='popularityUpOrFlat').text
                except:
                    try:
                        up_down=rew[1].find('span',class_='popularityDown').text
                        up_down=int(up_down)*(-1)
                    except:
                        up_down="None"
            if(len(rew)==3):
                rc=rew[1].find_all('a')
                try:
                    reviews=rc[0].text
                except:
                    reviews="None"
                try:
                    critics=rc[1].text
                except:
                    critics="None"
                popularity=rew[2].text
                try:
                    up_down=rew[2].find('span',class_='popularityUpOrFlat').text
                except:
                    try:
                        up_down=rew[2].find('span',class_='popularityDown').text
                        up_down=int(up_down)*(-1)
                    except:
                        up_down="None"


            try:
                titleDetails=soup1.find('div',id='titleDetails')
                all=titleDetails.find_all('div',class_='txt-block')
                if(all[0].h4.text=="Country:"):
                                country=all[0].a.text
                else:
                    country=all[1].a.text
            except:
                country="None"


            print(name.a.text)
            print(rating)
            print(votes)
            print(popularity.split()[0])
            csv_writer.writerow([name.a.text,a,b,rating,tv_movie,duration.strip(),genre,votes,reviews.split()[0],critics.split()[0],creators,stars,popularity.split()[0],up_down,country])
csv_file.close()
