from django.shortcuts import render
from django import forms
import markdown2
import random

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="")
    
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content (in Markdown)", widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))

class EditEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content (in Markdown)", widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })
    
def entry(request, entry):
    entry_content = util.get_entry(entry)
    if entry_content is None:
        get_entry = "not_found"
    else:
        get_entry = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/wiki/entry.html", {
        "entryTitle": entry,
        "entry": get_entry,
        "form": SearchForm()
    })


def search(request):
    
    if request.method == "POST":
        form = SearchForm(request.POST)
        searchList = []
        if form.is_valid():
            search = form.cleaned_data["search"]
            if search in util.list_entries():
                return render(request, "encyclopedia/wiki/entry.html", {
                    "entry": markdown2.markdown(util.get_entry(search)), "form": SearchForm()
    })
            else: 
                for entry in util.list_entries():
                    if search.lower() in entry.lower():
                        searchList.append(entry)
                if searchList:
                    return render(request, "encyclopedia/search.html", {
                            "entries": searchList, "form": SearchForm()
                        })
                    
                else:
                        return render(request, "encyclopedia/search.html", {
                        "entries": [], "form": SearchForm()
                    })
    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries(), "form": SearchForm()
    })
    
def new(request):
    if request.method == "POST":
        newEntryForm = NewEntryForm(request.POST)
        if newEntryForm.is_valid():
            title = newEntryForm.cleaned_data["title"]
            content = newEntryForm.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/new.html", {
                    "entries": util.list_entries(), "form": SearchForm(),
                    "newEntryForm": NewEntryForm(), "error": "Entry already exists."
                })
            else:   
                util.save_entry(title, content)
                return render(request, "encyclopedia/wiki/entry.html", {
                    "entry": markdown2.markdown(util.get_entry(title)), "form": SearchForm()
                })
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries(), "form": SearchForm(),
        "newEntryForm": NewEntryForm()
    })
    
def edit(request, entry):
    if request.method == "POST":
        newEntryForm = NewEntryForm(request.POST)
        if newEntryForm.is_valid():
            title = newEntryForm.cleaned_data["title"]
            content = newEntryForm.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/wiki/entry.html", {
                "entry": markdown2.markdown(util.get_entry(title)), "form": SearchForm()
            })
    return render(request, "encyclopedia/edit/entry.html", {
        "entry": entry, "form": SearchForm(),
        "editEntryForm": EditEntryForm(initial={'title': entry, 'content': util.get_entry(entry)})
    })
    
def delete(request, entry):
    util.delete_entry(entry)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": SearchForm()
    })
    
def randomEntry(request):
    entry = random.choice(util.list_entries())
    return render(request, "encyclopedia/wiki/entry.html", {
        "entryTitle": entry, "entry": markdown2.markdown(util.get_entry(entry)), "form": SearchForm()
    })