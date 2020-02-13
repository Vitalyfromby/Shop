from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView

from .forms import RegisterUserForm, ChangeUserInfoForm
from .utilities import signer
from .models import Category, Product, Customer


class BBLoginView(LoginView):
    template_name = 'shop/users/login.html'


@login_required
def profile(request):
    return render(request, 'shop/users/profile.html')


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'shop/users/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'shop/users/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('MainApp:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = Customer
    template_name = 'shop/users/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('MainApp:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'shop/users/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'shop/users/bad_signature.html')
    user = get_object_or_404(Customer, username=username)
    if user.is_activated:
        template = 'shop/users/user_is_activated.html'
    else:
        template = 'shop/users/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


def product_list(request, category_slug=None):
    selected_category = None
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    return render(request,
                  'shop/product/list.html',
                  {'category': selected_category,
                   'selected_category': selected_category,
                   'products': products,
                   'cart_product_form': cart_product_form})


def product_detail(request, category_slug, id):
    product = get_object_or_404(Product,
                                id=id,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {
                      'product': product,
                      'cart_product_form': cart_product_form})

