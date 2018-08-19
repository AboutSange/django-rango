import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views":100},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 99},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 98}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": 97},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": 96},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": 95}]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/",
         "views": 94},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": 93}]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}}

    # 如果想添加更多分类或网页，添加到前面的字典中即可

    # 下述代码迭代 cats 字典，添加各分类，并把相关的网页添加到分类中
    # 如果使用的是 Python 2.x，要使用 cats.iteritems() 迭代
    # 迭代字典的正确方式参见
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/

    for cat, cat_data in cats.items():
        views = cat_data["views"]
        likes = cat_data["likes"]

        c = add_cat(cat, views, likes)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # 打印添加的分类
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]  # (object, created)
    c.views = views
    c.likes = likes
    c.save()
    return c


# 从这开始执行
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()