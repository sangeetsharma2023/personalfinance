from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from categories.models import Category
from django.db.models import Count
from transactions.models import TransactionItem


@login_required
def tree_view(request):
    roots = Category.objects.filter(
        created_by=request.user,
        parent__isnull=True,
        is_deleted=False
    ).order_by("name")

    def attach_counts(nodes):
        result = []
        for node in nodes:
            node.tx_count = get_category_tx_count(node)
            node.children_cached = attach_counts(
                node.children.filter(is_deleted=False)
            )
            result.append(node)
        return result

    categories = attach_counts(roots)

    return render(
        request,
        "categories/tree.html",
        {"categories": categories}
    )



@login_required
def create_view(request):
    parent_id = request.GET.get("parent")

    if request.method == "POST":
        Category.objects.create(
            name=request.POST.get("name"),
            category_type=request.POST.get("category_type"),
            parent_id=request.POST.get("parent") or None,
            is_active=bool(request.POST.get("is_active")),
            created_by=request.user,
        )
        messages.success(request, "Category created")
        return redirect("categories")

    parents = Category.objects.filter(
        created_by=request.user,
        is_deleted=False
    )

    return render(
        request,
        "categories/create.html",
        {
            "parents": parents,
            "category_types": Category.CATEGORY_TYPES,
            "selected_parent": parent_id,
        }
    )



@login_required
def edit_view(request, pk):
    category = get_object_or_404(
        Category,
        pk=pk,
        created_by=request.user,
        is_deleted=False
    )

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.parent_id = request.POST.get("parent") or None
        category.is_active = bool(request.POST.get("is_active"))
        category.save()

        messages.success(request, "Category updated")
        return redirect("categories")

    parents = Category.objects.filter(
        created_by=request.user,
        is_deleted=False
    ).exclude(id=pk)

    return render(
        request,
        "categories/edit.html",
        {
            "category": category,
            "parents": parents,
        }
    )



def get_category_tx_count(category):
    categories = get_descendant_categories(category)

    return TransactionItem.objects.filter(
        expense_items__category__in=categories,
        transaction__is_deleted=False,
        transaction__is_draft=False,
    ).distinct().count()



@login_required
def delete_view(request, pk):
    category = get_object_or_404(
        Category,
        pk=pk,
        created_by=request.user,
        is_deleted=False
    )

    if get_category_tx_count(category) > 0:
        messages.error(request, "Cannot delete category with transactions")
        return redirect("categories")

    category.is_deleted = True
    category.save(update_fields=["is_deleted"])

    messages.success(request, "Category deleted")
    return redirect("categories")

def get_descendant_categories(category):
    """
    Recursively collect category + all its children.
    """
    result = [category]
    for child in category.children.filter(is_deleted=False):
        result.extend(get_descendant_categories(child))
    return result

