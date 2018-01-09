class Country(object):
    name = ''
    country_code = ''
    language_code = ''
    edition_code_newsapi = ''
    edition_code_gnews = ''
    categories = []
    NEWSAPI_KEY = ''

    def __init__(self, name, country_code, language_code, edition_code_newsapi, edition_code_gnews, categories, api_key):
        self.name = name
        self.country_code = country_code
        self.language_code = language_code
        self.edition_code_newsapi = edition_code_newsapi
        self.edition_code_gnews = edition_code_gnews
        self.categories = categories if categories is not None else []
        self.NEWSAPI_KEY = api_key
