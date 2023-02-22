from django.shortcuts import render
from django.http import HttpResponse
# importing the modules
import requests
from bs4 import BeautifulSoup
import csv


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search_it = request.POST.get('search')
    url = search_it
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    title = "title"
    description = "description"
    keywords = "keywords"

    for title in soup.find_all('title'):
        title = title.get_text()

    for meta in soup.find_all('meta'):
        if('name' in meta.attrs and meta.attrs['name'] == 'description'):
            description = meta.attrs['content']
        elif('name' in meta.attrs and meta.attrs['name'] == 'keywords'):
            keywords = meta.attrs['content']

    search_item = {
        'search': search_it,
        'title' : title,
        'desc' : description,
        'keywords' : keywords
    }

    

    return render(request, 'tools/new_search.html', search_item)





# Web Search 


def web_search(request):
    search_it = request.POST.get('search')
    url = "https://www.venuemonk.com"


    try:
        reqs = requests.get(url)
    except:
        print("Not Found")
    
    soup = BeautifulSoup(reqs.text, 'html.parser')

    data = {'title': [], 'desc' : [], 'keyword' : []}

    links = []
    for link in soup.findAll('a'):
            # webLink = (f"{url}{link.get('href')}")
        links.append(f"{url}{link.get('href')}")
            # print(f"{url}{link.get('href')}")

    urls = "Urls"

    for i in links:
            try:
                reqs2 = requests.get(i, timeout=2)
            except: 
                print("Url Not Found")

            # using the BeautifulSoup module
            soup2 = BeautifulSoup(reqs2.text, 'html.parser')

            print(f"Url :- {i}")
            for title in soup2.find_all('title'):
                # print("Title :- ", title.get_text())
                data["title"].append(title.get_text())

            for meta in soup2.find_all('meta'):
                if('name' in meta.attrs and meta.attrs['name'] == 'description'):
                    # print("Description :- ", meta.attrs['content'])
                    data["desc"].append(meta.attrs['content'])


                if('name' in meta.attrs and meta.attrs['name'] == 'keywords'):
                    # print("Keywords :- ", meta.attrs['content'] +"\n")
                    data["keyword"].append(meta.attrs['content'])


    print("Loop End")
    print(data['title'])
                                                                                                                                                                   
    with open('static/output/output.csv', 'w') as output:
        writer = csv.writer(output)
        for key, value in data.items():
            writer.writerow([key, value]) 

    return render(request, 'tools/web_search.html', data)


