from bs4 import BeautifulSoup
import requests
import csv
import time
from selenium.webdriver import Chrome
from Base import Initiate_Driver
from Library import ConfigReader

genre_length = ConfigReader.readConfigData('Details','genre_num')
filename="../output/popular_IMDB_Movies_Popularity.csv"
csv_file= open(filename,'w',newline='')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['name','from','to','rating','Tv/Movie','Country Name','Time Duration','Genre','votes','reviews','Meta Score','Certificate','critics','creators','stars','popularity_rank','Popularity up or down'])


genres = []
print("length of genre is ")
print(genre_length)
for i in range(int(genre_length)):
    gen = "genre"+str(i)
    genres.append(ConfigReader.readConfigData('Genre', gen))
# we are taking advantage of the url to get different types of content
print(genres)
for genre in genres:
    print("genre is ", genre)
    # creating their respective files to store data
    links = []
    driver = Initiate_Driver.startbrowser()
    url = ConfigReader.readConfigData('Details','Application_URL')

    driver.get(url)
    time.sleep(3)
    movies = driver.find_elements_by_xpath("//div[@class='lister-item-content']")
    title_length = len(movies)
    print(title_length)
    #taking no of pages to scrape 
    pages=1
    
    for i in range(pages):
        

        val = 1+title_length*i
        genre_num = ConfigReader.readConfigData('Details','genre_num')

        # url="https://www.imdb.com/search/title/?genres="+genre+"&start="+str(val)
        url = ConfigReader.read_urls(genre,val)
        print(url)
        driver.get(url) # changed
        

        # ** If I am navigating to each title page individually and then come back then I didnot work for me so I first collected the info for all the 50 titles which is present on the main page and 
        # then I navigated to each of the 50 pages by storing all the links in a list 
        movies = driver.find_elements_by_xpath("//div[@class='lister-item-content']")
        
        time.sleep(5)

        driver.implicitly_wait(5)
        # implicitly_wait( ) method tells the Webdriver to poll the DOM again and again for a certain amount of time.
        links = []
        header_list = []
        lista = []
        listb = []
        ratinglist = []
        voteslist = []
        tvormovie = []
        metas = []
        
        year_list = driver.find_elements_by_xpath("//span[@class='lister-item-year text-muted unbold']")
        # votes_list = driver.find_elements_by_xpath("//span[@name='nv']")
        print("length of movies is ")
        print(len(movies))
        for i in range(len(movies)):
            header = movies[i].find_element_by_tag_name('a')
            header_list.append(header.text)
            link = header.get_attribute('href')
            l="https://www.imdb.com"+link
            links.append(link) # storing all the 50 links on the page 
            header = movies[i].find_element_by_tag_name('a').text
            try:
                rating = movies[i].find_element_by_tag_name('strong').text
                
            except :
                rating = "None"
            ratinglist.append(rating)  # storing the ratings of 50 titles
            #             # year=movies[i].find_element_by_xpath("//span[@class='lister-item-year text-muted unbold']").text
            year = year_list[i].text
            #print(year)
            year_len = len(year) 
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
            #print(" a : ",a)
            #print(" b : ",b)
            #print(tv_movie)
            #try :   
              #  driver.find_element_by_xpath("//div[@class='bp_content']")
              #  tv_movie = "TV Series"
            #except :
             #   tv_movie = "Movie"    
            lista.append(a) # storing all the 50 from year values on the page
            listb.append(b)  # storing all the 50 to year values on the page
            tvormovie.append(tv_movie) 
            #try:
             #   votes=movies[i].find_element_by_xpath("//span[@name='nv']").text
            #except:
             #   votes="None"   
            #voteslist.append(votes)  # storing all the 50 vote values on the page 
            #print(votes)  
                    
        for i in range(len(movies)):
                
            # In this for loop I am navigating to all the links stored on the page and navigate through them 
            # and collect the data from individual pages
            driver.get(links[i])

            driver.implicitly_wait(5)
            # You can use implicit waits as well
            
            psw=driver.find_element_by_xpath("//div[@class='plot_summary_wrapper']")
            # collecting stars and creators information
            credit_summary_items=psw.find_elements_by_xpath("//div[@class='credit_summary_item']")
            try:
                cs=credit_summary_items[0].find_elements_by_tag_name('a')
                creators=[]
                for c in cs:
                    creators.append(c.text)
            except:
                creators="None"
            try:
                ss=credit_summary_items[1].find_elements_by_tag_name('a')
                stars=[]
                for s in ss:
                    stars.append(s.text)
                stars.pop()
            except:
                stars="None"
            
            creators_string = ""
            stars_string = ""
            for s in stars:
                stars_string = stars_string + s + "  " 
            for c in creators:
                creators_string = creators_string + c + "  "    
                
            try :
                meta = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[3]/div[1]/a/div/span").text
            except:
                meta = "None"
            
            # collecting reviews and critics information    
            rew=psw.find_elements_by_xpath("//span[@class='subText']")
            if(len(rew)==2):
                rc=rew[0].find_elements_by_tag_name('a')
                try:
                    reviews=rc[0].text
                except:
                    reviews="None"
                try:
                    critics=rc[1].text
                except:
                    critics="None"
                popularity=rew[1].text
            if(len(rew)==3):
                rc=rew[1].find_elements_by_tag_name('a')
                try:
                    reviews=rc[0].text
                except:
                    reviews="None"
                try:
                    critics=rc[1].text
                except:
                    critics="None"
                popularity=rew[2].text  # popularity information
            
            if reviews!="None" :
                reviews = reviews[0:len(reviews)-5]
              
            if critics!="None" :
                critics = critics[0:len(critics)-7] 
               
            # popularity up_down information 
            try :
                pop = driver.find_element_by_xpath("//span[@class='popularityUpOrFlat']").text
            except :
                pop = "None"

            if pop=="None":
                try :
                    pop = driver.find_element_by_xpath("//span[@class ='popularityDown']").text
                    pop = "-"+pop
                except :
                    pop = "None"    
            try :    
                title = driver.find_element_by_xpath("//h4[text()='Country:']/parent::div")    
                title_name = title.find_element_by_tag_name('a').text
                
            except :
                title_name = "None" 
            try :    
                tim = driver.find_element_by_xpath("//div[@class='subtext']") 
                time_duration = tim.find_element_by_tag_name('time').text
            except :
                time_duration = "None"    
            
            try : 
                votes =  driver.find_element_by_xpath("//span[@itemprop='ratingCount']").text
            except :
                votes = "None "
            try :
                certificate = driver.find_element_by_xpath("//h4[text()='Certificate:']/parent::div")
                certi = certificate.find_elements_by_tag_name('span')
                certificate = certi[0].text
            except :
                certificate = "None"
            #print(certificate)            
            #print(votes)  
            

            # writing in a csv file
            csv_writer.writerow([header_list[i],lista[i],listb[i],ratinglist[i],tvormovie[i],title_name,time_duration,genre,votes,reviews,meta,certificate,critics,creators_string,stars_string,popularity.split()[0],pop])
    Initiate_Driver.closebrowser()
    
csv_file.close()
