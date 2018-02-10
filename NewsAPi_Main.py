import requests
from Data import Country
from Connection import save

CATEGORY_LIST = [
    'general',
    'business',
    'entertainment',
    'sport',
    'technology',
]
COUNTRIES_LIST_API_NEWSAPI = [
    Country('USA', 'us', 'en', 'us', 'us', CATEGORY_LIST, '0811267b223b454a9698204d0888722a'), #api_email = zero_cruces@hotmail.com
    Country('United Kingdom', 'uk', 'en', 'gb', 'uk', CATEGORY_LIST, 'bc1069448aeb4cc0ab11f9253ff8b834'), #api_email = max.pp2222@gmail.com
]
ARTICLES_JSON_FORMAT = {"articles": [], "category_name": ""}

def load():
    for i, country in enumerate(COUNTRIES_LIST_API_NEWSAPI):
        for j, category in enumerate(country.categories):
            if country.edition_code_newsapi is not None:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?category=%s&language=%s&country=%s&apiKey=%s'
                    % (category, country.language_code, country.edition_code_newsapi, country.NEWSAPI_KEY))
                json = req.json().get('articles')
                (ARTICLES_JSON_FORMAT["articles"], ARTICLES_JSON_FORMAT["category_name"]) = json, category
                save('/APIs/0/countries/%s/news/categories/' % i, '%s' % j, ARTICLES_JSON_FORMAT)

if __name__ == '__main__':
    load()