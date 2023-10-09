import json
import random
import time

import bs4
import requests


def get_html(url: str) -> str:
    """
    Get html

    :param url: page address
    :return: html
    """
    response = requests.get(url)
    return response.text


def get_pages(html: str) -> int:
    """
    Get all pages of the site

    :param html: html
    :return: count pages
    """
    soup = bs4.BeautifulSoup(html, "lxml")
    count_advertisement_page = len(soup.find_all("div", "_93444fe79c--content--lXy9G"))
    total_advertisement_text = soup.find("div", "_93444fe79c--header--BEBpX").text
    total_advertisement_int = int("".join([nums for nums in total_advertisement_text if nums.isdigit()]))
    pages = total_advertisement_int // count_advertisement_page
    return pages


def get_data(url: str, pages: int) -> list:
    """
    Getting data from the page

    :param url: page address
    :param pages: page count
    :return: data from pages
    """
    data_content = []
    for page in range(1, pages + 1):
        response = requests.get(url.replace("p=1", f"p={page}"))
        html = response.text
        soup = bs4.BeautifulSoup(html, "lxml")
        content_full_data = soup.find_all("div", "_93444fe79c--content--lXy9G")
        for data in content_full_data:
            seller = data.find("div", "_93444fe79c--name-container--enElO").text
            title = data.find("div", "_93444fe79c--row--kEHOK").text
            another_title = None if data.find("div", "_93444fe79c--subtitle--vHiOV") is None else data.find("div",
                                                                                                            "_93444fe79c--subtitle--vHiOV").text
            address = data.find("div", "_93444fe79c--labels--L8WyJ").text
            price = data.find("div", "_93444fe79c--container--aWzpE").text
            price_per_square_meterice = data.find("p",
                                                  "_93444fe79c--color_gray60_100--MlpSF _93444fe79c--lineHeight_20px--tUURJ _93444fe79c--fontWeight_normal--P9Ylg _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6").text

            content = {
                "seller": seller,
                "title": title,
                "another_title": another_title,
                "address": address,
                "price": price,
                "price_per_square_meterice": price_per_square_meterice
            }

            data_content.append(content)

        wait_time = random.randint(1, 2)
        time.sleep(wait_time)
        print(f"Page number {page} is ready!!!")
    return data_content


def save_data(name_path: str, data: list, mode="w") -> None:
    """
    Save data in json file

    :param name_path: path to file
    :param data: data list
    :param mode: recording parameters
    """
    with open(name_path, mode=mode, encoding='utf-8') as save_in_json:
        json.dump(data, save_in_json, ensure_ascii=False)
    print("Saving successfully!!!")


if __name__ == "__main__":
    url = "https://omsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=1&region=4914&room3=1"
    html = get_html(url)
    pages = get_pages(html)
    data = get_data(url, pages)
    save_in_json = save_data("../data/data_about_apartments.json", data)
