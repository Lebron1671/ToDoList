from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from .models import ToDoList, Item
from .forms import CreateNewList
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request, id):
    try:
        ls = ToDoList.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/view")
        #raise Http404("Page not found.")
    if ls in request.user.todolist.all():
        if request.method == "POST":
            print(request.POST)
            if request.POST.get("save"):
                for item in ls.item_set.all():
                    if request.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif request.POST.get("newItem"):
                txt = request.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")
        return render(request, "main/list.html", {"ls": ls})
    return render(request, "main/view.html", {})


def home(request):
    return render(request, 'main/home.html', {})


def create(request):
    if request.method == "POST":
        try:
            form = CreateNewList(request.POST)

            if form.is_valid():
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
                request.user.todolist.add(t)

            return HttpResponseRedirect("/%i" %t.id)
        except AttributeError:
            return render(request, 'main/home.html', {})
    else:
        form = CreateNewList()
    return render(request, 'main/create.html', {"form": form})


def view(request):
    return render(request, "main/view.html", {})


def delete_list(request, id):
    to_do_list = ToDoList.objects.get(id=id)
    to_do_list.delete()
    return HttpResponseRedirect("/create")


def delete_task(request, id):
    task = Item.objects.get(id=id)
    ls = ToDoList.objects.get(id=task.todolist_id)
    task.delete()
    return HttpResponseRedirect("/%i" % ls.id)

