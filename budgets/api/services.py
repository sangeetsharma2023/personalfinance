from django.db.models import Sum
from transactions.models import TransactionItem, ExpenseItem


def calculate_budget_spent(budget):
    """
    Calculates total spent for a budget.
    """

    qs = ExpenseItem.objects.filter(
        transaction_item__transaction__date__gte=budget.start_date,
        transaction_item__transaction__date__lte=budget.end_date,
        transaction_item__transaction__is_draft=False,
        transaction_item__transaction__is_deleted=False,
        transaction_item__transaction__created_by=budget.created_by,
    )

    if budget.category:
        qs = qs.filter(
            category__in=budget.category.get_descendants(include_self=True)
        )

    if budget.person:
        qs = qs.filter(person=budget.person)

    if budget.tags.exists():
        qs = qs.filter(tags__in=budget.tags.all()).distinct()

    return qs.aggregate(
        total=Sum("amount")
    )["total"] or 0


def calculate_allocation_spent(allocation):
    qs = ExpenseItem.objects.filter(
        transaction_item__transaction__date__gte=allocation.budget.start_date,
        transaction_item__transaction__date__lte=allocation.budget.end_date,
        transaction_item__transaction__is_draft=False,
        transaction_item__transaction__is_deleted=False,
        transaction_item__transaction__created_by=allocation.created_by,
        category__in=allocation.category.get_descendants(include_self=True),
    )

    return qs.aggregate(
        total=Sum("amount")
    )["total"] or 0
