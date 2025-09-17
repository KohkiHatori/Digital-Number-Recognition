"""
Web Scraping Module for Digital Display Images

This module scrapes Google Images to collect training data for the alcohol
detection ML model. It searches for various digital displays (alcohol checkers,
digital clocks, calculators, etc.) and downloads images for manual labeling.

Developed for ML training data collection during internship at Second Xight Analytica.
"""

from bs4 import BeautifulSoup
import os, requests, lxml, re, json, unicodedata, urllib, socket, certifi, ssl
from urllib.request import build_opener, install_opener, urlopen, HTTPSHandler

context=ssl.create_default_context(cafile=certifi.where())
https_handler = HTTPSHandler(context=context)

NUM_PAGE = 2
# TO_SEARCH = ["体温計", "アルコールチェッカー", "デジタル時計", "ストップウォッチ" "Digital clock", "Digital thermometer", "alcohol checker", "Digital watch", "Digital stop watch"]
# TO_SEARCH = ["電卓", "Calculator"]
TO_SEARCH = ["Digital Scale", "エアコンのリモコン"]
DESTINATION = "/mnt/nas2/gbr/python/adhoc_src/sx_intern/deliverly/03_データ収集/scraped_dataset"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
JP_params = {
        "q": None,
        "tbm": "isch",
        "hl": "jp",
        "gl": "jp",
    }
US_params = {
        "q": None,
        "tbm": "isch",
        "hl": "en",
        "gl": "us",
    }

def get_html(word, params):
    """
    Fetch HTML content from Google Images search.

    Args:
        word: Search term for Google Images
        params: URL parameters for the search

    Returns:
        requests.Response: HTTP response from Google Images
    """
    headers = {
        "User-Agent": USER_AGENT
    }
    params["q"] = word
    return requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

def make_soup(html):
    return BeautifulSoup(html.text, "lxml")

def extract_image_data(script_tags):
    images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(script_tags)))
    images_data_fix = json.dumps(images_data)
    images_data_json = json.loads(images_data_fix)
    google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', images_data_json)
    return google_image_data

def remove_thumbnails(google_image_data):
    no_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(google_image_data))
    return no_thumbnails

def get_full_res(no_thumbnails):
    google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", no_thumbnails)
    full_res_images = []
    for fixed_image in google_full_resolution_images:
        not_fixed = bytes(fixed_image, "ascii").decode("unicode-escape")
        full_res_image = bytes(not_fixed, "ascii").decode("unicode-escape")
        full_res_images.append(full_res_image)
    return full_res_images

def save(image_url, index, parent_index):
    print(f"Downloading image{index} ...")
    opener= build_opener(https_handler)
    opener.addheaders=[("User-Agent", USER_AGENT)]
    install_opener(opener)
    try:
        data = urlopen(image_url, timeout=10).read()
        with open(os.path.join(DESTINATION, f"{parent_index}img_{index}.jpg"), "wb") as f:
            f.write(data)
    except (socket.timeout, urllib.error.URLError) as e:
        pass

def get_original_images(soup, parent_index):
    script_tags = soup.select("script")
    google_image_data = extract_image_data(script_tags)
    no_thumbnails = remove_thumbnails(google_image_data)
    full_res_images = get_full_res(no_thumbnails)
    for index, image_url in enumerate(full_res_images):
        save(image_url, index, parent_index)

def is_japanese(word):
    for ch in word:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    return False

def main():
    """
    Main scraping pipeline.

    Iterates through search terms, determines language, and downloads
    images from Google Images for ML training data collection.
    """
    for parent_index, word in enumerate(TO_SEARCH):
        print(f"Scraping images for: {word}")

        # Choose appropriate language parameters
        if is_japanese(word):
            html = get_html(word, JP_params)
        else:
            html = get_html(word, US_params)

        # Parse HTML and download images
        soup = make_soup(html)
        get_original_images(soup, parent_index + 10)

if __name__ == "__main__":
    main()
