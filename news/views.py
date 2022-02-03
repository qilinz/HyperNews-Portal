from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
import random

from datetime import datetime
import json


# Create your views here.
def index_view(request):
    return redirect("/news/")


class MainView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as json_file:
            news_list = json.load(json_file)

        # test search;
        search = request.GET.get("q")

        news_by_date = {}
        for item in news_list:
            if search and search not in item["title"]:
                continue
            news_date = item["created"].split()[0]
            if news_date in news_by_date:
                news_by_date[news_date].append(item)
            else:
                news_by_date[news_date] = [item]
        news_by_date = dict(sorted(news_by_date.items(), reverse=True))

        context = {"news_by_date": news_by_date}
        return render(request, "news/news.html", context=context)


class DetailsView(View):
    def get(self, request, news_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as json_file:
            news_list = json.load(json_file)

        for news_item in news_list:
            if news_item["link"] == news_id:
                context = {"news_item": news_item}
                return render(request, "news/news_details.html", context=context)


class NewPostView(View):

    def get(self, request, *args, **kwargs):
        print('??')
        return render(request, "news/new_post.html")

    def post(self, request, *args, **kwargs):
        print("Here???????????")
        with open(settings.NEWS_JSON_PATH) as json_file:
            news_list = json.load(json_file)

        news_ids = [item["link"] for item in news_list]

        # get the data
        title = request.POST.get("title")
        text = request.POST.get("text")
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = random.randint(10000, 100000)
        while link in news_ids:
            link = random.randint(10000, 100000)

        # save to json
        new_post = {
            "created": created,
            "text": text,
            "title": title,
            "link": link,
        }

        news_list.append(new_post)
        with open(settings.NEWS_JSON_PATH, "w") as json_file:
            json.dump(news_list, json_file)

        return redirect("/news/")


