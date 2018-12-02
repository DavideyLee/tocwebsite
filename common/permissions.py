from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.http.response import HttpResponseForbidden
from orgs.utils import current_org

class AdminUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not current_org.can_admin_by(self.request.user):
            self.raise_exception = True
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if not current_org:
            return redirect('orgs:switch-a-org')

        if not current_org.can_admin_by(request.user):
            if request.user.is_org_admin:
                return redirect('orgs:switch-a-org')
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)