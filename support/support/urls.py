import httpx
import random
import string
from typing import Callable
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpRequest, JsonResponse

create_random_string: Callable[[int], str] = lambda size: "".join(  # noqa
    [random.choice(string.ascii_letters) for i in range(size)]  # noqa
)  # noqa

# content = """
# <!DOCTYPE html>
# <html lang="en">
#     <head>
#         <meta charset="UTF-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#         <title>Information fetching</title>
#         <link 
#             href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" 
#             rel="stylesheet" 
#             integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" 
#             crossorigin="anonymous"
#         />
#         <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
#     </head>
#     <body>
#         <h1>Information fetcher</h1> 
#         <button id="generate" class="btn btn-primary">Fetch information</button>
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
#                         alert("An error was accured during generating the article idea");
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
#                         alert("An error was accured during generating the article idea");
#                     },
#                 });
#                 });
#             });    
#         </script>        
#     </body>
# </html>    
# """

# def generate_article_idea(request: HttpRequest) -> HttpResponse:  # отображает на веб-странице выше описанный html и JS код.
#     return HttpResponse(content)

# def generate_article_idea(request: HttpRequest) -> HttpResponse:  #
#     content = "<h1>Hello World</h1>"
#     return HttpResponse(content)   # отдает на странице результат в виде text/html

def generate_article_idea(request: HttpRequest) -> JsonResponse:
    content = {
        "title": create_random_string(size=10),
        "description": create_random_string(size=20),
    }
    return JsonResponse(content)    # отдает на странице результат в виде application/json


async def get_current_market_state(request: HttpRequest):
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=XSN17SDSA5RAM5W2"
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
    rate: str = response.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    return JsonResponse({"rate": rate})


urlpatterns = [
    #path("admin/", admin.site.urls),
    # передается не функция, а ее объект. Django сам ее вызовет,когда мы перейдем по ссылке.
    path(route="generate-article", view=generate_article_idea),  
    path(route="market", view=get_current_market_state)
]



