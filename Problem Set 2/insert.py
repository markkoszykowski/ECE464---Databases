# Mark Koszykowski
# ECE464 - Problem Set 2
# Web Scraping Code

# Web Scraping Reviews from IMDB's most reviewed film according to Google (The Shawshank Redemption)

import datetime
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://root:ece464@idmb.zqkw5.mongodb.net/admin')
db = client.reviews
db.The_Shawshank_Redemption.delete_many({})

url = "https://www.imdb.com/title/tt0111161/reviews"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

while True:
    try:
        loadmore = driver.find_element_by_id("load-more-trigger")
        driver.implicitly_wait(10)
        loadmore.click()
    except ElementNotInteractableException:
        break

html_soup = BeautifulSoup(driver.page_source, "lxml")
reviews_containers = html_soup.find_all("div", class_="imdb-user-review")

print(F"Finished web scraping, {len(reviews_containers)} reviews scraped")

for review in reviews_containers:
    title = review.find("a", class_="title").text.strip()

    # Rating is not a required field of a review
    try:
        rating = int(review.find_all("span")[1].text.strip())
    except:
        rating = None

    rev = review.find("div", class_="show-more__control").text.strip()
    month = datetime.datetime.strptime(review.find("span", class_="review-date").text.strip().split()[1], "%B").month
    day = int(review.find("span", class_="review-date").text.strip().split()[0])
    year = int(review.find("span", class_="review-date").text.strip().split()[2])
    user = review.find("span", class_="display-name-link").text.strip()
    spoiler = bool(review.find("span", class_="spoiler-warning"))
    foundHelpful = int(review.find("div", class_="actions").text.strip().split()[0].replace(',', ''))
    totalHelpful = int(review.find("div", class_="actions").text.strip().split()[3].replace(',', ''))
    reviewLink = review.find("a", class_="title")['href']
    userLink = review.find("span", class_="display-name-link").a['href']

    if rating is not None:
        entry = {
            "title": title,
            "review": rev,
            "ratingOutof10" : rating,
            "date": {
                "month": month,
                "day": day,
                "year": year
            },
            "user": user,
            "spoiler": spoiler,
            "foundHelpful": foundHelpful,
            "totalHelpful": totalHelpful,
            "reviewLink": "https://www.imdb.com" + reviewLink,
            "userLink": "https://www.imdb.com" + userLink
        }
    else:
        entry = {
            "title" : title,
            "review" : rev,
            "date" : {
                "month" : month,
                "day" : day,
                "year" : year
            },
            "user" : user,
            "spoiler" : spoiler,
            "foundHelpful" : foundHelpful,
            "totalHelpful" : totalHelpful,
            "reviewLink" : "https://www.imdb.com" + reviewLink,
            "userLink" : "https://www.imdb.com" + userLink
        }
    db.The_Shawshank_Redemption.insert_one(entry)