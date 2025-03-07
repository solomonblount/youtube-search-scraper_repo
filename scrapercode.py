# https://selenium-python.readthedocs.io/waits.html

from selenium import webdriver
from selenium.webdriver.common.by import By
# importing keys allows selenium to use keyboard keys to auto-type
from selenium.webdriver.common.keys import Keys
# importing time allows selenium to count in seconds
import time
import mysql.connector

# Connect to sql database
connectSQL = mysql.connector.connect(
    host="localhost",
    user="root",
    password="o@G6Exybga3R?!s?",
    database="scrapeyt2025")
# cursor is an object used to execute SQL queries on the database
myCursor = connectSQL.cursor()

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH

try:
    # Open YouTube
    driver.get("https://www.youtube.com")

    # Find the search box and enter the search query
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("how to data scrape youtube")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(5)  # Adjust the sleep time if necessary

    # Find all video titles on the results page
    video_titles = driver.find_elements(By.XPATH, '//a[@id="video-title"]')

    # Print each video title
    titles = []
    for title in video_titles:
        titles.append(title.text)
        print(title.text)

    # Find all view counts and upload dates
    views_date = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]')

    # Print each view count and date
    metadatas = []
    for metadata in views_date:
        metadatas.append(metadata.text)
        print(metadata.text)

    # Find all channel names
    channel_name = driver.find_elements(By.XPATH, '//ytd-channel-name[@id="channel-name"]')

    # Print each channel name
    channels = []
    for channel in channel_name:
        channels.append(channel.text)
        print(channel.text)

    # Find all video links in the search results
    video_elements = driver.find_elements(By.CSS_SELECTOR, "a#video-title")

    # Get the video links (href attribute)
    links = []
    for video_element in video_elements:
        video_link = video_element.get_attribute("href")
        links.append(video_link)
        print(video_link)


    # Put scraped data in rows, then print them
    data = list(zip(titles, metadatas, channels, links))
    print(data)

    # Insert pairs into workbench table
    myCursor.executemany("INSERT INTO viddata (Title, ViewsDate, Channel, Link) VALUES (%s, %s, %s, %s)", data)
    connectSQL.commit()

finally:
    # driver.quit closes the pop-up browser, driver.close would just close the current tab
    driver.quit()
    # closes cursor
    myCursor.close()
    # closes sql workbench connection
    connectSQL.close()
