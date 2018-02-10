# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from random import shuffle
import requests
from Data import Country
from Connection import save

CATEGORY_LIST = {
    'general': 'n',
    'business': 'b',
    'entertainment': 'e',
    'sport': 's',
    'technology': 't',
    'world': 'w'
}
COUNTRIES_LIST_API_GNEWS = [
    Country('Argentina', 'ar', ['es', 'es-419'], None, 'es_ar', CATEGORY_LIST, None),
    Country('Brazil', 'br', ['pt', 'pt-BR'], None, 'pt-BR_br', CATEGORY_LIST, None),
    Country('Canada', 'ca', ['fr', 'fr-ca'], None, 'fr_ca', CATEGORY_LIST, None),
    Country('Chile', 'cl', ['es', 'es-419'], None, 'es_cl', CATEGORY_LIST, None),
    Country('Colombia', 'co', ['es', 'es-419'], None, 'es_co', CATEGORY_LIST, None),
    Country('Cuba', 'cu', ['es', 'es-419'], None, 'es_cu', CATEGORY_LIST, None),
    Country('France', 'fr', ['fr', 'fr'], None, 'fr', CATEGORY_LIST, None),
    Country('Germany', 'de', ['de', 'de'], None, 'de', CATEGORY_LIST, None),
    Country('Israel', 'il', ['he', 'iw'], None, 'iw_il', CATEGORY_LIST, None),
    Country('Italy', 'it', ['it', 'it'], None, 'it', CATEGORY_LIST, None),
    Country('Mexico', 'mx', ['es', 'es-419'], None, 'es_mx', CATEGORY_LIST, None),
    Country('Netherlands', 'nl', ['nl', 'nl'], None, 'nl_nl', CATEGORY_LIST, None),
    Country('Peru', 'pe', ['es', 'es-419'], None, 'es_pe', CATEGORY_LIST, None),
    Country('Poland', 'pl', ['pl', 'pl'], None, 'pl_pl', CATEGORY_LIST, None),
    Country('Portugal', 'pt', ['pt', 'pt-PT'], None, 'pt-PT_pt', CATEGORY_LIST, None),
    Country('Russia', 'ru', ['ru', 'ru'], None, 'ru_ru', CATEGORY_LIST, None),
    Country('South Africa', 'za', ['en', 'en'], None, 'en_za', CATEGORY_LIST, None),
    Country('United Arab Emirates', 'ae', ['ar', 'ar'], None, 'ar_ae', CATEGORY_LIST, None),
    Country('Venezuela', 've', ['es', 'es-419'], None, 'es_ve', CATEGORY_LIST, None),
]
ARTICLES_JSON_FORMAT = {"articles": [], "category_name": ""}
global ARTICLE_DETAIL_FORMAT

def load():
    global articles
    for i, country in enumerate(COUNTRIES_LIST_API_GNEWS):
        for j, category in enumerate(country.categories):
            articles = []
            req = requests.get(
                "http://www.rssdog.com/index.htm?url=http%3A%2F%2Fnews.google.com%2Fnews%3Fpz%3D1%26cf%3Dall%26ned%3D{}%26hl%3D{}%26gl%3D{}%26topic%3D{}%26output%3Drss%26num%3D30&mode=html&showonly=&maxitems=0&showdescs=1&desctrim=0&descmax=0&tabwidth=100%25&showdate=1&utf8=1&linktarget=_blank&textsize=inherit&bordercol=%23d4d0c8&headbgcol=%23999999&headtxtcol=%23ffffff&titlebgcol=%23f1eded&titletxtcol=%23000000&itembgcol=%23ffffff&itemtxtcol=%23000000&ctl=0"
                    .format(country.edition_code_gnews, country.language_code[1], country.country_code,
                            country.categories[category]))  # edition, language, country, topic
            bs = BeautifulSoup(req.text, 'html.parser')
            titles = bs.find_all('a', {'class': 'rssdog'})
            titles.pop(0)
            titles.pop(0)
            image_url = bs.find_all('img', {'class': 'rssdog'})
            description = bs.find_all('font', {'size': '-1'})
            publishedAt = bs.find_all('i')
            publishedAt.pop(0)
            for index in range(len(image_url)):
                ARTICLE_DETAIL_FORMAT = {"description": "", "publishedAt": "", "source": {"name": ""}, "title": "",
                                         "url": "",
                                         "urlToImage": ""}
                ARTICLE_DETAIL_FORMAT["title"], ARTICLE_DETAIL_FORMAT["source"]["name"] = splitTitle(titles[index].text)
                (ARTICLE_DETAIL_FORMAT["publishedAt"],ARTICLE_DETAIL_FORMAT["url"],
                 ARTICLE_DETAIL_FORMAT["urlToImage"]) = publishedAt[index].text, titles[index]['href'],\
                                                        'http://'+image_url[index]['src'][2:]
                articles.append(ARTICLE_DETAIL_FORMAT)
            count = 0
            for desc in description:
                if len(desc.text) > 150 and count < len(image_url):
                    articles[count]["description"] = desc.text
                    count += 1
            shuffle(articles)
            (ARTICLES_JSON_FORMAT["articles"], ARTICLES_JSON_FORMAT["category_name"]) = articles, category
            save('/APIs/1/countries/%s/news/categories/' % i, '%s' % j, ARTICLES_JSON_FORMAT)

def splitTitle(title):
    global title_splited, aux, source_complete
    title_splited = ''
    source_complete = ''
    aux = ''
    if title.count('-') >= 3:
        title_splited, aux, source_complete = tuple(title.rsplit('-', 2))
        source_complete = aux.strip() + '-' + source_complete
    else:
        title_splited, aux = tuple(title.rsplit('-', 1))
        source_complete = aux.strip()
    return (title_splited, source_complete)

def loadWorldCategoryUSA():
    articles = []
    req = requests.get(
        "http://www.rssdog.com/index.htm?url=http%3A%2F%2Fnews.google.com%2Fnews%3Fpz%3D1%26cf%3Dall%26ned%3D{}%26hl%3D{}%26gl%3D{}%26topic%3D{}%26output%3Drss%26num%3D30&mode=html&showonly=&maxitems=0&showdescs=1&desctrim=0&descmax=0&tabwidth=100%25&showdate=1&utf8=1&linktarget=_blank&textsize=inherit&bordercol=%23d4d0c8&headbgcol=%23999999&headtxtcol=%23ffffff&titlebgcol=%23f1eded&titletxtcol=%23000000&itembgcol=%23ffffff&itemtxtcol=%23000000&ctl=0"
            .format('us', 'en', 'us', 'w'))
    bs = BeautifulSoup(req.text, 'html.parser')
    titles = bs.find_all('a', {'class': 'rssdog'})
    titles.pop(0)
    titles.pop(0)
    image_url = bs.find_all('img', {'class': 'rssdog'})
    description = bs.find_all('font', {'size': '-1'})
    publishedAt = bs.find_all('i')
    publishedAt.pop(0)
    for index in range(len(image_url)):
        ARTICLE_DETAIL_FORMAT = {"description": "", "publishedAt": "", "source": {"name": ""}, "title": "",
                                 "url": "",
                                 "urlToImage": ""}
        ARTICLE_DETAIL_FORMAT["title"], ARTICLE_DETAIL_FORMAT["source"]["name"] = splitTitle(titles[index].text)
        (ARTICLE_DETAIL_FORMAT["publishedAt"], ARTICLE_DETAIL_FORMAT["url"],
         ARTICLE_DETAIL_FORMAT["urlToImage"]) = publishedAt[index].text, titles[index]['href'], \
                                                'http://'+image_url[index]['src'][2:]
        articles.append(ARTICLE_DETAIL_FORMAT)

    count = 0
    for desc in description:
        if len(desc.text) > 150 and count < len(image_url):
            articles[count]["description"] = desc.text
            count += 1
    shuffle(articles)
    (ARTICLES_JSON_FORMAT["articles"], ARTICLES_JSON_FORMAT["category_name"]) = articles, 'world'
    save('/APIs/0/countries/0/news/categories/', '5', ARTICLES_JSON_FORMAT)

def loadTechCategoryUK():
    articles = []
    req = requests.get(
        "http://www.rssdog.com/index.htm?url=http%3A%2F%2Fnews.google.com%2Fnews%3Fpz%3D1%26cf%3Dall%26ned%3D{}%26hl%3D{}%26gl%3D{}%26topic%3D{}%26output%3Drss%26num%3D30&mode=html&showonly=&maxitems=0&showdescs=1&desctrim=0&descmax=0&tabwidth=100%25&showdate=1&utf8=1&linktarget=_blank&textsize=inherit&bordercol=%23d4d0c8&headbgcol=%23999999&headtxtcol=%23ffffff&titlebgcol=%23f1eded&titletxtcol=%23000000&itembgcol=%23ffffff&itemtxtcol=%23000000&ctl=0"
            .format('uk', 'en-GB', 'gb', 't'))
    bs = BeautifulSoup(req.text, 'html.parser')
    titles = bs.find_all('a', {'class': 'rssdog'})
    titles.pop(0)
    titles.pop(0)
    image_url = bs.find_all('img', {'class': 'rssdog'})
    description = bs.find_all('font', {'size': '-1'})
    publishedAt = bs.find_all('i')
    publishedAt.pop(0)
    for index in range(len(image_url)):
        ARTICLE_DETAIL_FORMAT = {"description": "", "publishedAt": "", "source": {"name": ""}, "title": "",
                                 "url": "",
                                 "urlToImage": ""}
        ARTICLE_DETAIL_FORMAT["title"], ARTICLE_DETAIL_FORMAT["source"]["name"] = splitTitle(titles[index].text)
        (ARTICLE_DETAIL_FORMAT["publishedAt"], ARTICLE_DETAIL_FORMAT["url"],
         ARTICLE_DETAIL_FORMAT["urlToImage"]) = publishedAt[index].text, titles[index]['href'], \
                                                'http://'+image_url[index]['src'][2:]
        articles.append(ARTICLE_DETAIL_FORMAT)

    count = 0
    for desc in description:
        if len(desc.text) > 150 and count < len(image_url):
            articles[count]["description"] = desc.text
            count += 1
    shuffle(articles)
    (ARTICLES_JSON_FORMAT["articles"], ARTICLES_JSON_FORMAT["category_name"]) = articles, 'technology'
    save('/APIs/0/countries/1/news/categories/', '4', ARTICLES_JSON_FORMAT)

def loadWorldCategoryUK():
    articles = []
    req = requests.get(
        "http://www.rssdog.com/index.htm?url=http%3A%2F%2Fnews.google.com%2Fnews%3Fpz%3D1%26cf%3Dall%26ned%3D{}%26hl%3D{}%26gl%3D{}%26topic%3D{}%26output%3Drss%26num%3D30&mode=html&showonly=&maxitems=0&showdescs=1&desctrim=0&descmax=0&tabwidth=100%25&showdate=1&utf8=1&linktarget=_blank&textsize=inherit&bordercol=%23d4d0c8&headbgcol=%23999999&headtxtcol=%23ffffff&titlebgcol=%23f1eded&titletxtcol=%23000000&itembgcol=%23ffffff&itemtxtcol=%23000000&ctl=0"
            .format('uk', 'en-GB', 'gb', 'w'))
    bs = BeautifulSoup(req.text, 'html.parser')
    titles = bs.find_all('a', {'class': 'rssdog'})
    titles.pop(0)
    titles.pop(0)
    image_url = bs.find_all('img', {'class': 'rssdog'})
    description = bs.find_all('font', {'size': '-1'})
    publishedAt = bs.find_all('i')
    publishedAt.pop(0)
    for index in range(len(image_url)):
        ARTICLE_DETAIL_FORMAT = {"description": "", "publishedAt": "", "source": {"name": ""}, "title": "",
                                 "url": "",
                                 "urlToImage": ""}
        ARTICLE_DETAIL_FORMAT["title"], ARTICLE_DETAIL_FORMAT["source"]["name"] = splitTitle(titles[index].text)
        (ARTICLE_DETAIL_FORMAT["publishedAt"], ARTICLE_DETAIL_FORMAT["url"],
         ARTICLE_DETAIL_FORMAT["urlToImage"]) = publishedAt[index].text, titles[index]['href'], \
                                                'http://'+image_url[index]['src'][2:]
        articles.append(ARTICLE_DETAIL_FORMAT)

    count = 0
    for desc in description:
        if len(desc.text) > 150 and count < len(image_url):
            articles[count]["description"] = desc.text
            count += 1
    shuffle(articles)
    (ARTICLES_JSON_FORMAT["articles"], ARTICLES_JSON_FORMAT["category_name"]) = articles, 'world'
    save('/APIs/0/countries/1/news/categories/', '5', ARTICLES_JSON_FORMAT)


if __name__ == '__main__':
    loadWorldCategoryUSA()
    loadTechCategoryUK()
    loadWorldCategoryUK()
    load()
