import requests
import pandas as pd
from config import API_KEY


class NYTimesAPI:
    def __init__(self, api_key=API_KEY):
        """Initialize with API key from config.py"""
        self.api_key = api_key
        self.endpoints = {
            'article_search': "https://api.nytimes.com/svc/search/v2/articlesearch.json",
            'most_popular': "https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json",
            'movie_reviews': "https://api.nytimes.com/svc/movies/v2/reviews/search.json"
        }

    def make_request(self, endpoint, params=None):
        """Generic request handler"""
        params = params or {}
        params['api-key'] = self.api_key

        try:
            response = requests.get(self.endpoints[endpoint], params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Failed: {e}")
            return None

    def search_articles(self, query=None, **kwargs):
        """Search NYTimes articles"""
        params = {}
        if query:
            params['q'] = query  # NYTimes API uses 'q' parameter
        params.update(kwargs)
        return self.make_request('article_search', params)

    def get_most_popular(self, days=1):
        """Get most popular articles"""
        return self.make_request('most_popular', {'days': days})

    def search_movie_reviews(self, query=None, **kwargs):
        """Search movie reviews"""
        params = {}
        if query:
            params['query'] = query
        params.update(kwargs)
        return self.make_request('movie_reviews', params)

    def articles_to_dataframe(self, json_data):
        """Convert article search results to DataFrame"""
        articles = json_data.get('response', {}).get('docs', [])
        data = []

        for article in articles:
            data.append({
                'headline': article.get('headline', {}).get('main', ''),
                'abstract': article.get('abstract', ''),
                'url': article.get('web_url', ''),
                'date': article.get('pub_date', ''),
                'section': article.get('section_name', ''),
                'word_count': article.get('word_count', 0),
                'keywords': ', '.join([kw['value'] for kw in article.get('keywords', [])])
            })

        return pd.DataFrame(data)

    def movies_to_dataframe(self, json_data):
        """Convert movie reviews to DataFrame"""
        reviews = json_data.get('results', [])
        data = []

        for review in reviews:
            data.append({
                'title': review.get('display_title', ''),
                'mpaa_rating': review.get('mpaa_rating', ''),
                'critics_pick': review.get('critics_pick', 0),
                'summary': review.get('summary_short', ''),
                'review_url': review.get('link', {}).get('url', ''),
                'publication_date': review.get('publication_date', '')
            })

        return pd.DataFrame(data)