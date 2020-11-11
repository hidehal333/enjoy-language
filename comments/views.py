from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from .forms import CommentsCreateForm
from .models import Comments

from diary.models import Diary
from users.models import CustomUser


#コメント作成ページ
class CommentsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comments
    template_name = 'comments_create.html'
    form_class = CommentsCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Diary, pk=post_pk)
        comments = form.save(commit=False)
        comments.diary = post
        comments.user = self.request.user
        comments.save()
        messages.success(self.request, 'コメントを作成しました。')
        return redirect('diary:diary_list')

    def form_invalid(self, form):
        messages.error(self.request, "コメントの作成に失敗しました。")
        return super().form_invalid(form)


#コメント削除ページ
class CommentsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comments
    template_name = 'comments_delete.html'

    def get_success_url(self):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comments, pk=comment_pk)
        post_pk = comment.diary.pk
        return reverse_lazy('diary:diary_list')


    def delete(self, request, *args, **kwargs):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comments, pk=comment_pk)
        post_pk = comment.diary.pk
        item = Comments.objects.get(pk=self.kwargs['pk'])
        if self.request.user == item.user:
            messages.success(self.request, "コメントを削除しました。")
            return super().delete(request, *args, **kwargs)
        else:
            return redirect('diary:diary_list')
