from django import forms

class NewPlayerForm(forms.Form):
    name = forms.CharField(label="Name")
    oppo = forms.CharField(label="Opponent")
    BINGO_word = forms.CharField(label="Your BINGO! word", max_length=5, min_length=5)