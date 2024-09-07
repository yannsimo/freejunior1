from django import forms

from Blog.models import Comment


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'text', ]
