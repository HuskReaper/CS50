import markdown2, random
from django.shortcuts import render
from . import util

md = markdown2.Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def get(title):
    entry = util.get_entry(title)
    if entry != None: return md.convert(entry)
    else: return None
    
def entry(request, title):
    web_content = get(title)
    if web_content == None: return render(request, "encyclopedia/error.html", {"message": "Entry was not found."})
    else:
        return render(request, "encyclopedia/view_entry.html", {
            "title": title,
            "content": web_content
        })
        
def search_entry(request):
    if request.method == "POST":
        web_content = get(request.POST['q'])
        if web_content != None: return render(request, "encyclopedia/view_entry.html", {
            "title": request.POST['q'],
            "content": web_content
        })
        else:
            entries = util.list_entries()
            auto_fill = []
            for entry in entries:
                if request.POST['q'].lower() in entry.lower(): auto_fill.append(entry)
            return render(request, "encyclopedia/search_results.html", {"contents": auto_fill})  
        
def new_entry(request):
    if request.method == "GET": return render(request, "encyclopedia/new_entry.html")
    else:
        title = request.POST['entry_title']
        contents = request.POST['entry_contents']
        
        if util.get_entry(title) != None: return render(request, "encyclopedia/error.html", {"message": "Entry already exists."})
        else:
            util.save_entry(title, contents)
            web_content = get(title)
            return render(request, "encyclopedia/view_entry.html", {
                "title": title,
                "content": web_content
            })
            
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        web_content = get(title)
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "content": web_content
        })
        
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        web_content = get(title)
        return render(request, "encyclopedia/view_entry.html", {
            "title": title,
            "content": web_content
        })
        
def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    web_content = get(title)
    return render(request, "encyclopedia/view_entry.html", {
        "title": title,
        "content": web_content
    })