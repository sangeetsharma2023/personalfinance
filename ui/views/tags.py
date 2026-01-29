from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from transactions.models import Tag

@login_required
def list_view(request):
    tags = Tag.objects.filter(
        created_by=request.user,
        
    ).order_by("name")

    return render(request, "tags/list.html", {"tags": tags})

@login_required
def create_view(request):
    if request.method == "POST":
        Tag.objects.create(
            name=request.POST.get("name"),
            created_by=request.user,
        )
        messages.success(request, "Tag created")
        return redirect("tags")

    return render(request, "tags/create.html")

@login_required
def edit_view(request, pk):
    tag = get_object_or_404(
        Tag, pk=pk, created_by=request.user,
    )

    if request.method == "POST":
        tag.name = request.POST.get("name")
        tag.save()
        messages.success(request, "Tag updated")
        return redirect("tags")

    return render(request, "tags/edit.html", {"tag": tag})
