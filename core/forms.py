from django import forms

from .models import Comment


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    subject = forms.CharField(
        label="Тема",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "content"]
        widgets = {
            "author_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Ваш комментарий",
                }
            ),
        }
