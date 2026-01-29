from django.urls import path
from ui.views import (
    dashboard,
    auth,
    profile,
)

urlpatterns = [
    # Dashboard
    path("", dashboard.index, name="dashboard"),

    # Auth
    path("login/", auth.login_view, name="login"),
    path("signup/", auth.signup_view, name="signup"),
    path("logout/", auth.logout_view, name="logout"),

    # Profile
    path("profile/", profile.profile_view, name="profile"),
    path("profile/edit/", profile.profile_edit, name="profile_edit"),
]

from ui.views import accounts

urlpatterns += [
    path("accounts/", accounts.list_view, name="accounts"),
    path("accounts/new/", accounts.create_view, name="account_create"),
    path("accounts/<int:pk>/edit/", accounts.edit_view, name="account_edit"),
]


from ui.views import categories

urlpatterns += [
    path("categories/", categories.tree_view, name="categories"),
    path("categories/new/", categories.create_view, name="category_create"),
    path("categories/<int:pk>/edit/", categories.edit_view, name="category_edit"),
    path("categories/<int:pk>/delete/", categories.delete_view, name="category_delete"),

]

from ui.views import tags

urlpatterns += [
    path("tags/", tags.list_view, name="tags"),
    path("tags/new/", tags.create_view, name="tag_create"),
    path("tags/<int:pk>/edit/", tags.edit_view, name="tag_edit"),
]

from ui.views import persons

urlpatterns += [
    path("persons/", persons.list_view, name="persons"),
    path("persons/new/", persons.create_view, name="person_create"),
    path("persons/<int:pk>/edit/", persons.edit_view, name="person_edit"),
]

from ui.views import transactions

urlpatterns += [
    path("transactions/", transactions.list_view, name="transactions"),
    path("transactions/new/", transactions.create_view, name="transaction_create"),
    
    path("<int:pk>/", transactions.transaction_detail, name="transaction_detail"),
    path("<int:pk>/edit/", transactions.transaction_edit, name="transaction_edit"),
    path("<int:pk>/delete/", transactions.transaction_delete, name="transaction_delete"),
    path("<int:pk>/draft/delete/", transactions.transaction_draft_delete, name="transaction_draft_delete"),

]



