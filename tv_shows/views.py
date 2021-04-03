from django.shortcuts import render, redirect
from .models import Show, Network
from django.contrib import messages

def check_network(netwk):
    nt = Network.objects.filter(name=netwk)
    if len(nt) == 0:
        Network.objects.create(name=netwk)
    all_nt = Network.objects.all()
    for network in all_nt:
        if network.name == netwk:
            return network

def index(request):
    return redirect('/shows')

def shows(request):
    context = {
        'shows':Show.objects.all()
    }
    return render(request, 'shows.html', context)

def new(request):
    
    return render(request, 'new.html')

def create(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Show.objects.basic_validator(request.POST)
    ttl = Show.objects.filter(title=request.POST['title'])
    if len(ttl) != 0:
        errors["title2"] = "Show title already exists"
        # check if the errors dictionary has anything in it    
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        context = {
            'title': request.POST['title'],
            'network': request.POST['network'],
            'release': request.POST['release'],
            'description': request.POST['description'],
            'errors': errors
        }
        return render(request, 'new.html', context)
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the show to be created, make the changes, and save        
        show_title = request.POST['title']
        show_network = request.POST['network']
        show_release = request.POST['release']
        show_description = request.POST['description']
        s_network = check_network(show_network)
        # print(s_network)
        Show.objects.create(title=show_title, description=show_description, release_date=show_release, network=s_network)
        return redirect('/shows')

# =====================FROM SOLUTION 1 for create=========================================
    # errors = Show.objects.validate(request.POST)
    # if errors:
    #     for (key, value) in errors.items():
    #         messages.error(request, value)
    #     return redirect('/shows/new')

    # Show.objects.create(
    #     title = request.POST['title'],
    #     network = request.POST['network'],
    #     release_date = request.POST['release_date'],
    #     description = request.POST['description']
    # )
# ===============================================================================


def info(request, uid):
    context = {
        'show': Show.objects.get(id=uid)
    }
    return render(request, 'show.html', context)

def edit(request, uid):
    context = {
        'show': Show.objects.get(id=uid)
    }
    return render(request, 'edit.html', context)

def update(request, uid):
    if request.method == 'GET':
        return redirect('/')
    errors = Show.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it    
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/'+str(uid)+'/edit')
    else:
        update_show = Show.objects.get(id=uid)
        update_show.title = request.POST['title']    
        update_show.release_date = request.POST['release']
        update_show.description = request.POST['description']
        show_network = request.POST['network']
        update_show.network = check_network(show_network)
        update_show.save()
        return redirect('/shows')

def destroy(request, uid):
    delete_show = Show.objects.get(id=uid)
    delete_show.delete()
    return redirect('/shows')