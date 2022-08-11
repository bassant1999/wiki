from django.shortcuts import render
from django.shortcuts import redirect
from markdown2 import Markdown
import markdown2
import random

markdowner = Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry
def get_entry(request, title):
    if request.method == "POST":
        # get q
        search = request.POST["q"]
        entry = util.get_entry(search)
        if(entry is None):
            matching = [s for s in util.list_entries() if search.lower() in s.lower()]
            return render(request, "encyclopedia/results.html", {"matching":matching})
        return redirect("../../wiki/"+search)
        # # or return redirect("http://127.0.0.1:8000/wiki/"+search)
    entry = util.get_entry(title)
    page = entry
    if(entry is None):
        return render(request, "encyclopedia/error.html", {})
    entry = markdowner.convert(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, "title":title, "page":page
    })

# create new entry
def create(request):
    if request.method == "POST":
        # get title, and content
        title = request.POST["title"]
        content = request.POST["content"]
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {
                "error": "This Title Is Already Exist"})
        util.save_entry(title, content)
        return redirect("wiki/"+title)
    return render(request, "encyclopedia/create.html", {})

#edit an existing entry
def edit(request, title):
    if request.method == "POST":
        # get the content
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("../wiki/"+title)
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "entry": entry, "title":title
    })

#get a random page
def random(request):
    elist = util.list_entries()
    import secrets
    title = secrets.choice(elist)
    return redirect("wiki/"+title)


