#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser,PermissionsMixin):
    ROLE_ADMIN = 'Admin'
    ROLE_USER = 'User'

    ROLE_CHOICES = (
        (ROLE_ADMIN, _('Administrator')),
        (ROLE_USER, _('User')),
    )

    SOURCE_LOCAL = 'local'
    SOURCE_LDAP = 'ldap'
    SOURCE_CHOICES = (
        (SOURCE_LOCAL, 'Local'),
        (SOURCE_LDAP, 'LDAP/AD'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    username = models.CharField(
        max_length=128, unique=True, verbose_name=_('Username')
    )

    usernumber = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('User number')
    )

    name = models.CharField(max_length=128, verbose_name=_('Name'))
    email = models.EmailField(
        max_length=128, unique=True, verbose_name=_('Email')
    )
    groups = models.ManyToManyField(
        'users.UserGroup', related_name='users',
        blank=True, verbose_name=_('User group')
    )
    role = models.CharField(
        choices=ROLE_CHOICES, default='User', max_length=10,
        blank=True, verbose_name=_('Role')
    )
    avatar = models.ImageField(
        upload_to="avatar", null=True, verbose_name=_('Avatar')
    )
    wechat = models.CharField(
        max_length=128, blank=True, verbose_name=_('Wechat')
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('Phone')
    )

    comment = models.TextField(
        max_length=200, blank=True, verbose_name=_('Comment')
    )
    is_first_login = models.BooleanField(default=True)

    created_by = models.CharField(
        max_length=30, default='', verbose_name=_('Created by')
    )
    source = models.CharField(
        max_length=30, default=SOURCE_LOCAL, choices=SOURCE_CHOICES,
        verbose_name=_('Source')
    )

    def __str__(self):
        return '{0.name}({0.username})'.format(self)

    class Meta:
        ordering = ['username']
        verbose_name = _("User")