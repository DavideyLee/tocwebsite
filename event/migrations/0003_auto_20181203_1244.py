# Generated by Django 2.1.3 on 2018-12-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20181203_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='comment',
            field=models.TextField(blank=True, max_length=200, verbose_name='事件描述'),
        ),
        migrations.AlterField(
            model_name='event',
            name='even_dev',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='应用开发负责人'),
        ),
        migrations.AlterField(
            model_name='event',
            name='even_ops',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='应用运营负责人'),
        ),
        migrations.AlterField(
            model_name='event',
            name='even_state',
            field=models.CharField(blank=True, choices=[('state_1', '待审批'), ('state_2', '已审批'), ('state_3', '已处理'), ('state_4', '关闭')], default='LEVEL_7', max_length=10, verbose_name='事件状态'),
        ),
        migrations.AlterField(
            model_name='event',
            name='system_name',
            field=models.CharField(max_length=128, null=True, verbose_name='系统名称'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=70, verbose_name='事件标题'),
        ),
    ]