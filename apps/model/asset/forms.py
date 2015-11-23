# -*- coding: utf-8 -*-
from wtforms import Form, StringField, validators, SubmitField, SelectMultipleField, \
    SelectField, FormField, TextAreaField, IntegerField, RadioField, widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class GTForm(Form):
    gt_gtname = StringField(u'组类型名称', [validators.required('组类型名称必须填写！'), validators.length(max=30)])
    gt_submit = SubmitField(u'提交')


class GTypeSelectForm(Form):
    gtype = SelectField(u'组类型', coerce=int)


class GTypeNameForm(Form):
    gtype = FormField(GTypeSelectForm)
    gname = SelectField(u'组名', coerce=int)


class GDbForm(Form):
    gdb_gname = FormField(GTypeNameForm)
    gdb_db = StringField(u'db名', [validators.required("db名必须填写！"), validators.length(max=30)])
    gdb_submit = SubmitField(u'提交')


class GForm(Form):
    g_name = StringField(u'组名', [validators.required('组名必须填写！'), validators.length(max=30)])
    g_gtype = FormField(GTypeSelectForm)
    g_des = StringField(u'简介', [validators.length(max=100)])
    g_scenario = TextAreaField(u'使用场景', [validators.length(max=500)])
    g_contacts = StringField(u'联系人', [validators.length(max=100)])
    g_submit = SubmitField(u'提交')


class HAWForm(Form):
    haw_type = SelectField(u'类型', coerce=int)
    host_wel_next = SubmitField(u'下一步')


class HAHForm(Form):
    haf_text = TextAreaField(u'机器', [validators.required('机器名发布填写！')])
    host_ip_pre = SubmitField(u'上一步')
    host_ip_next = SubmitField(u'下一步')


class HForm(Form):
    h_name = StringField(u'机器名', [validators.required('机器名必须填写！'), validators.length(max=30)])
    h_core = IntegerField(u'cpu核数', [validators.required('cpu核数需为整数')])
    h_memory = IntegerField(u'内存大小', [validators.required('内存大小需为整数')])
    h_disk_type = SelectField(u'磁盘类型', choices=[(0, 'SAS'), (1, 'SSD'), (2, 'SATA')], coerce=int)
    h_disk_num = IntegerField(u'磁盘数量', [validators.required('磁盘数量需为整数')])
    h_disk_size = IntegerField(u'单盘容量', [validators.required('单盘容量需为整数')])
    h_eth = SelectField(u'网卡设备', choices=[(0, 'eth0'), (1, 'em0')], coerce=int)
    h_ip = StringField(u'网卡IP', [validators.required('网卡ip必须填写！'), validators.length(max=15)])
    h_remote_ip = StringField(u'远控卡IP', [validators.length(max=15)])
    h_idc = SelectField(u'IDC', choices=[(0, '天津IDC'), (1, 'IDC10'), (2, 'IDC20')], coerce=int)
    h_rack = StringField(u'机架位置')
    h_brf = RadioField(u'充放电', choices=[('0', '否'), ('1', '是')], default='0')
    h_brt = StringField(u'放电时间')
    h_status = RadioField(u'机器状态', choices=[('0', 'offline'), ('1', 'online')], default='0')
    h_remark = TextAreaField(u'备注', [validators.length(max=200)])
    h_submit = SubmitField(u'提交')


class InstanceForm(Form):
    i_name = SelectField(u'组名', coerce=int)
    i_hostname = StringField(u'机器名', [validators.required(u'机器名必须填写！'), validators.length(32)])
    i_port = IntegerField(u'port')
    i_ip = StringField(u'ip')
    i_version = StringField(u'版本号')
    i_status = RadioField(u'状态', choices=[('0', 'offline'), ('1', 'online')], default='0')
    i_role = SelectField(u'角色', coerce=int)
    i_remark = StringField(u'备注', [validators.length(max=200)])
    i_submit = SubmitField(u'提交')


class MysqlForm(Form):
    i_base = FormField(InstanceForm)


class McForm(Form):
    i_base = FormField(InstanceForm)
    mc_mem = IntegerField(u'分配内存')
    mc_thread = StringField(u'进程数')
    mc_factor = IntegerField(u'增长因子')
    mc_con = IntegerField(u'最大连接数')
    mc_user = StringField(u'用户')
    mc_para = StringField(u'其他参数')


class RedisForm(Form):
    i_base = FormField(InstanceForm)
    r_mem = IntegerField(u'分配内存')
    r_pre = RadioField(u'持久化', choices=[('0', '否'), ('1', '是')], default='0')
