from django.shortcuts import render, redirect
from .models import Keyword, Trend
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from .forms import KeywordForm, TrendForm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Create your views here.
def keyword(request):
    keywords = Keyword.objects.all()
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.save()
            return redirect('trends:keyword')
    else:
        form = KeywordForm()
    context = {
        'form' : form,
        'keywords' : keywords
    }
    return render(request, 'trends/keyword.html', context)

def keyword_detail(request, pk):
    keyword = Keyword.objects.get(pk=pk)
    keyword.delete()
    return redirect('trends:keyword')

def crawling(request):
    # 저장했던 keyword를 불러온다
    keywords = Keyword.objects.all()
    # 크롤링
    for k in keywords:
        url = f'https://www.google.com/search?q={k.name}'
        driver = webdriver.Chrome()
        driver.get(url)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        result_stats = soup.select_one("#result-stats")
        context = {
            'result' : result_stats.text,
        }
        # print(result_stats.text)
        t = result_stats.text
        t = t.replace(',','').strip()
        s = ''
        for i in range(len(t)):
            if t[i].isdigit()==True:
                s += t[i]
            elif t[i] == '개':
                break
        s = int(s)
        print(k.name)
        if Trend.objects.filter(name=k.name, search_period="all").exists():
            trend = Trend.objects.get(name=k.name, search_period="all")
            trend.result = s
            trend.save()
        else: 
            Trend.objects.create(name=k.name, result=s, search_period="all")
    return render(request, 'trends/crawling.html', context)

def crawling_histogram(request):
    # 크롤링 수행 후 수행 결과 막대 그래프 생성

    trends = Trend.objects.all()
    x = []
    y = []
    for trend in trends:
        x.append(trend.name)
        y.append(trend.result)

    plt.bar(x, y)
    plt.title('Technology Trend Analysis')
    plt.xlabel('Keyword')
    plt.ylabel('Result')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    context = {
        'image' : f'data:image/png;base64, {img_base64}',
    }
    return render(request, 'trends/crawling_histogram.html', context)

def crawling_advanced(request):
    # 지난 1년 기준으로 크롤링 수행 후 막대 그래프 생성
    return render(request, 'trends/crawling_advanced.html')