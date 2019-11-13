from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\\JMadd\\git\\web-scraping-challenge\\Missions_to_Mars"}
    return Browser("chrome", **executable_path, headless=False)



# NASA MARS NEWS
def scrape_mars_news():
    try: 

       
        browser = init_browser()

        browser.is_element_present_by_css("div.content_title", wait_time=1)

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # Parse HTML
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve the latest thing that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()


# FEATURED IMAGE
def scrape_mars_image():

    try: 

        
        browser = init_browser()

        browser.is_element_present_by_css("img.jpg", wait_time=1)

        # go to spaceimages
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)


        # Parse HTML
        html_image = browser.html
        soup = BeautifulSoup(html_image, 'html.parser')

        # get image
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # add together
        featured_image_url = main_url + featured_image_url

        featured_image_url 

    
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()

# Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # Parse HTML
        html_weather = browser.html
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve elements that contain news title
        for tweet in latest_tweets: 
            mars_weather_tweet = tweet.find('p').text
            # Run only if sol, and pressure are available
            if 'Sol' and 'pressure' in weather_tweet:
                print(mars_weather_tweet)
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['mars_weather'] = mars_weather_tweet
        
        return mars_info
    finally:

        browser.quit()


            


# Mars Facts
def scrape_mars_facts():

    # parse html with Pandas
    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']


    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry
    mars_info['mars_facts'] = data

    return mars_info

# MARS HEMISPHERES


def scrape_mars_hemi():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # Parse HTML
        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 

            # Store title
            title = i.find('h3').text
            
            # Store link
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # Parse HTML for every individual hemisphere information website
            partial_img_html = browser.html 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # get full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Aadd to list
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()