# Dependencies
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from pprint import pprint
from time import sleep

# Create a init_browser function to visit urls
def init_browser():
    return Browser("firefox", headless=False)

# Create a scrape function to scrape websites
def scrape():
    browser = init_browser()

    # ======================================NASA Mars News======================================
    # URL of page to be scraped
    url_news = "https://mars.nasa.gov/news"

    # Retrieve page with the requests module
    response_news = requests.get(url_news)

    # Create BeautifulSoup object; parse with 'html5lib'
    soup_news = bs(response_news.text, "html5lib")

    # Scrape the NASA Mars News Site and collect the latest News Title
    news_title = soup_news.find("div", class_="content_title").text.strip()

    # Scrape the NASA Mars News Site and collect Paragraph Text
    news_p = soup_news.find("div", class_="rollover_description_inner").text.strip()


    # ======================================JPL Mars Space Images======================================
    # URL of page to be scraped
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Visit the url for JPL Featured Space Image
    browser.visit(url_img)

    # HTML object
    html_img = browser.html

    # Parse HTML with Beautiful Soup
    soup_image = bs(html_img, "lxml")

    # Find the image url for the current Featured Mars Image
    image_url = soup_image.find("li", class_="slide").find('a', class_="fancybox")['data-fancybox-href']

    # Assign the url string to a variable called featured_image_url
    featured_image_url = "https://www.jpl.nasa.gov/"+image_url


    # ======================================Mars Weather======================================
    # URL of page to be scraped
    url_weather = "https://www.twitter.com/marswxreport"

    # Visit the Mars Weather twitter account
    # browser_weather = Browser("firefox", headless=True)
    browser.visit(url_weather)
    sleep(3)

    # HTML object
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup_weather = bs(html_weather, "html5lib")

    # Scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather
    article_weather = soup_weather.find_all("article", role="article")
    mars_weather = ""

    # Loop through all posts to find "span", then look through all "span" to find text that start with "InSight", since not all posts are related to the weather on Mars
    for article in article_weather:
        text_weather = article.find_all("span")
        for wea in text_weather:
            if wea.text.startswith("InSight"):
                mars_weather= wea.text
                break
        if mars_weather:
            break

    # ======================================Mars Facts======================================
    # URL of page to be scraped
    url_facts = "https://space-facts.com/mars/"

    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    tables = pd.read_html(url_facts)
    mars_table = tables[0]
    mars_table = mars_table.rename(columns={0:"", 1:"value"}).set_index("")

    # Use Pandas to convert the data to a HTML table string
    html_mars_table = mars_table.to_html(classes="mars-table").replace("\n", "").replace("text-align: right", "text-align: left")

    # ######Convert the data to a HTML table string and save as html file
    mars_table.to_html("mars_table.html")
    
    # ======================================Mars Hemispheres======================================
    # Visit the USGS Astrogeology site 
    url_main = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Retrieve page with the requests module
    response_main = requests.get(url_main)

    # Parse HTML with Beautiful Soup
    soup_main = bs(response_main.text, "html5lib")

    # Find all products in results
    url_all = soup_main.find_all("div", class_="item")

    # Create an empty list
    url_list=[]

    # List all urls for each links to the hemispheres
    for sub_url in url_all:
        new_url = sub_url.find("a", class_="itemLink")["href"]
        new_url = "https://astrogeology.usgs.gov/"+new_url
        url_list.append(new_url)

    # Create an empty list and dictionary
    hemisphere_image_urls = []
    hem_dict = {}

    # Loop through all urls to save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name
    for hem_url in url_list:
        hem_response = requests.get(hem_url)
        hem_soup = bs(hem_response.text, "html5lib")
        hem_img = hem_soup.find("img", class_="wide-image")["src"]
        hem_img = "https://astrogeology.usgs.gov/"+hem_img
        hem_title = hem_soup.find("h2", class_="title").text
        hem_dict = {"title": hem_title, "img_url": hem_img}
        hemisphere_image_urls.append(hem_dict)

    # Create a dictionary that includes all the information we scraped
    mars_dic = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_mars_table": html_mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    # Return all information
    return mars_dic
    