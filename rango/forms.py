from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # 嵌套的类，为表单提供额外信息
    class Meta:
        # 把这个ModelForm与一个模型连接起来
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # 把这个 ModelForm 与一个模型连接起来
        model = Page

        # 想在表单中放哪些字段？
        # 有时不需要全部字段
        # 有些字段接受空值，因此可能无需显示
        # 这里我们想隐藏外键字段
        # 为此，可以排除 category 字段
        exclude = ('category',)
        # 也可以直接指定想显示的字段（不含 category 字段）
        # fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # 如果 url 字段不为空，而且不以“http://”开头
        # 在前面加上“http://”
        if url and not url.startswith('http://'):
            url = 'http://' + url
        cleaned_data['url'] = url
        return cleaned_data