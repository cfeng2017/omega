#! -*- coding: utf8 -*-
from flask import render_template, request, flash, jsonify, redirect, url_for

from apps.service.asset_service import AssetService
from apps.model.asset.forms import GTForm, GDbForm, GForm
from apps.model.asset.group_type import GroupType
from apps.model.asset.group import Group
from apps.model.asset.group_db import GroupDb
from apps.view.asset import asset
from apps.view.asset import MYSQL_TYPE_ID


@asset.route('/g/')
def groups():
    aservice = AssetService()
    gtypes = aservice.get_all_gtypes()
    dbs = aservice.get_all_gdbs()
    groups = aservice.get_group_by_type(MYSQL_TYPE_ID)             # Display mysql groups by default.
    return render_template('asset/group_info.html', gtypes=gtypes, dbs=dbs, groups=groups)


@asset.route('/gtype/add/', methods=['GET', 'POST'])
def gtype_add():
    form = GTForm(request.form)
    aservice = AssetService()
    egs = aservice.get_all_gtypes()
    if request.method == 'POST' and form.validate():
        gtype = form.gt_gtname.data.upper()
        if not aservice.get_gtype_by_type_name(gtype):
            gt = GroupType(gtype)
            aservice.add(gt)
            egs.append(gtype)
            flash(u"Add Success!", 'info')
            return redirect(url_for('.groups'))
        else:
            flash('该类型已存在！', 'warning')
    return render_template('asset/add_gtype.html', form=form, egs=egs)


@asset.route('/gdb/add/', methods=['GET', 'POST'])
def gdb_add():
    form = GDbForm(request.form)
    gtype_choices = [(gt.id, gt.type) for gt in AssetService.get_all_gtypes()]
    form.gdb_gname.gtype.gtype.choices = gtype_choices
    if not gtype_choices:
        gname_choices = []
    else:
        gname_choices = [(mg.id, mg.name) for mg in AssetService.get_group_by_type(gtype_choices[0][0])]
    form.gdb_gname.gname.choices = gname_choices
    if request.method == 'POST':
        aservice = AssetService()
        gid = form.data['gdb_gname']['gname']
        db_name = form.data['gdb_db']
        if not db_name:
            flash(u'db名必须填空！', 'warning')
            return render_template('asset/add_gdb.html', form=form)
        elif len(db_name)>30:
            flash(u'db名不能超过30个字符长度！', 'warning')
            return render_template('asset/add_gdb.html', form=form)

        if not aservice.get_db_by_gid_and_name(gid, db_name):
            gdb = GroupDb(gid, db_name)
            aservice.add(gdb)
            flash(u"Add Success!", 'info')
            return redirect(url_for('.groups'))
        else:
            flash('同类型组中该DB名已存在！请更换DB名！', 'warning')
    return render_template('asset/add_gdb.html', form=form)


@asset.route('/g/add/', methods=['GET', 'POST'])
def group_add():
    form = GForm(request.form)
    form.g_gtype.gtype.choices = [(gt.id, gt.type) for gt in AssetService.get_all_gtypes()]
    if request.method == 'POST' and form.validate():
        aservice = AssetService()
        gname = form.g_name.data
        gtype = form.g_gtype.data['gtype']
        des = form.g_des.data
        scenario = form.g_scenario.data
        contacts = form.g_contacts.data
        group = Group(gname, gtype, des, scenario, contacts)
        if not aservice.get_group_by_type_and_name(gtype, gname):
            aservice.add(group)
            flash(u"Add Success!", 'info')
            return redirect(url_for('.groups'))
        else:
            flash('同类型中该组名已存在！请更换组名！', 'warning')
    return render_template('asset/add_group.html', form=form)


@asset.route('/g/get_group_by_type/', methods=['GET'])
def get_group_by_type():
    aservice = AssetService()
    tid = request.args.get('tid', MYSQL_TYPE_ID, type=int)                       # Default group type is Mysql
    groups = [group.to_json() for group in aservice.get_group_by_type(tid)]
    return jsonify(groups=groups)


