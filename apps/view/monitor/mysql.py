# -*- coding: utf8 -*-
import datetime
from flask import render_template, request, flash, redirect, url_for, jsonify, g

from apps.view.user import login_required
from apps.service.monitor_service import MonitorService
from apps.model.asset.mysql_instance import MysqlInstance
from apps.model.monitor.monitor_template_name import MonitorTemplateName
from apps.model.monitor.chart import Chart
from apps.model.monitor.ds import Ds
from apps.model.monitor.monitor_alarm import MonitorAlarm
from apps.view.monitor import monitor, MYSQL


@monitor.route('/m/')
def mysql_index():
    ms = MonitorService()
    mysql_type = ms.get_groups_by_type(MYSQL)

    gtypes = [t[0] for t in mysql_type]
    mysql_infos = ms.get_all_online_infos(MysqlInstance(), gtypes)
    infos = []
    for mt in mysql_type:
        ginfos, _ = [], {}
        for mi in mysql_infos:
            if mi[0] != mt[0]:
                continue
            else:
                ginfo = {'hid': mi[1],
                         'iid': mi[2],
                         'host': mi[3],
                         'ip': mi[4],
                         'port': mi[5],
                         'role': 'Master' if mi[6] == 1 else 'Slave'
                         }
                ginfos.append(ginfo)
            _['gid'] = mt[0]
            _['gname'] = mt[1]
            _['ginfos'] = ginfos
        if ginfos:
            infos.append(_)
    return render_template('monitor/mysql_index.html', infos=infos)


@monitor.route('/m/group/')
def mysql_group():
    return render_template('monitor/mysql_group.html')


@monitor.route('/m/host/')
def mysql_host():
    ms = MonitorService()
    r_infos = ms.get_all_hosts(MysqlInstance())
    hosts = []
    for i in r_infos:
        hosts.append(i[0])
    templates = ms.get_tmeplate_by_hid_list(hosts)

    online_hosts, offline_hosts = [], []
    for i in r_infos:
        cids, tids, tnames = [], [], []
        for t in templates:
            if i[0] == t[1]:
                cids.append(t[0])
                tids.append(t[2])
                tnames.append(t[3])
        _ = {}
        _['id'] = i[0]
        _['name'] = i[1]
        _['chart_id'] = cids
        _['tid'] = tids
        _['tnames'] = tnames
        if i[2] == 1:
            online_hosts.append(_)
        else:
            offline_hosts.append(_)
    template_types = [t[0] for t in ms.get_all_monitor_template_type()]
    return render_template('monitor/mysql_host.html', online_hosts=online_hosts,
                           offline_hosts=offline_hosts, template_types=template_types)


@monitor.route('/m/host/<hid>/')
def mysql_host_info(hid):
    ms = MonitorService()
    charts = ms.get_charts_by_hid(hid)
    cids = [c[0] for c in charts]
    dss = ms.get_ds_by_chart_id_list(cids)
    infos = []
    for c in charts:
        ds_list = []
        for d in dss:
            if c[0] == d.chart_id:
                _ = {}
                _['ds_id'] = d.id
                _['ds_name'] = d.name
                _['ds_desc'] = d.description
                ds_list.append(_)
        infos.append({'chart_id': c[0], 'chart_name': c[1], 'chart_desc': c[2], 'ds_list': ds_list})
    return render_template('monitor/mysql_host_chart.html', hid=hid, infos=infos)


@monitor.route('/m/instance/')
def mysql_instance():
    return render_template('monitor/mysql_instance.html')


@monitor.route('/m/get_template_name_by_type/')
def get_template_name_by_type():
    template_type = request.args.get('type')
    ms = MonitorService()
    raw_templates = ms.get_all_template_name_by_type(MonitorTemplateName(template_type))
    templates = [{'id': t.id, 'name': t.name} for t in raw_templates]
    return jsonify(templates=templates)


@monitor.route('/m/mysql_host_relate_to_template/', methods=['GET', 'POST'])
@login_required
def mysql_host_relate_to_template():
    tid = request.args.get('template_name_id')
    hid = request.args.get('hid')

    ms = MonitorService()

    # 如果已经host已经关联
    if ms.is_exist(tid, hid):
        flash('该主机已关联此模板', 'warning')
        return redirect(url_for('.mysql_host'))

    # 初始化chart
    initial_chart_list, initial_chart_name_list = [], []
    template_infos = ms.get_charts_by_template_id(tid)
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    for ti in template_infos:
        if ti.chart_name not in initial_chart_name_list:
            _ = Chart(tid, ti.chart_name, ti.chart_description, 0, hid, 0, g.user.id, '', now)
            initial_chart_list.append(_)
            initial_chart_name_list.append(ti.chart_name)
    ms.addmany(initial_chart_list)

    # 初始化数据源
    initial_ds_list = []
    chart_infos = ms.get_chart_name_and_description_by_template_id_and_hid_list(tid, [hid])
    for c in chart_infos:
        for t in template_infos:
            if t.chart_name == c[2]:
                _ = Ds(t.ds_name, t.ds_description, c[0])
                initial_ds_list.append(_)
    ms.addmany(initial_ds_list)

    # 初始化报警规则
    initial_alarm_list = []
    chart_id_list = [c[0] for c in chart_infos]
    ds_infos = ms.get_ds_by_chart_id_list(chart_id_list)
    for d in ds_infos:
        for t in template_infos:
            if d.name == t.ds_name:
                _ = MonitorAlarm(t.id, d.id, t.status, t.mode, t.warn_lower, t.warn_upper, t.disaster_lower,
                                 t.disaster_upper, t.last, t.interval, t.begin_time, t.end_time)
                initial_alarm_list.append(_)
    ms.addmany(initial_alarm_list)
    flash('模板关联成功！', 'info')
    return redirect(url_for('.mysql_host'))


