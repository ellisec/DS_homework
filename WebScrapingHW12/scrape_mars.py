from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time


def init_browser():

#Executable path to driver
    executable_path={'executable_path':'C:/Users/ellis/Downloads/chromedriver_win32/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# # NASA MARS NEWS

def scrape():
    mars_info={}

    browser=init_browser()

    # URL of page to be scraped
    url='https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(2)

    # Scrape page into Soup
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find headline and summary
    news_title=soup.find('div',class_='content_title').find('a').text
    news_p=soup.find('div',class_='article_teaser_body').text

    mars_info["news_title"]=news_title
    mars_info["news_p"]=news_p

    
# # JPL MARS SPACE IMAGES

    browser=init_browser()

    # Visit url
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)
    #Scrape page
    image_html=browser.html
    soup=BeautifulSoup(image_html,'html.parser')


    #Find URL for featured image
    featured_image_url=soup.find('article')['style'].replace('background-image: url(','').replace(');','')
   
    featured_image_url=featured_image_url[1:-1]
    
    jpl_url='https://www.jpl.nasa.gov'

    #Base URL + Image URL
    featured_image_url=jpl_url+featured_image_url

    #Add image URL to dictionary
    mars_info["featured_image_url"]=featured_image_url

    #Close browser after scraping
    browser.quit()

# # MARS WEATHER

    browser=init_browser()

    #Visit url
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)

    #Scrape
    weather_html=browser.html
    soup=BeautifulSoup(weather_html,'html.parser')

    #Gather weather data from latest tweet
    tweets=soup.find('p',class_='TweetTextSize').text
    #Remove excess information
    mars_weather=tweets.replace('InSight','')

    #Add information to dictionary
    mars_info["mars_weather"]=mars_weather

    #Close browser after scraping
    browser.quit()

# # MARS FACTS

    browser=init_browser()

    #Visit url
    facts_url='https://space-facts.com/mars/'
    time.sleep(2)

    #Read tables
    tables=pd.read_html(facts_url)

    mars_facts_df=tables[0]
    
    #Format table
    mars_facts_df.columns=['','Value']
    mars_facts_df.set_index('',inplace=True)
    mars_facts_df

    #Transform table into hml
    mars_facts=mars_facts_df.to_html()

   #Add table to dictionary
    mars_info["mars_facts"]=mars_facts

    #Close browser after scraping
    browser.quit()

# # MARS HEMISPHERES

    browser=init_browser()

    #Visit url
    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    time.sleep(2)

    #Scrape
    hemi_html=browser.html
    soup=BeautifulSoup(hemi_html,'html.parser')

    #Find all information for mars hempisheres
    hemisphere=soup.find_all('div',class_='item')

    #Create empty list to store information
    hemisphere_image_url=[]

    #Loop through ifnormation found to identify image title and url
    for image in hemisphere:

        #Assign variable to title
        title=image.find('h3').text
        
        #Assign variable to link to full image page
        hemi_page_url=image.find('a',class_="itemLink product-item")['href']
        

        hemisphere_base_url='https://astrogeology.usgs.gov'
        
        #Visit full image page
        browser.visit(hemisphere_base_url+hemi_page_url)
        html=browser.html
        
        time.sleep(2)

        #Parse with Soup
        soup=BeautifulSoup(html,'html.parser')
        
        #Retrieve full image url
        img_url=soup.find('img',class_='wide-image')['src']
        
        #Append full image url to base url
        img_url= hemisphere_base_url + img_url
        
        #Add information to hempishere list
        hemisphere_image_url.append({'title':title,'image_url':img_url})

    mars_info["hemisphere_image_url"]=hemisphere_image_url

   
    browser.quit()

    return mars_info