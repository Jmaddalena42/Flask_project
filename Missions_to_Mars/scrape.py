from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    time.sleep(5)
    mars = {}

    ## Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find("div", class_="content_title").find("a").text
    news_p = soup.find ("div", class_="article_teaser_body").text

    mars["news_title"] = news_title
    mars["news_p"] = news_p

    ## Mars Featured Image
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(5)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")
    partial_img = soup.find("img", class_ = "fancybox-image")["src"]
    featured_image_url = img_url[:24] + partial_img

    mars["featured_image_url"] = featured_image_url

    ## Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("div", class_="js-tweet-text-container")
    mars_weather = result.p.text

    mars["mars_weather"] = mars_weather

    ## Mars Facts
    facts_url = "http://space-facts.com/mars/"
    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]
    mars_df.columns = ["description", "value"]
    mars_df = mars_df.set_index("description")
    
    facts_html = mars_df.to_html()
    mars["facts_html"] = facts_html


    # Mars Hemispheres
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    time.sleep(5)
    mars_hemi_html = browser.html

    soup = BeautifulSoup(mars_hemi_html, 'html.parser')

    hemi_image_urls = []
    # Retreive all items that contain mars hemispheres information
    h3_soup = soup.find_all('div', class_='item')

    # Store the main_ul 
    hemi_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in h3_soup: 

        # Store title
        title = i.find('h3').text
            
        # Store link
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
        # Visit the link that contains the full image website 
        browser.visit(hemi_main_url + partial_img_url)

        time.sleep(5)
            
        # Parse HTML for every individual hemisphere information website
        partial_img_html = browser.html 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
            
        # get full image source 
        img_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
            
        # Aadd to list
        hemi_image_urls.append({"title" : title, "img_url" : img_url})

    mars["hemi_image_urls"] = hemi_image_urls

    browser.quit()

    return mars