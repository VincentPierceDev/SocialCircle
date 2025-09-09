from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Server, Membership

def server_member_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        server_id = kwargs.get('public_id')
        server = get_object_or_404(Server, u_uniqueid=server_id)

        is_in_server = Membership.objects.filter(
            user=request.user,
            server=server
        ).exists()

        if not is_in_server:
            return HttpResponseForbidden("You are not a member of this server.")
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view