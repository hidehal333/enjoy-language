import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from diary.models import Diary
from comments.models import Comments
from users.models import CustomUser
from .forms import InquiryForm, ProfileChangeForm

logger = logging.getLogger(__name__)

#ホームページ用
class HomePageView(TemplateView):
    template_name = 'home.html'

#Aboutページ用
class AboutPageView(TemplateView):
    template_name = 'about.html'

#お問い合わせページ用
class InquiryPageView(FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('pages:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('inquiry sent by{}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

#Profileページ用
@login_required
def listview(request, pk):
    user = CustomUser.objects.get(pk=pk)
    profile_list = CustomUser.objects.filter(pk=pk)
    diary_list = Diary.objects.filter(user_id=pk).order_by('-created_at')

    #コメントリスト取得
    #上記で取得した日記リストオブジェクトから日記idを取得(diary_id=diary_list[i].id)
    comments_list=[]
    for i in range(len(diary_list)):
        comments_list.append(Comments.objects.filter(diary_id=diary_list[i].id).order_by('created_at'))

    #ページネーション
    page_obj_c = paginate_queryset(request, comments_list, 5)
    comments_list = page_obj_c.object_list

    page_obj = paginate_queryset(request, diary_list, 5)
    diary_list = page_obj.object_list

    #テンプレート用に2つのクエリをセットにする。
    items=[]
    for item in zip(diary_list, comments_list):
        items.append(item)

    dict = {
        'profile_list':profile_list,
        'items': items,
        'object_id': pk
    }
    return render(request, 'profile.html', dict)

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

#Profile編集用ページ
class ProfileChangeView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    template_name = 'profile_change.html'
    form_class = ProfileChangeForm

    def get_success_url(self):
        return reverse_lazy('pages:profile', kwargs={'pk':self.request.user.id})

    def get_object(self):
        return self.request.user

#ユーザー検索（全ユーザー）
class UserSearchAllListView(LoginRequiredMixin,ListView):
    model = CustomUser
    template_name = 'user_search_all.html'
    context_object_name = 'user_search'
    paginate_by = 10

    def get_queryset(self):
        return CustomUser.objects.filter(last_login__isnull=False).exclude(id=self.request.user.id)

#ユーザー検索（リクエストユーザー母語=学習言語）
class UserSearchMLListView(LoginRequiredMixin,ListView):
    model = CustomUser
    template_name = 'user_search_ml.html'
    context_object_name = 'user_search'
    paginate_by = 10

    def get_queryset(self):
        return CustomUser.objects.filter(last_login__isnull=False, learn_language=self.request.user.mother_language).exclude(id=self.request.user.id)


#ユーザー検索（リクエストユーザー学習言語=学習言語）
class UserSearchLLListView(LoginRequiredMixin,ListView):
    model = CustomUser
    template_name = 'user_search_ll.html'
    context_object_name = 'user_search'
    paginate_by = 10

    def get_queryset(self):
        return CustomUser.objects.filter(last_login__isnull=False, learn_language=self.request.user.learn_language).exclude(id=self.request.user.id)