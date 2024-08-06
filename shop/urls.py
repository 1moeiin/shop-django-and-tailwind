from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "shop"

urlpatterns = [
    path('', views.main, name="main"),
    path('products/', views.products_list, name="products_list"),
    path('products/<pk>/<slug:slug>', views.product_details, name="product_details"),
    path('products/<slug:category_slug>/', views.products_list, name='product_list_by_category'),
    path('products/<product_id>/<product_slug>/comment', views.product_comment, name="product_comment"),
    
    path('ticket/', views.ticket, name="ticket"),
    path('search/', views.search_post, name="search_post"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('disabelaccount/', views.disable_account, name="disable_account"),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    
    path('password-reset', auth_views.PasswordResetView.as_view(success_url='password-reset/done/'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete/'), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path('register/', views.register, name="register"),
]
