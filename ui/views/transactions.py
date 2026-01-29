from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datetime import date

from django.db import transaction as db_tx
from transactions.models import Transaction, TransactionItem, Tag, Person, ExpenseItem

from accounts.models import Account
from categories.models import Category

@login_required
def list_view(request):
    qs = Transaction.objects.filter(
        created_by=request.user,
        is_deleted=False,
    ).order_by("-date", "-id")

    status = request.GET.get("status")
    if status == "draft":
        qs = qs.filter(is_draft=True)
    elif status == "posted":
        qs = qs.filter(is_draft=False)

    return render(
        request,
        "transactions/list.html",
        {
            "transactions": qs[:200],
            "status": status,
        }
    )


@login_required
def create_view(request, tx=None):
    # ----------------------------
    # MASTER DATA
    # ----------------------------
    accounts = Account.objects.filter(
        created_by=request.user,
        is_deleted=False,
        is_active=True
    )

    expense_categories = Category.objects.filter(
        created_by=request.user,
        category_type="EXPENSE",
        is_deleted=False,
        is_active=True
    )

    income_categories = Category.objects.filter(
        created_by=request.user,
        category_type="INCOME",
        is_deleted=False,
        is_active=True
    )

    tags = Tag.objects.filter(created_by=request.user, is_deleted=False)
    persons = Person.objects.filter(created_by=request.user, is_deleted=False)

    # ----------------------------
    # POST
    # ----------------------------
    if request.method == "POST":

        tx_type = request.POST.get("tx_type")

        # 1️⃣ CREATE TRANSACTION (DRAFT FIRST)
        if tx is None:
            tx = Transaction(
                transaction_type=request.POST.get("tx_type"),
                date=request.POST.get("date") or date.today(),
                narration=request.POST.get("narration", "").strip(),
                is_draft=True,
                created_by=request.user,
            )
            tx.save()
        else:
            tx.transaction_type = request.POST.get("tx_type")
            tx.date = request.POST.get("date")
            tx.narration = request.POST.get("narration", "").strip()
            tx.updated_by = request.user
            tx.save()


        TransactionItem.objects.filter(transaction=tx).delete()
        ExpenseItem.objects.filter(transaction_item__transaction=tx).delete()

        try:
            with db_tx.atomic():

                # ============================
                # EXPENSE
                # ============================
                if tx_type == "EXPENSE":

                    account_id = request.POST.get("account")

                    # split inputs
                    item_amounts = request.POST.getlist("item_amount[]")
                    item_categories = request.POST.getlist("item_category[]")

                    # single inputs
                    amount = request.POST.get("amount")
                    category_id = request.POST.get("category")

                    tag_ids = request.POST.getlist("tags")
                    person_id = request.POST.get("person") or None

                    # detect real split
                    has_split = any(a for a in item_amounts if a.strip())

                    expense_rows = []

                    if has_split:
                        for amt, cat in zip(item_amounts, item_categories):
                            if amt and cat:
                                expense_rows.append((amt, cat))
                    else:
                        if amount and category_id:
                            expense_rows.append((amount, category_id))

                    if not expense_rows or not account_id:
                        raise ValueError("Incomplete expense")

                    account = Account.objects.get(id=account_id)

                    total_amount = sum(float(a) for a, _ in expense_rows)

                    # ONE ledger entry
                    tx_item = TransactionItem(
                        transaction=tx,
                        account=account,
                        amount=total_amount,
                        is_debit=True,
                    )
                    tx_item.created_by = request.user
                    tx_item.save()

                    # Expense analytics
                    for amt, cat_id in expense_rows:
                        category = Category.objects.get(id=cat_id)

                        ei = ExpenseItem(
                            transaction_item=tx_item,
                            category=category,
                            description=tx.narration or "Expense",
                            amount=amt,
                            person_id=person_id,
                        )
                        ei.created_by = request.user
                        ei.save()

                        if tag_ids:
                            ei.tags.set(tag_ids)

                # ============================
                # INCOME
                # ============================
                elif tx_type == "INCOME":

                    account_id = request.POST.get("account")
                    amount = request.POST.get("amount")

                    if not account_id or not amount:
                        raise ValueError("Incomplete income")

                    account = Account.objects.get(id=account_id)

                    tx_item = TransactionItem(
                        transaction=tx,
                        account=account,
                        amount=amount,
                        is_debit=False,  # CREDIT
                    )
                    tx_item.created_by = request.user
                    tx_item.save()

                # ============================
                # TRANSFER
                # ============================
                elif tx_type == "TRANSFER":

                    from_account_id = request.POST.get("from_account")
                    to_account_id = request.POST.get("to_account")
                    amount = request.POST.get("amount")

                    if not from_account_id or not to_account_id or not amount:
                        raise ValueError("Incomplete transfer")

                    from_account = Account.objects.get(id=from_account_id)
                    to_account = Account.objects.get(id=to_account_id)

                    # DR from source
                    dr_item = TransactionItem(
                        transaction=tx,
                        account=from_account,
                        amount=amount,
                        is_debit=True,
                    )
                    dr_item.created_by = request.user
                    dr_item.save()

                    # CR to destination
                    cr_item = TransactionItem(
                        transaction=tx,
                        account=to_account,
                        amount=amount,
                        is_debit=False,
                    )
                    cr_item.created_by = request.user
                    cr_item.save()

                else:
                    raise ValueError("Unknown transaction type")

                # FINALIZE
                tx.is_draft = False
                tx.save(update_fields=["is_draft"])

        except Exception as e:
            # Draft intentionally retained
            print("Posting failed, draft kept:", e)

        return redirect("transactions")

    # ----------------------------
    # GET
    # ----------------------------
    context = {
        "accounts": accounts,
        "expense_categories": expense_categories,
        "income_categories": income_categories,
        "tags": tags,
        "persons": persons,
        "today": date.today(),
        "tx": tx,   # IMPORTANT
    }

    return render(request, "transactions/create.html", context)



@login_required
def transaction_delete(request, pk):
    tx = get_object_or_404(
        Transaction,
        pk=pk,
        created_by=request.user,
        is_deleted=False,
    )

    tx.is_deleted = True
    tx.updated_by = request.user
    tx.save(update_fields=["is_deleted", "updated_by"])

    return redirect("transactions")


@login_required
def transaction_edit(request, pk):
    tx = get_object_or_404(
        Transaction,
        pk=pk,
        created_by=request.user,
        is_deleted=False,
    )

    return create_view(request, tx=tx)





@login_required
def transaction_detail(request, pk):
    tx = get_object_or_404(
        Transaction.objects.prefetch_related(
            "items__account",
            "items__expense_items__category",
            "items__expense_items__tags",
            "items__expense_items__person",
        ),
        pk=pk,
        created_by=request.user,
    )

    return render(
        request,
        "transactions/detail.html",
        {"tx": tx},
    )

@login_required
def transaction_draft_delete(request, pk):
    tx = get_object_or_404(
        Transaction,
        pk=pk,
        created_by=request.user,
        is_draft=True,
        is_deleted=False,
    )

    tx.is_deleted = True
    tx.updated_by = request.user
    tx.save(update_fields=["is_deleted", "updated_by"])

    return redirect("transactions")
