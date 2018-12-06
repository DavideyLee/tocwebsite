#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import uuid
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from collections import OrderedDict
from common.utils import get_signer, date_expired_default

__all__ = ['MyUser']

class MyUser(AbstractUser):
    ROLE_ADMIN = 'Admin'
    ROLE_USER = 'User'
    ROLE_APP = 'App'
    OTP_LEVEL_CHOICES = (
        (0, _('禁用')),
        (1, _('启用')),
        (2, _("强制启用")),
    )
    ROLE_CHOICES = (
        (ROLE_ADMIN, _('管理员')),
        (ROLE_USER, _('普通用户')),
        (ROLE_APP, _('应用程序')),
    )
    SOURCE_LOCAL = 'local'
    SOURCE_LDAP = 'ldap'
    SOURCE_OPENID = 'openid'
    SOURCE_CHOICES = (
        (SOURCE_LOCAL, 'Local'),
        (SOURCE_LDAP, 'LDAP/AD'),
        (SOURCE_OPENID, 'OpenID'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(
        max_length=128, unique=True, verbose_name=_('Username')
    )
    name = models.CharField(max_length=128, null=True, verbose_name=_('姓名'))
    usernumber = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('User number')
    )
    email = models.EmailField(
        max_length=128, unique=True, verbose_name=_('Email')
    )
    groups = models.ManyToManyField(
        Group, related_name='users',
        blank=True, verbose_name=_('用户组')
    )
    role = models.CharField(
        choices=ROLE_CHOICES, default='User', max_length=10,
        blank=True, verbose_name=_('角色')
    )
    avatar = models.ImageField(
        upload_to="avatar", null=True, verbose_name=_('头像')
    )
    wechat = models.CharField(
        max_length=128, blank=True, verbose_name=_('微信')
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('手机')
    )
    otp_level = models.SmallIntegerField(
        default=0, choices=OTP_LEVEL_CHOICES, verbose_name=_('MFA')
    )
    comment = models.TextField(
        max_length=200, blank=True, verbose_name=_('备注')
    )
    is_first_login = models.BooleanField(default=True)
    created_by = models.CharField(
        max_length=30, blank=True, verbose_name=_('Created by')
    )
    date_expired = models.DateTimeField(
        default=date_expired_default, blank=True, null=True,
        db_index=True, verbose_name=_('失效日期')
    )
    source = models.CharField(
        max_length=30, default=SOURCE_LOCAL, choices=SOURCE_CHOICES,
        verbose_name=_('Source')
    )

    @property
    def is_superuser(self):
        if self.role == 'Admin':
            return True
        else:
            return False

    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.role = 'Admin'
        else:
            self.role = 'User'

    def avatar_url(self):
        admin_default = settings.MEDIA_URL + "avatar/root.png"
        user_default = settings.STATIC_URL + "avatar/user.png"
        if self.avatar:
            return self.avatar.url
        if self.is_superuser:
            return admin_default
        else:
            return user_default

    def __str__(self):
        return '{0.username}'.format(self)

    class Meta:
        ordering = ['username']
        verbose_name = _("User")

    # @property
    # def admin_orgs(self):
    #     from orgs.models import Organization
    #     return Organization.get_user_admin_orgs(self)
    #
    # @property
    # def is_org_admin(self):
    #     if self.is_superuser or self.admin_orgs.exists():
    #         return True
    #     else:
    #         return False
    #
    # @property
    # def is_app(self):
    #     return self.role == 'App'

    def to_json(self):
        return OrderedDict({
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'role': self.get_role_display(),
            'groups': [group.name for group in self.groups.all()],
            'source': self.get_source_display(),
            'wechat': self.wechat,
            'phone': self.phone,
            'comment': self.comment,
        })
