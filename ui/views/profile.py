from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, "profile/view.html")


@login_required
def profile_edit(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")

        password = request.POST.get("password")
        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile")

    return render(request, "profile/edit.html")
