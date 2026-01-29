from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import Account

@login_required
def list_view(request):
    accounts = Account.objects.filter(
        created_by=request.user,
        is_deleted=False
    ).order_by("account_type", "name")

    return render(
        request,
        "accounts/list.html",
        {"accounts": accounts}
    )

@login_required
def create_view(request):
    if request.method == "POST":
        Account.objects.create(
            name=request.POST.get("name"),
            account_type=request.POST.get("account_type"),
            opening_balance=request.POST.get("opening_balance") or 0,
            opening_date=request.POST.get("opening_date"),
            is_active=bool(request.POST.get("is_active")),
            created_by=request.user,
        )

        messages.success(request, "Account created successfully")
        return redirect("accounts")

    return render(
        request,
        "accounts/create.html",
        {
            "account_type_choices": Account.ACCOUNT_TYPES
        }
    )



@login_required
def edit_view(request, pk):
    account = get_object_or_404(
        Account,
        pk=pk,
        created_by=request.user,
        is_deleted=False
    )

    if request.method == "POST":
        account.name = request.POST.get("name")
        account.opening_balance = request.POST.get("opening_balance") or 0
        account.opening_date = request.POST.get("opening_date")
        account.is_active = bool(request.POST.get("is_active"))
        account.save()

        messages.success(request, "Account updated successfully")
        return redirect("accounts")

    return render(
        request,
        "accounts/edit.html",
        {
            "account": account,
            "account_type_choices": Account.ACCOUNT_TYPES
        }
    )

