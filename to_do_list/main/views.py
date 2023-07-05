from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from .models import ToDoList
from .forms import CreateNewList
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(response, id):
    try:
        ls = ToDoList.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/view")
        #raise Http404("Page not found.")
    if ls in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")
        return render(response, "main/list.html", {"ls": ls})
    return render(response, "main/view.html", {})


def home(response):
    return render(response, 'main/home.html', {})


def create(response):
    if response.method == "POST":
        try:
            form = CreateNewList(response.POST)

            if form.is_valid():
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
                response.user.todolist.add(t)

            return HttpResponseRedirect("/%i" %t.id)
        except AttributeError:
            return render(response, 'main/home.html', {})
    else:
        form = CreateNewList()
    return render(response, 'main/create.html', {"form": form})


def view(response):
    return render(response, "main/view.html", {})

