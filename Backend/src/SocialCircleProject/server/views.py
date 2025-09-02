from django.shortcuts import render
from .forms import CreateServerForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def create_server_view(request):

    temp_username = "User"

    try:
        username = request.user.username
        user_initial = username[0]
    except:
        username = temp_username
        user_initial = "U"        

    if username != temp_username and request.method == "POST":
        form = CreateServerForm(request.POST)
        if form.is_valid():
            form.save(username)
            return redirect('/user/dashboard')
    elif username == temp_username and request.method == "POST":
        return redirect('/user/dashboard')
    else:
        form = CreateServerForm()

    context = {
        "username": username,
        "user_initial": user_initial,
        "form": form
    }

    return render(request, 'server/create-server.html', context)