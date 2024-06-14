from typing import List, Union

import requests
from bs4 import BeautifulSoup


def last_sport_news(url: str) -> Union[List[str], None]:
    """
    Return last 20 sport news.

    Args:
        url (str): url of destination site

    Returns:
        Union[List[str], None]: list of news containing date title and detail url.
    """
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        news_list = []
        for news_div in soup.find_all('div', class_="news-list__body"):
            date_time = news_div.find('span', class_='label__timestamp').text
            headline = news_div.find('a', class_="news-list__headline-link").text.strip()
            link = news_div.find('a', class_="news-list__headline-link")['href']
            news_list.append(f"{date_time} - {headline} - {link}")
        return news_list
    else:
        return []


sport_news_url = "https://www.skysports.com/news-wire"
news = last_sport_news(sport_news_url)
for item in news:
    print(item)
