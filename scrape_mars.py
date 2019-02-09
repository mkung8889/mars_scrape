import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # executable_path = {'executable_path': 'C:/Users/Office fdpa/Dropbox/Homework/chromedriver.exe'}
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()

    # NASA Mars News
    news_url="https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(5)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html,'html.parser')
    news_results = news_soup.find_all('li',class_='slide')
    news_titles = []
    for result in news_results:
        news_title = result.find('div',class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text
        dict_entry={
            'news_title': news_title,
            'news_p': news_p
        }
        news_titles.append(dict_entry)
    latest_news = news_titles[0]

    # JPL Mars Space Images - Featured Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html,'html.parser')
    partial_img_url = jpl_soup.find('footer').find('a', class_='button fancybox')['data-fancybox-href']
    large_url = partial_img_url.replace('mediumsize','largesize')
    large_url = large_url.replace('_ip', '_hires')
    featured_img_url = f"https://www.jpl.nasa.gov{large_url}"

    # Mars Facts
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html,'html.parser')
    twitter_results = twitter_soup.find_all('li', class_='js-stream-item')
    mars_weather = []
    for results in twitter_results:
        weather = results.find('p', class_='TweetTextSize').text
        if weather.split(' ')[0] == 'Sol':
            mars_weather.append(weather)
    latest_weather = mars_weather[0]

    # Mars Facts
    facts_url = "http://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    facts_soup = BeautifulSoup(facts_html,'html.parser')
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Description','Value']
    mars_facts = df.to_html(index=False)


    # Mars Hemispheres
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html,'html.parser')
    hemisphere_results = hemisphere_soup.find_all('div', class_='item')
    hemisphere_img_url = []
    for result in hemisphere_results:
        title = result.find('h3').text
        browser.find_by_text(title).click()
        img_url = browser.find_link_by_text('Sample')['href']
        dict_entry = {
            'title': title,
            'img_url': img_url
        }
        hemisphere_img_url.append(dict_entry)
        browser.find_link_by_text('Back').click()

    mars_data = {
        'latest_news': latest_news,
        'featured_img': featured_img_url,
        'latest_weather': latest_weather,
        'facts': mars_facts,
        'hemisphere_img': hemisphere_img_url
        }

    return mars_data