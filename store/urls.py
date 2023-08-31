from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("register",views.sign_up, name="register"),
    path("login",views.sign_in, name="login"),
    path("logout",views.sign_out, name="logout"),
    path("change_password",views.change_password, name="change_password"),
    path("cart", views.cart, name="cart"),
    path('add_cart', views.add_cart, name='add_cart'),
    path('delete_comment', views.delete_comment, name='delete_comment'),
    path('delete_cart_item', views.delete_cart_item, name='delete_cart_item'),
    path('update_volume', views.update_volume, name='update_volume'),
    # path("404", views.not_found, name="not_found"),
    path("<slug:slug>",views.product, name="product"),
    path("add_comment/<slug:slug>/", views.add_comment, name="add_comment"),
    path("<slug:slug>/<int:comment_id>/", views.edit_comment, name="edit_comment"),
    
    
]