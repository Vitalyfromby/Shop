from django.urls import path

from .views import *

app_name = 'MainApp'

urlpatterns = [

    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    # path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('', product_list, name='showcase'),
    path('<str:category_slug>/', product_list, name='product_list'),
    path('<str:category_slug>/<int:id>/', product_detail, name='product_detail'),

]

