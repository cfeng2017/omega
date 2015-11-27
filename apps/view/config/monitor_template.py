# -*- coding: utf8 -*-
from flask import render_template, request, flash, redirect, url_for

from apps.service.config_service import ConfigService
from apps.view.config import config
from apps.model.monitor.monitor_template import MonitorTemplate
from apps.model.monitor.monitor_template_name import MonitorTemplateName


@config.route('/t/', methods=['GET'])
def templates():
    cs = ConfigService()
    infos = cs.get_monitor_template_type_and_name()
    return render_template('config/templates_index.html', infos=infos)


@config.route('/t/add_monitor_template/', methods=['GET', 'POST'])
def add_monitor_template():
    cs = ConfigService()
    monitor_type = request.args.get('type')
    if not monitor_type:
        monitor_type = cs.get_all_monitor_template_type()[0]['monitor_type']
    monitor_template_list = [(mt.id, mt.name)
                             for mt in cs.get_all_template_name_by_type(MonitorTemplateName(monitor_type))
                             if mt]
    if request.method == 'POST':
        template_name_id = request.form.get('template_name_id')
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
            _ = []
            if mode_list:
                for ind in range(len(alarm_ds_list)):
                    if alarm_ds_list[ind] == dn:
                        _ = MonitorTemplate(template_name_id, chart_name, chart_desc, dn, dd, 1,
                                            mode_list[ind],
                                            warn_lower_list[ind],
                                            warn_upper_list[ind] if warn_upper_list[ind] else 0,
                                            dis_lower_list[ind],
                                            dis_upper_list[ind] if dis_upper_list[ind] else 0,
                                            last_time_list[ind],
                                            interval_time_list[ind],
                                            begin_time_list[ind],
                                            end_time_list[ind]
                                            )
                        mts.append(_)
            else:                              # 若没有报警规则

                mts.append(MonitorTemplate(template_name_id, chart_name, chart_desc, dn, dd))
        if mts:
            cs.addmany(mts)
            flash('添加成功', 'info')
            return redirect(url_for('.show_monitor_template_info', tid=template_name_id, name=template_name))
        else:
            flash('添加失败，请添加数据源！', 'warning')
    return render_template('config/add_monitor_template.html', mt_list=monitor_template_list, monitor_type=monitor_type)


@config.route('/t/add_ds_template_name/', methods=['POST'])
def add_ds_template_name():
    monitor_type = request.args.get('type').strip()
    if request.method == 'POST':
        t_name = request.form.get('new_template_name')
        mtn = MonitorTemplateName(monitor_type, t_name)
        cs = ConfigService()
        if cs.is_exist(mtn):
            flash('该模板名已存在！', 'warning')
        else:
            cs.add(mtn)
            flash('添加成功！', 'info')
    return redirect(url_for('.add_monitor_template',  type=monitor_type))


@config.route('/t/monitor_template_info/', methods=['GET'])
def show_monitor_template_info():
    tid = request.args.get('tid')
    name = request.args.get('name')
    cs = ConfigService()
    infos = cs.get_monitor_template_info(MonitorTemplate(tid))
    # if not infos:
    #     print 'infos is []'
    return render_template('config/monitor_template_info.html', infos=infos, name=name)


@config.route('/t/add_monitor_template_type/', methods=['GET', 'POST'])
def add_monitor_template_type():
    if request.method == 'POST':
        cs = ConfigService()
        name = request.form.get('name')
        mtype = request.form.get('mtype').lower().strip()
        mtn = MonitorTemplateName(mtype, name)

        if cs.is_exist(mtn):
            flash('模板类型或模板名已存在，请重新输入', 'warning')
        else:
            cs.add(mtn)
            flash('添加成功！', 'info')
    return render_template('config/add_monitor_template_type.html')