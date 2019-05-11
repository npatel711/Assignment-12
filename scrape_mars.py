from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
import requests 

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    mars = {}
    browser= init_browser()

    #Scrape NASA Mars News site for News title and paragraph text
    url= 'https://mars.nasa.gov/news/'
    response= requests.get(url)
    soup= bs(response.text, 'html.parser')

    #get news title and paragraph text and save as variables
    news_title= soup.find("div", class_="content_title").text
    news_p= soup.find("div", class_="rollover_description_inner").text

    #Scrape JPL Featured Space images. Use splinter to find current feature Mars full-size image and assign to variable
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html= browser.html
    im_soup=bs(html,'html.parser')
    featured_image= im_soup.select('li.slide a.fancybox')

    #make a list of just the data-fancybox-hrefs
    img_list = [i.get('data-fancybox-href') for i in featured_image]

    #combine the base url with the first img url
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + img_list[0]   

    #Mars weather twitter. Scrape latest Mars weather tweet from the page and save as a variable.
    url= 'https://twitter.com/marswxreport?lang=en'
    tw_response= requests.get(url)
    tw_soup= bs(tw_response.text, 'html.parser')

    #create list of weather tweets
    weather_list= []
    for weather_info in tw_soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_list.append(weather_info.text.strip())

    #add conditional to get Sol info
    for tweet in reversed (weather_list):
        if tweet[:3]=="InS":
            mars_weather=tweet

    #Mars facts
    mars_url= 'https://space-facts.com/mars/'
    mars_table= pd.read_html(mars_url)
    mars_table

    mars_df= mars_table[0]
    
    mars_df.set_index(0, inplace=True)
    
    mars_df.index.names= [None]
    mars_df.columns= ['']

    mars_df_html=mars_df.to_html()
    mars_df_html

    mars_df_html.replace('\n','')

    mars_html= mars_df.to_html()

    #Mars Hemispheres
    mars_hem_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_hem_response= requests.get(mars_hem_url)
    soup= bs(mars_hem_response.text, 'html.parser')
    mars_hem= soup.find_all('a', class_='itemLink product-item')

    hem_image_urls=[]
    for hem_image in mars_hem:
        im_title= hem_image.find('h3').text
        link= "https://astrogeology.usgs.gov" + hem_image['href']
        im_request= requests.get(link)
        soup= bs(im_request.text, "html.parser")
        img_tag=soup.find("div", class_="downloads").find('ul').find('li')
        img_url= img_tag.a['href']
        hem_image_urls.append({"Title":im_title, "Image_url": img_url})

    mars= {
        "title": news_title,
        "text": news_p,
        "image": featured_image_url,
        "weather": mars_weather,
        "facts": mars_html,
        "hemispheres": hem_image_urls
    }
    
    browser.quit()

    return mars