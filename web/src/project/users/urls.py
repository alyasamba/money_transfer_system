from django.urls import re_path, path
from django.conf.urls import url
from users.views import UserListView, UserDetailsView, UserCreateUpdateView
from money.views import AccountListForOwnerView, AccountListOfUserView

urlpatterns = [
    path('create/', UserCreateUpdateView.as_view(), name='user_create'),
    path('<int:pk>/edit/', UserCreateUpdateView.as_view(), name='user_edit'),
    path('<int:pk>/accounts/', AccountListOfUserView.as_view(), name='account_list_of_user'),
    path('<int:pk>/', UserDetailsView.as_view(), name='user_details'),
    path('accounts/create/', AccountListForOwnerView.as_view(), name='account_create'),
    path('accounts/', AccountListForOwnerView.as_view(), name='my_accounts'),
    path('', UserListView.as_view(), name='user_list'),
]