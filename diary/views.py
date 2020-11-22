from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

from .forms import DiaryCreateForm
from django.urls import reverse_lazy
from django.views import generic

from diary.models import Diary
from comments.models import Comments
from users.models import CustomUser
from .models import Diary

from itertools import chain

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


#日記リスト（コメント表示）
@login_required
def diary_list(request):
    #日記リスト取得
    diary_list = Diary.objects.all().order_by('-created_at')

    #いいね
    liked_list =[]
    for diary in diary_list:
        liked = False

        if diary.like.filter(id=request.user.id).exists():
            liked=True
        liked_list.append(liked)


    #ページネーション
    #1ページあたりの日記表示数
    per_page = 10

    page_obj = paginate_queryset(request, diary_list, per_page)
    diary_list = page_obj.object_list

    page_obj = paginate_queryset(request, liked_list, per_page)
    liked_list = page_obj.object_list

    #テンプレート用に2つのクエリをセットにする。
    items=[]
    for item in zip(diary_list, liked_list):
        items.append(item)


    return render(request, 'diary_list.html', {'items':items,  'page_obj':page_obj})


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


#日記詳細ページ
@login_required
def diary_detail(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    comments = Comments.objects.filter(diary_id=pk).order_by('created_at')
    print(comments)
    liked = False
    if diary.like.filter(id=request.user.id).exists():
       liked = True
    return render(request, 'diary_detail.html', {'diary': diary, 'comments': comments, 'liked': liked})

#いいね機能
@login_required
def like(request):
    diary = get_object_or_404(Diary, id=request.POST.get('diary_id'))
    liked = False
    if diary.like.filter(id=request.user.id).exists():
       diary.like.remove(request.user)
       liked = False
    else:
       diary.like.add(request.user)
       liked = True
    likes= len(diary.like.all())

    # return redirect('diary:diary_list')
    context={
       'diary_id': diary.id,
       'liked': liked,
       'likes':likes
       }
    print(context)
    # if request.is_ajax():
    html = render_to_string('diary/like.html', context, request=request )
    print(html)
    return JsonResponse({ 'context':context})


#日記作成ページ
class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

#日記編集ページ
class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        item = Diary.objects.get(pk=self.kwargs['pk'])
        if self.request.user == item.user:
            messages.success(self.request, '日記を更新しました。')
            return super().form_valid(form)
        else:
            return redirect('diary:diary_list')

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

#日記削除ページ
class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        item = Diary.objects.get(pk=self.kwargs['pk'])
        if self.request.user == item.user:
            messages.success(self.request, "日記を削除しました。")
            return super().delete(request, *args, **kwargs)
        else:
            return redirect('diary:diary_list')

#ajax日記削除
@login_required
def ajax_post_delete(request):
    print(request)
    print(request.POST)

    if request.method == 'POST':
        try:
            diary = get_object_or_404(Diary, id=request.POST.get('diary_id'))
        except Diary.DoesNotExist:
            raise Http404
        if request.user == diary.user:
            diary.delete()
            d = True
        return HttpResponse(d)


#翻訳する
@login_required
def translate(request):
    diary = get_object_or_404(Diary, id=request.POST.get('diary_id'))
    #diaryから内容を取得
    content= diary.content
    print(content)
    #翻訳用URLを作作成
    if content:
        url = "https://script.google.com/macros/s/AKfycbwU1c-SrdusLY-cjzAKbwnoXB8r2qBwjOwXjqj7c_zS4nIW74s/exec?text=" + content+ "&source=ja&target=en"
        soup = get_soup(url)
        print("url")
        print(url)
        print(soup)

        return HttpResponse(soup)
    else:
        return render(request, 'translate_no_result.html')

#翻訳ページスクレイピング
def get_soup(url):
    try:
        # データ取得
        resp = requests.get(url)
        print(resp)
        resp.encoding = resp.apparent_encoding
        # 要素の抽出
        soup = BeautifulSoup(resp.text, "html.parser")
        print(soup)
        return soup
    except Exception as e:
        return print("スクレイピングできませんでした。")


#ふりがな
@login_required
def furigana(request):
    diary = get_object_or_404(Diary, id=request.POST.get('diary_id'))

    target_url = "https://jlp.yahooapis.jp/FuriganaService/V1/furigana"
    api_key= "dj00aiZpPUZTeHV0c1Y3NUJnTCZzPWNvbnN1bWVyc2VjcmV0Jng9YzY-"

    sentence = diary.content

    data = {
        "appid":api_key,
        "grade":"1",
        "sentence":sentence
    }

    response = requests.post(target_url, data=data)

    root = ET.fromstring(response.text)

    ruby_dict = {}
    text = []
    for line in root:
        for word_list in line[0]:
            if len(word_list) == 1:
                text.append(word_list[0].text)
            else:
                text.append(word_list[0].text)
                ruby_dict[word_list[0].text] = word_list[1].text

    text_content=[]
    for word in text:
        if word in list(ruby_dict.keys()):
            text_content.append("<ruby>{}<rp>".format(word))
            text_content.append("（</rp><rt>{}</rt><rp>）</rp></ruby>".format(ruby_dict[word]))
        else:
            text_content.append(word)
    return HttpResponse(text_content)


#ajax日記投稿
def ajax_post_add(request):
    if request.method == 'POST':

        #画像ファイルのリストを取得(MultiValueDictから)
        image_list=request.FILES.getlist('image')
        #画像数
        k = len(image_list)
        #画像を取得
        if k == 1:
            posted_img1=image_list[0]
            posted_img2 = None
            posted_img3 = None
        elif k ==2:
            posted_img1=image_list[0]
            posted_img2=image_list[1]
            posted_img3 = None
        elif k == 3:
            posted_img1=image_list[0]
            posted_img2=image_list[1]
            posted_img3 =image_list[2]
        else:
            posted_img1 = None
            posted_img2 = None
            posted_img3 = None

        #日記本文を取得
        content = request.POST['content']

        diary = Diary.objects.create(content=content, photo1=posted_img1, photo2=posted_img2, photo3=posted_img3, user=request.user)
        #画像URLを取得
        if diary.photo1:
            photo1=diary.photo1.url
        else:
            photo1=None
        if diary.photo2:
            photo2=diary.photo2.url
        else:
            photo2=None
        if diary.photo3:
            photo3=diary.photo3.url
        else:
            photo3=None

    d = {
        "user_id":diary.user.id,
        "nickname": diary.user.nickname,
        "photo_url":diary.user.profile_photo.url,
        "mother_language": diary.user.mother_language,
        "learn_language": diary.user.learn_language,
        "diary_id":diary.id,
        "content":diary.content,
        "created_at": diary.created_at,
        "photo1": photo1,
        "photo2": photo2,
        "photo3": photo3,
    }

    return JsonResponse(d)
