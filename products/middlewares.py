class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("This is printed before the view is called")

        # check request header
        if "Something-Header" not in request.headers:
            raise Exception("Header is missing")

        response = self.get_response(request)

        print("This is printed after the view is called")
        # Code to be executed for each request/response after
        # the view is called.
        response['context'] = {"message": "This is a simple middleware"}
        response['Custom-Header'] = "This is a custom header"

        return response


import requests
from django.http import HttpResponse

# Previous imports and timing middleware should remain unchanged


def stackoverflow(get_response):
    def middleware(request):
        # This method does nothing, all we want is exception processing
        return get_response(request)

    def process_exception(request, exception):
        url = 'https://api.stackexchange.com/2.2/search'
        params = {
            'site': 'stackoverflow',
            'order': 'desc',
            'sort': 'votes',
            'pagesize': 3,
            'tagged': 'python;django',
            'intitle': str(exception),
        }
        response = requests.get(url, params=params)
        html = ''
        for question in response.json()['items']:
            html += '<h2><a href="{link}">{title}</a></h2>'.format(**question)
        return HttpResponse(html)

    middleware.process_exception = process_exception

    return middleware