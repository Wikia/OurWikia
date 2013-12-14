from django import forms


class CommentForm(forms.Form):
    message = forms.TextInput