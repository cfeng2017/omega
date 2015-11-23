# -*- coding: utf8 -*-
from flask import render_template, request, flash, jsonify, redirect, url_for, make_response

from apps.service.config_service import ConfigService
from apps.view.config import config
from apps.model.config.monitor_template import MonitorTemplate


@config.route('/t/', methods=['GET'])
def templates():
    cs = ConfigService()
    infos = cs.get_monitor_template_type_and_name()
    print infos, '--------------'
    return render_template('config/templates_index.html', infos=infos)


@config.route('/t/add_monitor_template/', methods=['GET', 'POST'])
def add_monitor_template():
    cs = ConfigService()
    monitor_template_list = [mt[0] for mt in cs.get_all_template_name(MonitorTemplate()) if mt]
    if request.method == 'POST':
        template_name = request.form.get('template_name')
        chart_name = request.form.get('chart_name')
        chart_desc = request.form.get('chart_desc')
        ds_name_list = request.form.getlist('ds_name')
        ds_desc_list = request.form.getlist('ds_desc')
        alarm_ds_list = request.form.getlist('selected_ds')
        mode_list = request.form.getlist('mode')
        warn_lower_list = request.form.getlist('warn_lower')
        warn_upper_list = request.form.getlist('warn_upper')
        dis_lower_list = request.form.getlist('dis_lower')
        dis_upper_list = request.form.getlist('dis_upper')
        last_time_list = request.form.getlist('last_time')
        interval_time_list = request.form.getlist('interval_time')
        begin_time_list = request.form.getlist('begin_time')
        end_time_list = request.form.getlist('end_time')

        mts = []
        for index in range(len(ds_name_list)):
            dn, dd = ds_name_list[index], ds_desc_list[index]
            rules = []
            for ind in range(len(alarm_ds_list)):
                rule = {}
                if mode_list[ind] == '3':
                    rule['warn_upper'] = warn_upper_list[ind]
                    rule['dis_upper'] = dis_upper_list[ind]
                if alarm_ds_list[ind] == dn:
                    rule['mode'] = mode_list[ind]
                    rule['warn_lower'] = warn_lower_list[ind]
                    rule['dis_lower'] = dis_lower_list[ind]
                    rule['last'] = last_time_list[ind]
                    rule['interval'] = interval_time_list[ind]
                    rule['begin_time'] = begin_time_list[ind]
                    rule['end_time'] = end_time_list[ind]
                    rules.append(rule)
            mts.append(MonitorTemplate(template_name, chart_name, chart_desc, dn, dd, str(rules)))
        if mts:
            cs.addmany(mts)
            flash('添加成功', 'info')
        else:
            flash('添加失败', 'warning')
    return render_template('config/add_monitor_template.html', mt_list=monitor_template_list)


@config.route('/t/add_ds_template_name/', methods=['POST'])
def add_ds_template_name():
    if request.method == 'POST':
        t_name = request.form.get('new_template_name')
        mt = MonitorTemplate(t_name)
        cs = ConfigService()
        if cs.is_exist(mt):
            flash('该模板名已存在！', 'warning')
        else:
            cs.add(mt)
    return redirect(url_for('.add_monitor_template'))


@config.route('/t/monitor_template_info/', methods=['GET'])
def show_monitor_template_info(template_name=''):
    cs = ConfigService()
    if template_name:
        aa = cs.get_monitor_template_info(template_name)
    else:
        aa = cs.get_ss

    return render_template('config/monitor_template_info/')
