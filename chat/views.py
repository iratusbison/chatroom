from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View

def chatPage(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login-user")
	context = {}
	return render(request, "chat/chatPage.html", context)

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Perform logout action
        logout(request)
        # Redirect to a desired page after logout
        return HttpResponseRedirect('/')  # Redirect to a specific URL after logout
