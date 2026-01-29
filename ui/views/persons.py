from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from transactions.models import Person

@login_required
def create_view(request):
    if request.method == "POST":
        Person.objects.create(
            name=request.POST.get("name"),
            relation=request.POST.get("relation"),
            created_by=request.user,
        )
        messages.success(request, "Person added")
        return redirect("persons")

    return render(request, "persons/create.html")


@login_required
def list_view(request):
    persons = Person.objects.filter(
        created_by=request.user,
        is_deleted=False
    ).order_by("name")

    return render(
        request,
        "persons/list.html",
        {"persons": persons}
    )


@login_required
def edit_view(request, pk):
    person = get_object_or_404(
        Person,
        pk=pk,
        created_by=request.user,
        is_deleted=False
    )

    if request.method == "POST":
        person.name = request.POST.get("name")
        person.relation = request.POST.get("relation")
        person.save()

        messages.success(request, "Person updated successfully")
        return redirect("persons")

    return render(
        request,
        "persons/edit.html",
        {"person": person}
    )
