from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, RainTable, RainDay
from .forms import CreateNewList
import datetime
# Create your views here.


def index(response, id):
    if response.user.is_authenticated:
        ls = ToDoList.objects.get(id=id)
        if ls in response.user.todolist.all():
            if response.method == "POST":
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
                        print("Item name has to be longer than 2 characters")
                elif response.POST.get("remove_completed"):
                    for item in ls.item_set.all():
                        if item.complete == True:
                            item.delete()
                        
            return render(response, "main/list.html", {"ls":ls})
        return render(response, "main/home.html", {})
    return HttpResponseRedirect("/login")

def home(response):
    user_name = "Not logged in"
    user_id = -1
    logout_txt = ""
    if response.user.is_authenticated:
        user_name = response.user.username
        user_id = response.user.id
        logout_txt = "Logout"
        return render(response, "main/home.html", {"user_id":user_id, "user_name":user_name, "logout_txt":logout_txt})
    return HttpResponseRedirect("/login")

def create(response):
    if response.user.is_authenticated:
        if response.method == "POST":
            form = CreateNewList(response.POST)

            if form.is_valid():
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
                response.user.todolist.add(t) 
                return HttpResponseRedirect("/%i" %t.id)
            

        else:
            form = CreateNewList()

        return render(response, "main/create.html", {"form":form})
    return HttpResponseRedirect("/login")

def view(response):
    if response.user.is_authenticated:
        allrt = RainTable.objects.all()
        districtList = []
        for rt in allrt:
            if rt.district not in districtList:
                districtList.append(rt.district)
            
        return render(response, "main/view.html", {"allrt":allrt, "districtList":districtList})
    return HttpResponseRedirect("/login")

def show(response, district, county):
    if response.user.is_authenticated:
        #allrt = RainTable.objects.all()
        rt = RainTable.objects.get(county=county)
        return render(response, "main/show.html", {
                                                    "rt":rt,
                                                    "district":district,
                                                    "county":county,
                                                    })
    return HttpResponseRedirect("/login")