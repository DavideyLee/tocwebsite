from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import MyUser
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from common.permissions import AdminUserRequiredMixin
from django.utils.translation import ugettext as _
from orgs.utils import current_org
from .models import UserGroup
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from common.const import create_success_msg, update_success_msg
from django.http.response import JsonResponse
from django.core import serializers
from .signals import post_user_create
from . import forms
# Create your views here.

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    else:
        return render(request, 'index.html')


class UserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = MyUser
    form_class = forms.UserCreateUpdateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users:user_list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'app': _('Users'), 'action': _('创建用户')})
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.created_by = self.request.user.username or 'System'
        user.save()
        post_user_create.send(self.__class__, user=user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs

# class UserListView(TemplateView):
#     template_name = 'users/user_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_myuers'] = MyUser.objects.all()
#         context.update({
#             'app': _('Users'),
#             'action': _('用户列表'),
#         })
#         print(context)
#         return context

class UserListView(AdminUserRequiredMixin,TemplateView):
    model = MyUser
    template_name = 'users/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_myuers'] = MyUser.objects.all()
        context.update({
            'app': _('用户管理'),
            'action': _('用户列表'),
        })
        # print(MyUser.to_json(self))
        print(context)
        return context


class UserDetailView(AdminUserRequiredMixin, DetailView):
    model = MyUser
    template_name = 'users/user_detail.html'
    context_object_name = "user_object"
    key_prefix_block = "_LOGIN_BLOCK_{}"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        key_block = self.key_prefix_block.format(user.username)
        groups = UserGroup.objects.exclude(id__in=self.object.groups.all())
        context = {
            'app': _('Users'),
            'action': _('User detail'),
            'groups': groups,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        org_users = current_org.get_org_users().values_list('id', flat=True)
        queryset = queryset.filter(id__in=org_users)
        return queryset
