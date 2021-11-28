from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages

from .models import User
from orders.models import Order, OrderItem
from .forms import ChangeUserInfoForm, RegisteredUserForm


class LoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    orders = Order.objects.filter(owner=request.user)
    return render(request, 'main/profile.html', {'orders': orders})



class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'



class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    send_message = 'Пароль пользователя изменён'



class RegisterUserView(CreateView):
    model = User
    template_name = 'main/register_user.html'
    form_class = RegisteredUserForm
    success_url = reverse_lazy('accounts:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('accounts:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

def order_list(request):
    orders = Order.objects.filter(owner=request.user)
    return render(request, 'main/profile.html',{'orders': orders,})