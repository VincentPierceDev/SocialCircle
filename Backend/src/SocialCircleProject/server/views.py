from django.shortcuts import render


def create_server_view(request):
    try:
        username = request.user.username
        user_initial = username[0]
    except:
        username = "User"
        user_initial = "U"

    context = {
        "username": username,
        "user_initial": user_initial
    }

    return render(request, 'server/create-server.html', context)