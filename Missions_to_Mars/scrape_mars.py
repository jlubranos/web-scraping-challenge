from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
#from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/jlubr/bin/chromedriver_win32/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

# Latest Mars News
    browser=init_browser()
    url='https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(10)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    news_title=str(soup.find('div',{'class':['bottom_gradient']}))
    news_p=str(soup.find('div',{'class':['article_teaser_body']}))
    ltitle=re.search('<h3>(.*?)</h3>',news_title)
    ltitle=str(ltitle.group(1))
    lparagraph=re.search('>(.*?)</div>',news_p)
    lparagraph=str(lparagraph.group(1))

# JPL Mars Space Images - Feature Image

    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    moreinfo=browser.html
    moreinfosoup=BeautifulSoup(moreinfo,'html.parser')
    find=str(moreinfosoup.find('figure',{'class':['lede']}))
    image=find.split('<a href="')[1]
    image=image.split('">')[0]
    featured_image_url=url.split('/spaceimages/?')[0] + image

# Mars Facts

    url="https://space-facts.com/mars"
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    table=soup.find('tbody')
    column_one=table.find_all('td',{'class':['column-1']})
    column_two=table.find_all('td',{'class':['column-2']})
    col_one=[]
    col_two=[]
    for i in range(len(column_one)):
        col_one.append(str(column_one[i].text).split(':')[0])
        col_two.append(str(column_two[i].text))
    facts_df=pd.DataFrame({"Description":col_one,"Mars":col_two})
    facts_df.set_index("Description",inplace=True)
    html=facts_df.to_html()
    facts_html = html.replace('<th>','<th align="left">')
    facts_file = open("Marsfacts.html", "w") 
    facts_file.write(facts_html) 
    facts_file.close()

# Mars Hemispheres

    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1-target&v1=Mars"
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    links=soup.find_all('a',{'class':['itemLink product-item']})
    hemisphere_image_urls=[]
    image_url={}
    for link in links:
        title=str(link.get_text())
        if len(title)>0:
            url=str(link.get('href'))
            image_url['title']=title
            image_jpg='https://astrogeology.usgs.gov'+url
            browser.visit(image_jpg)
            html=browser.html
            soup=BeautifulSoup(html,'html.parser')
            image=soup.find('img',{'class':['wide-image']})
            image_url['url']='https://astrogeology.usgs.gov' + str(image.get('src'))
            browser.back()
            hemisphere_image_urls.append(dict(image_url))
    browser.quit()

 # Store data into dictionary --> mars_data

    mars_data = {
        "newstitle":ltitle,
        "news_p":lparagraph,
        "fimageurl":featured_image_url,
        "marsfacts":str(facts_html),
        "himageurls":hemisphere_image_urls
    }
 
# Close the browser after scraping
    browser.quit()


# Return results
    return mars_data
