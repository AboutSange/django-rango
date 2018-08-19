from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm


"""
def index(request):
    # return HttpResponse("Rango says hey there parter! <br/> <a href=\"/rango/about/\">About</a>")

    # 构建一个字典，作为上下文传给模板引擎
    # 注意， boldmessage 键对应于模板中的 {{ boldmessage }}
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # 返回一个渲染后的响应发给客户端
    # 为了方便，我们使用的是 render 函数的简短形式
    # 注意，第二个参数是我们想使用的模板
    return render(request, 'rango/index.html', context=context_dict)
"""

def index(request):
    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前 5 个分类（如果分类数少于 5 个，那就获取全部）
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages':page_list}

    # 渲染响应，发给客户端
    return render(request, 'rango/index.html', context_dict)


def about(request):
    # return HttpResponse("Rango says here is the about page. <br/> <a href=\"/rango/\">Index</a>")

    context_dict = {'boldmessage': "About Sange"}

    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}

    try:
        # 能通过传入的分类别名找到对应的分类吗？
        # 如果找不到， .get() 方法抛出 DoesNotExist 异常
        # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)

        # 检索关联的所有网页
        # 注意， filter() 返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)

        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages

        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category

    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None

    # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    # 是HTTP POST请求吗？
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # 表单数据有效吗？
        if form.is_valid():
            # 把新分类存入数据库
            cat = form.save(commit=True)
            print(cat, cat.slug)
            # 保存新分类后可以显示一个确认消息
            # 不过既然最受欢迎的分类在首页
            # 那就把用户带到首页吧
            return index(request)
        else:
            # 表单数据有错误
            # 直接在终端里打印出来
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})