from django.urls import path 
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view 
from app.forms import LoginForm, ChangePasswordForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [

    path('',views.ProductView.as_view(), name='home'),

    path('product-details/<int:pk>',views.ProductDetailView.as_view(), name='product_details'),

    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name="show-cart"),
    path('pluscart/',views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('buy/',views.buy_now, name='buy-now'),

    # path('profile/',views.profile, name='profile'),
    path('profile/',views.CustomerProfileView.as_view(), name='profile'),

    path('address/',views.address, name='address'),

    path('checkout/', views.Checkout.as_view(), name='checkout'),

    path('paymentdone/',views.payment_done, name='paymentdone'),

    path('orders/',views.orders, name='orders'),

    # path('changepassword/',views.change_password, name='changepassword'),
    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=ChangePasswordForm , success_url='/changepassworddone/'), name='changepassword'),

    path('changepassworddone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/changepassworddone.html') , name="changepassworddone"),


    path('resetpassword/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class = MyPasswordResetForm), name='resetpassword'),

    path('resetpassword/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('resetpassword/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('mobile/',views.mobile, name='mobile'),

    path('mobile/<slug:data>',views.mobile, name='mobiledata'),

    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),

    path('logout/', auth_view.LogoutView.as_view(next_page='home'), name='logout'),

    path('registration/', views.registration, name='registration'),
    # path('registration/',views.CustomerRegistrationView.as_view(), name='registration'),

   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
