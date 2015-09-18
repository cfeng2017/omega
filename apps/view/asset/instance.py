# -*- encoding: utf8 -*-
from flask import render_template, request, flash, redirect, url_for
from apps.view.asset import asset
from apps import app
from apps.service.asset_service import AssetService
from apps.model.asset.mysql_instance import MysqlInstance
from apps.model.asset.redis_instance import RedisInstance
from apps.model.asset.mc_instance import McInstance
from apps.model.asset.forms import MysqlForm, McForm, RedisForm


@asset.route('/i/')
def instances():
    aservice = AssetService()
    m_return_groups = aservice.get_all_mysql_instance_info()
    m_groups = shuffle_groups(m_return_groups)

    mc_return_groups = aservice.get_all_mc_instance_info()
    mc_groups = shuffle_groups(mc_return_groups)

    r_return_groups = aservice.get_all_redis_instance_info()
    r_groups = shuffle_groups(r_return_groups)

    return render_template('asset/instance_info.html', m_groups=m_groups, mc_groups=mc_groups, r_groups=r_groups)


def shuffle_groups(s_groups):
    groups = []
    for g in s_groups:
        info = [v for i, v in enumerate(g) if i != 1 and i != 2]
        if (not groups and g[1] not in groups) or (groups and g[1] != groups[-1]['gid']):
            _ = dict()
            _['gid'] = g[1]
            _['gname'] = g[2]
            _['infos'] = []
            _['infos'].append(info)
            groups.append(_)
        else:
            groups[-1]['infos'].append(info)
    return groups


@asset.route('/i/add_mysql/', methods=['GET', 'POST'])
def add_mysql_instance():
    aservice = AssetService()
    gtype = aservice.get_gtype_by_type_name("MYSQL")
    group_names = [(g.id, g.name) for g in aservice.get_group_by_type(gtype.id)]
    form = MysqlForm(request.form)
    form.i_base.i_role.choices = [(0, 'Master'), (1, 'Slave')]
    form.i_base.i_name.choices = group_names
    if request.method == 'POST' and form.validate():
        gid = form.i_base.i_name.data
        ver = form.i_base.i_version.data
        host = form.i_base.i_hostname.data
        ip = form.i_base.i_ip.data
        port = form.i_base.i_port.data
        role = form.i_base.i_role.data
        status = form.i_base.i_status.data
        remark = form.i_base.i_remark.data

        r_hid = aservice.get_hid_by_name(host)
        if not r_hid:
            flash(u'该机器名不存在，请重新填写！', 'warning')
        else:
            hid = r_hid[0]
            check_ins = aservice.find_mysql_instance_by_name_and_ip_and_port(gid, hid, ip, port)
            if not check_ins:
                mi = MysqlInstance(gid, hid, ip, port, role, status, ver, remark)
                aservice.add(mi)
                flash(u"Add Success!", 'info')
                return redirect(url_for('.instances'))
            else:
                flash(u'该实例已存在，请重新填写！', 'warning')
    return render_template('asset/add_instance.html', form=form, gtype=gtype)


@asset.route('/i/add_mc/', methods=['GET', 'POST'])
def add_mc_instance():
    aservice = AssetService()
    gtype = aservice.get_gtype_by_type_name("MEMCACHED")
    group_names = [(g.id, g.name) for g in aservice.get_group_by_type(gtype.id)]
    form = McForm(request.form)
    form.i_base.i_role.choices = [(0, 'StandAlone'), (1, 'Master'), (2, 'Slave')]
    form.i_base.i_name.choices = group_names
    if request.method == 'POST' and form.validate():
        gid = form.i_base.i_name.data
        ver = form.i_base.i_version.data
        host = form.i_base.i_hostname.data
        ip = form.i_base.i_ip.data
        port = form.i_base.i_port.data
        role = form.i_base.i_role.data
        status = form.i_base.i_status.data
        remark = form.i_base.i_remark.data
        mem = form.mc_mem.data
        thread = form.mc_thread.data
        factor = form.mc_factor.data
        con = form.mc_con.data
        muser = form.mc_user.data
        para = form.mc_para.data

        r_hid = aservice.get_hid_by_name(host)
        if not r_hid:
            flash(u'该机器名不存在，请重新填写！', 'warning')
        else:
            hid = r_hid[0]
            check_ins = aservice.find_mc_instance_by_name_and_ip_and_port(gid, hid, ip, port)
            if not check_ins:
                mi = McInstance(gid, hid, ip, port, mem, thread, con, factor, para, role, status, muser, ver, remark)
                aservice.add(mi)
                flash(u"Add Success!", 'info')
                return redirect(url_for('.instances'))
            else:
                flash(u'该实例已存在，请重新填写！', 'warning')
    return render_template('asset/add_instance.html', form=form, gtype=gtype)


@asset.route('/i/add_redis/', methods=['GET', 'POST'])
def add_redis_instance():
    aservice = AssetService()
    gtype = aservice.get_gtype_by_type_name("REDIS")
    group_names = [(g.id, g.name) for g in aservice.get_group_by_type(gtype.id)]
    form = RedisForm(request.form)
    form.i_base.i_role.choices = [(0, 'StandAlone'), (1, 'Master'), (2, 'Slave')]
    form.i_base.i_name.choices = group_names
    if request.method == 'POST' and form.validate():
        gid = form.i_base.i_name.data
        ver = form.i_base.i_version.data
        host = form.i_base.i_hostname.data
        ip = form.i_base.i_ip.data
        port = form.i_base.i_port.data
        role = form.i_base.i_role.data
        status = form.i_base.i_status.data
        remark = form.i_base.i_remark.data
        mem = form.r_mem.data
        pre = form.r_pre.data

        r_hid = aservice.get_hid_by_name(host)
        if not r_hid:
            flash(u'该机器名不存在，请重新填写！', 'warning')
        else:
            hid = r_hid[0]

            check_ins = aservice.find_redis_instance_by_name_and_ip_and_port(gid, hid, ip, port)
            if not check_ins:
                mi = RedisInstance(gid, hid, ip, port, mem, pre, role, status, ver, remark)
                aservice.add(mi)
                flash(u"Add Success!", 'info')
                return redirect(url_for('.instances'))
            else:
                flash(u'该实例已存在，请重新填写！', 'warning')
    return render_template('asset/add_instance.html', form=form, gtype=gtype)