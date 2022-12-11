from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import NewPlayerForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        _NewPlayerForm = NewPlayerForm(request.POST)
        if _NewPlayerForm.is_valid():
            me = _NewPlayerForm.cleaned_data['name']
            oppo = _NewPlayerForm.cleaned_data['oppo']
            BINGO_word = _NewPlayerForm.cleaned_data['BINGO_word']

            return HttpResponseRedirect(reverse('game:start', args=(me, oppo)))

    return render(request, 'prelogin/index.html', context={
        "form": NewPlayerForm()
    })