"""server_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from register_login import api_register_manage
from register_login import urls as register_urls
from django.conf import settings

# 正常的 url 在添加到这个 list 里
url_list = [
    register_urls.urlpatterns
]
urlpatterns = []
for url in url_list:
    urlpatterns = urlpatterns + url

# 测试环境下才可用的url，放在这个 list 里
test_url_list = [
    register_urls.urlpatterns_test
]

if settings.DEBUG is True:
    for test_url in test_url_list:
        urlpatterns = urlpatterns + test_url
