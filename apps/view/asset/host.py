#! -*- coding: utf8 -*-
import json

from flask import render_template, request, flash, redirect, url_for
from apps.view.asset import asset
from apps.service.asset_service import AssetService
from apps.model.asset.forms import HAWForm, HAHForm, HForm
from apps.model.asset.host import Host


@asset.route('/h/')
def hosts():
    aservice = AssetService()
    all_hosts = aservice.find_all_host_name_and_ip()
    return render_template('asset/host_info.html', all_hosts=all_hosts)


@asset.route('/h/add_host_wizard/welcome/')
def host_add_welcome():
    aservice = AssetService()
    hawform = HAWForm()
    hawform.haw_type.choices = [(gtype.id, gtype.type) for gtype in aservice.get_all_gtypes()]
    return render_template('asset/host_add_welcome.html', form=hawform)


@asset.route('/h/add_host_wizard/hosts/', methods=['POST'])
def host_add_ip():
    tid = request.data
    aservice = AssetService()
    hahform = HAHForm()
    return render_template('asset/host_add_ip.html', form=hahform)


@asset.route('/h/add/', methods=['GET', 'POST'])
def add_host():
    form = HForm(request.form)
    aservice = AssetService()
    if request.method == 'POST' and form.validate():
        name = form.h_name.data
        core = form.h_core.data
        mem = form.h_memory.data
        dtype = form.h_disk_type.data
        dnum = form.h_disk_num.data
        dsize = form.h_disk_size.data
        eth = form.h_eth.data
        ip = form.h_ip.data
        remote_ip = form.h_remote_ip.data
        idc = form.h_idc.data
        rack = form.h_rack.data
        brf = form.h_brf.data
        brt = form.h_brt.data
        status = form.h_status.data
        remark = form.h_remark.data

        if not brt:
            brt = '1000-01-01 00:00:00'
        disk = json.dumps(((dtype, dnum, dsize),))
        if name != '' and ip != '':
            is_exist = aservice.find_host_by_name_and_ip(name, ip)
            if not is_exist:
                host = Host(name, core, mem, disk, eth, ip, '', remote_ip, idc, rack, brf, brt, status, remark)
                aservice.add(host)
                flash(u"Add Success!", 'info')
                return redirect(url_for('.hosts'))
            else:
                flash(u'该机器名或ip已存在，请修改后再输入！', 'warning')
        else:
            flash(u'请填写机器名和ip！', 'warning')
    return render_template('asset/add_host.html', form=form)

