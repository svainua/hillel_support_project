import random
import string
from typing import Callable

import httpx
from django.contrib import admin  # noqa
from django.http import HttpRequest, HttpResponse, JsonResponse  # noqa
from django.urls import path

create_random_string: Callable[[int], str] = lambda size: "".join(  # noqa
    [random.choice(string.ascii_letters) for i in range(size)]  # noqa
)  # noqa

# content = """
# <!DOCTYPE html>
# <html lang="en">
#     <head>
#         <meta charset="UTF-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1.0" />     #noqa
#         <title>Information fetching</title>
#         <link
#             href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
#             rel="stylesheet"
#             integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"   #noqa
#             crossorigin="anonymous"
#         />
#         <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
#     </head>
#     <body>
#         <h1>Information fetcher</h1>
#         <button id="generate" class="btn btn-primary">Fetch information</button>     #noqa
#         <button id="fetchMarket" class="btn btn-primary">Market</button>
#         <span id ="marketRate">NOT AVAILABLE</span>

#         <br />
#         <br />

#         <table class="table table-striped">
#             <tr>
#                 <th>Title</th>
#                 <th>Description</th>
#             </tr>
#             <tbody id="article-ideas"></tbody>
#         </table>


#         <script>
#             $(document).ready(function () {
#                 $("#fetchMarket").click(function () {
#                 $.ajax({
#                     url:"http://localhost:9000/fetch-market",
#                     type: "GET",
#                     success: function(data) {
#                         $("#marketRate").text(data.rate);
#                     },
#                     error: function(jqdata, status, error) {
#                         console.log(error);
#                         alert("An error was accured during generating the article idea");    #noqa
#                     },
#                 });
#                 });

#                 $("#generate").click(function () {
#                 $.ajax({
#                     url:"http://localhost:9000/generate-article",
#                     type: "GET",
#                     success: function(data) {
#                         const newItem = `<tr>
#                             <td>${data.title}</td>
#                             <td>${data.description}</td>
#                         </tr`;
#                         $("#article-ideas").append(newItem);
#                     },
#                     error: function(jqdata, status, error) {
#                         console.log(error);
#                         alert("An error was accured during generating the article idea");    #noqa
#                     },
#                 });
#                 });
#             });
#         </script>
#     </body>
# </html>
# """

# def generate_article_idea(request: HttpRequest) -> HttpResponse:  # отображает на веб-странице выше описанный html и JS код.   #noqa
#     return HttpResponse(content)

# def generate_article_idea(request: HttpRequest) -> HttpResponse:  #
#     content = "<h1>Hello World</h1>"
#     return HttpResponse(content)   # отдает на странице результат в виде text/html   #noqa


def generate_article_idea(request: HttpRequest) -> JsonResponse:
    content = {
        "title": create_random_string(size=10),
        "description": create_random_string(size=20),
    }
    return JsonResponse(
        content
    )  # отдает на странице результат в виде application/json


async def get_current_market_state(request: HttpRequest):
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=WQXS8S9M44M1B1BO"
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
    rate: str = response.json()["Realtime Currency Exchange Rate"][
        "5. Exchange Rate"
    ]
    return JsonResponse({"rate": rate})


async def get_exchange_rate(request: HttpRequest) -> HttpResponse:
    post_data = request.POST.copy()
    source = post_data.get("source")
    destination = post_data.get("destination")

    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={source}&to_currency={destination}&apikey=WQXS8S9M44M1B1BO"

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
    rate: str = response.json()["Realtime Currency Exchange Rate"][
        "5. Exchange Rate"
    ]

    result = f"The exchange rate for {source} and {destination} is {rate}."
    return JsonResponse(result)


urlpatterns = [
    # path("admin/", admin.site.urls),
    # передается не функция, а ее объект. Django сам ее вызовет,когда мы перейдем по ссылке.   #noqa
    path(route="generate-article", view=generate_article_idea),
    path(route="market", view=get_current_market_state),
    path(route="exchange-rate", view=get_exchange_rate),
]
