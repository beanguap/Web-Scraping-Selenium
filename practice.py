from requests.api import get
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
import time
from PIL import Image

# Path for Webdriver

PATH = "/Users/jerielmartinez/Desktop/Web Scraping Images/chromedriver"

wd = webdriver.Chrome(PATH)


# Function that defines pulling of images/scrolling of webpage.


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

# Url of the website and pulling.

    url = "https://www.google.com/search?q=dogs&tbm=isch&ved=2ahUKEwikqqut5fPzAhUEBd8KHRCmCg4Q2-cCegQIABAA&oq=dogs&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIICAAQgAQQsQMyBAgAEEMyBAgAEEM6BggAEAgQHlDwBljwBmD7CGgAcAB4AIABRIgBgQGSAQEymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=yBh-YaSmJISK_AaQzKpw&bih=1242&biw=699"
    wd.get(url)

    image_urls = set()

    while len(image_urls) < max_images:
        scroll_down(wd)

# Get all image thumbnail results.

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls):max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print("Found image!")

    return image_urls


# Function that defines the path and download of imgs

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)


urls = get_images_from_google(wd, 2, 10)

for i, url in enumerate(urls):
    download_image("imgs/", url, str(i) + ".jpg")


wd.quit()
