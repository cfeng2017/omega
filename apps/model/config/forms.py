# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators, SubmitField, SelectMultipleField, DateTimeField, \
    SelectField, FormField, TextAreaField, IntegerField, BooleanField, RadioField

#
# class TForm(Form):
#     chart_name = StringField(u'图表名', [validators.required('图表名须填写！'), validators.length(max=50)])
#     ds_name = StringField(u'数据源名', [validators.required('数据源名须填写！'), validators.length(max=50)])
#     level = SelectField(u'报警级别', choices=[(0, '严重'), (1, '警告')], coerce=int)
#     begin_time = DateTimeField(u'报警起始时间', format='%H:%M')
#     end_time = DateTimeField(u'报警结束时间', format='%H:%M')
#     mode = SelectField(u'报警模式', choices=[(0, '上限'), (1, '下限'), (2, '范围'), (3, '斜率')], coerce=int)
#     threshold = IntegerField(u'报警阈值', [validators.required('报警阈值须为整数！')], default=0)
#     interval = IntegerField(u'报警间隔', [validators.required('报警间隔须为整数！')], default=1)
#     last = IntegerField(u'延迟报警', [validators.required('报警间隔须为整数！')], default=1)
#     status = RadioField(u'开启报警', choices=[(0, 'offline'), (1, 'online')], coerce=int, default=0)
#     desc = TextAreaField(u'描述', [validators.length(max=500)])
#     t_submit = SubmitField(u'提交')