from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django import forms
from orgs.mixins import OrgModelForm
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ("username", "email")

class UserCreateUpdateForm(OrgModelForm):
    role_choices = ((i, n) for i, n in MyUser.ROLE_CHOICES if i != MyUser.ROLE_APP)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput,
        max_length=128, strip=False, required=False,
    )
    role = forms.ChoiceField(
        choices=role_choices, required=True,
        initial=MyUser.ROLE_USER, label=_("Role")
    )
    public_key = forms.CharField(
        label=_('ssh public key'), max_length=5000, required=False,
        widget=forms.Textarea(attrs={'placeholder': _('ssh-rsa AAAA...')}),
        help_text=_('Paste user id_rsa.pub here.')
    )

    class Meta:
        model = MyUser
        fields = [
            'username', 'name', 'email', 'groups', 'wechat',
            'phone', 'role', 'date_expired', 'comment', 'otp_level'
        ]
        help_texts = {
            'username': '* required',
            'name': '* required',
            'email': '* required',
        }
        widgets = {
            'otp_level': forms.RadioSelect(),
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'select2',
                    'data-placeholder': _('Join user groups')
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UserCreateUpdateForm, self).__init__(*args, **kwargs)

        roles = []
        # Super admin user
        if self.request.user.is_superuser:
            roles.append((MyUser.ROLE_ADMIN, dict(MyUser.ROLE_CHOICES).get(MyUser.ROLE_ADMIN)))
            roles.append((MyUser.ROLE_USER, dict(MyUser.ROLE_CHOICES).get(MyUser.ROLE_USER)))

        # Org admin user
        else:
            user = kwargs.get('instance')
            # Update
            if user:
                role = kwargs.get('instance').role
                roles.append((role, dict(MyUser.ROLE_CHOICES).get(role)))
            # Create
            else:
                roles.append((MyUser.ROLE_USER, dict(MyUser.ROLE_CHOICES).get(MyUser.ROLE_USER)))

        field = self.fields['role']
        field.choices = set(roles)

    def clean_public_key(self):
        public_key = self.cleaned_data['public_key']
        if not public_key:
            return public_key
        if self.instance.public_key and public_key == self.instance.public_key:
            msg = _('Public key should not be the same as your old one.')
            raise forms.ValidationError(msg)

        # if not validate_ssh_public_key(public_key):
        #     raise forms.ValidationError(_('Not a valid ssh public key'))
        return public_key

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        otp_level = self.cleaned_data.get('otp_level')
        public_key = self.cleaned_data.get('public_key')
        user = super().save(commit=commit)
        if password:
            user.set_password(password)
            user.save()
        if otp_level:
            user.otp_level = otp_level
            user.save()
        if public_key:
            user.public_key = public_key
            user.save()
        return user