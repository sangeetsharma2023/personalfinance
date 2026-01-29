from transactions.models import Transaction, TransactionItem, ExpenseItem
from accounts.models import Account


def create_transaction_service(
    *,
    user,
    transaction_type,
    date,
    narration,
    from_account,
    to_account,
    amount,
    expense_items=None,
    reversed_transaction=None,
):
    """
    Central transaction creation logic.
    """

    tx = Transaction.objects.create(
        transaction_type=transaction_type,
        date=date,
        narration=narration,
        is_draft=False,
        reversed_transaction=reversed_transaction,
        created_by=user,
    )

    # ---- DEBIT / CREDIT LOGIC ----
    if transaction_type in ("EXPENSE", "TRANSFER"):
        debit_account = to_account
        credit_account = from_account
    elif transaction_type == "INCOME":
        debit_account = to_account
        credit_account = from_account
    else:
        raise ValueError("Unsupported transaction type")

    # Debit
    debit_item = TransactionItem.objects.create(
        transaction=tx,
        account=debit_account,
        amount=amount,
        is_debit=True,
        created_by=user,
    )

    # Credit
    TransactionItem.objects.create(
        transaction=tx,
        account=credit_account,
        amount=amount,
        is_debit=False,
        created_by=user,
    )

    # ---- EXPENSE ITEMS ----
    if transaction_type == "EXPENSE" and expense_items:
        total = sum(item["amount"] for item in expense_items)
        if total != amount:
            raise ValueError("Expense items total must match transaction amount")

        for item in expense_items:
            ExpenseItem.objects.create(
                transaction_item=debit_item,
                description=item["description"],
                category=item["category"],
                amount=item["amount"],
                person=item.get("person"),
                created_by=user,
            ).tags.set(item.get("tags", []))

    return tx
