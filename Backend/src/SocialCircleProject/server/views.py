from django.shortcuts import render, get_object_or_404
from .forms import CreateServerForm, SearchServerForm
from .models import Server, Membership
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .decorators import server_member_required
from django.http import HttpResponse
import uuid


@login_required
def create_server_view(request):

    username, user_initial, temp_username = collect_user_info(request)

    if username != temp_username and request.method == "POST":
        form = CreateServerForm(request.POST)
        if form.is_valid():
            form.save(username)
            return redirect('dashboard')
    elif username == temp_username and request.method == "POST":
        return redirect('dashboard')
    else:
        form = CreateServerForm()

    context = {
        "username": username,
        "user_initial": user_initial,
        "form": form
    }

    return render(request, 'server/create-server.html', context)

@login_required
def join_server_view(request):
    username, user_initial, temp_username = collect_user_info(request)
    search_results = []
    search_form = SearchServerForm(request.GET or None)
    no_search = True

    if username == temp_username:
        return redirect('dashboard')
    
    if request.method == "GET" and search_form.is_valid():
        server_query = search_form.cleaned_data.get('name')
        owner_query = search_form.cleaned_data.get('owner')
        no_search = False
        #get the servers based on search params and remove servers the current user is already in
        if server_query and owner_query == "":
            search_results = Server.objects.filter(name__icontains=server_query).exclude(membership__user__username=username)
        elif server_query and owner_query:
            search_results = Server.objects.filter(membership__user__username__icontains=owner_query, membership__status=Membership.ROLE_MAP["Owner"], name__icontains=server_query).exclude(membership__user__username=username)
    elif request.method == "POST":
        server_id = request.POST.get("server_id")
        joined_server = Server.objects.get(id=server_id)
        if(joined_server):
            joined_server.add_member(user=request.user)
        return redirect('dashboard')
            

    context = {
        "username": username,
        "user_initial": user_initial,
        "form": search_form,
        "results": search_results,
        "no_search": no_search
    }

    return render(request, 'server/join-server.html', context)

@server_member_required
@login_required
def server_home_view(request, public_id):
    print(public_id)
    try:
        uid = uuid.UUID(hex=public_id)
    except ValueError:
        print("Invalid ID")
    server_info = get_object_or_404(Server, u_uniqueid=uid)
    context = {
        'title': server_info.name
    }
    return render(request, 'server/server-home.html', context)


def collect_user_info(request):
    temp_username = "User"
    try:
        username = request.user.username
        user_initial = username[0]
    except:
        username = temp_username
        user_initial = "U"
    return username, user_initial, temp_username