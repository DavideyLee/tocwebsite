from django.db import models
import uuid
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Event(models.Model):
    LEVEL_1 = 'level_1'
    LEVEL_2 = 'level_2'
    LEVEL_3 = 'level_3'
    LEVEL_4 = 'level_4'
    LEVEL_5 = 'level_5'
    LEVEL_6 = 'level_6'
    LEVEL_7 = 'level_7'

    EVENT_LEVEL_CHOICES = (
        (LEVEL_1, _('1级事件')),
        (LEVEL_2, _('2级事件')),
        (LEVEL_3, _('3级事件')),
        (LEVEL_4, _('4级事件')),
        (LEVEL_5, _('5级事件')),
        (LEVEL_6, _('6级事件')),
        (LEVEL_7, _('7级事件')),
    )

    STATE_1 = 'state_1'
    STATE_2 = 'state_2'
    STATE_3 = 'state_3'
    STATE_4 = 'state_4'

    EVENT_STATE_CHOICES = (
        (STATE_1, _('待审批')),
        (STATE_2, _('已审批')),
        (STATE_3, _('已处理')),
        (STATE_4, _('关闭')),
    )

    even_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=70, verbose_name=_('事件标题'))   # 事件标题
    created_time = models.DateTimeField(verbose_name=_('创建时间'))
    modified_time = models.DateTimeField(verbose_name=_('修改时间'))
    finish_time = models.DateTimeField(verbose_name=_('处理结束时间'))
    even_starttime = models.DateTimeField(verbose_name=_('事件开始时间'))
    even_endtime = models.DateTimeField(verbose_name=_('事件恢复时间'))
    system_name = models.CharField(max_length=128, null=True, verbose_name=_('系统名称'))
    even_level = models.CharField(
        choices=EVENT_LEVEL_CHOICES, default='LEVEL_7', max_length=10,
        blank=True, verbose_name=_('事件等级')
    )
    even_ops = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('应用运营负责人')
    )
    even_dev = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('应用开发负责人')
    )
    comment = models.TextField(
        max_length=200, blank=True, verbose_name=_('事件描述')
    )
    even_state = models.CharField(
        choices=EVENT_STATE_CHOICES, default='LEVEL_7', max_length=10,
        blank=True, verbose_name=_('事件状态')
    )

