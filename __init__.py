# -*- coding: utf-8 -*-
'''
Created on 2017. 6. 26.
@author: HyechurnJang
'''

import requests
from page import *

admin = PAGE()

@PAGE.MAIN(admin, 'Admin')
def admin_page_main(req):
    
    return DIV().html(
        HEAD(2).html('Installed Modules'),
        admin.patch('install_module_view'),
        HEAD(2).html('Pygics Applications'),
        admin.patch('repo_app_view'),
        HEAD(2).html('Pygics Experimental'),
        admin.patch('repo_exp_view')
    )

@PAGE.VIEW(admin)
def install_module_view(req, name=None):
    if name != None:
        ENV.MOD.uninstall(name)
        return DIV().html(
            admin.table(
                TABLE.SYNC('Name', 'Base', 'Distribution', 'Path', 'Dependency', 'Start Time', 'Action'),
                'install_module_table'
            ),
            admin.refresh('repo_app_view'),
            admin.refresh('repo_exp_view')
        )
    else:
        return admin.table(
            TABLE.SYNC('Name', 'Base', 'Distribution', 'Path', 'Dependency', 'Start Time'),
            'install_module_table'
        )
    
@PAGE.TABLE(admin)
def install_module_table(table):
    descs = ENV.MOD.DESC
    for desc in descs.values():
        table.record(desc['name'], desc['base'], desc['dist'], desc['path'], ','.join(desc['deps']), desc['time'], ' ')

@PAGE.VIEW(admin)
def repo_app_view(req, path=None):
    ret = DIV().html(
        admin.table(
            TABLE.SYNC('Name', 'Description'),
            'repo_app_table'
        )
    )
    if path != None:
        ENV.MOD.install(path)
        ret.html(admin.refresh('install_module_view'))
    return ret

@PAGE.TABLE(admin)
def repo_app_table(table):
    app = requests.get('https://api.github.com/users/pygics-app/repos')
    if app.status_code == 200:
        repos = app.json()
        for repo in repos:
            if repo['name'] not in ENV.MOD.PRIO:
                table.record(DIV().html(
                                DIV(STYLE='float:left;').html(
                                    admin.trigger(
                                         BUTTON(CLASS='btn-success btn-xs', STYLE='margin:0px;padding:0px 5px;width:60px;font-size:11px;').html('Install'),
                                        'repo_app_view', 'app::' + repo['name'])),
                                SPAN(STYLE='float:left;margin-left:5px;').html(repo['name'])
                             ),
                             repo['description'])
            else:
                table.record(DIV().html(
                                DIV(STYLE='float:left;').html(
                                    admin.trigger(
                                        BUTTON(CLASS='btn-danger btn-xs', STYLE='margin:0px;padding:0px 5px;width:60px;font-size:11px;').html('Uninstall'),
                                        'install_module_view', repo['name'])),
                                SPAN(STYLE='flow:left;margin-left:5px;').html(repo['name'])
                             ),
                             repo['description'], ' ')

@PAGE.VIEW(admin)
def repo_exp_view(req, path=None):
    ret = DIV().html(
        admin.table(
            TABLE.SYNC('Name', 'Description'),
            'repo_exp_table'
        )
    )
    if path != None:
        ENV.MOD.install(path)
        ret.html(admin.refresh('install_module_view'))
    return ret

@PAGE.TABLE(admin)
def repo_exp_table(table):
    exp = requests.get('https://api.github.com/users/pygics-app-exp/repos')
    if exp.status_code == 200:
        repos = exp.json()
        for repo in repos:
            if repo['name'] not in ENV.MOD.PRIO:
                table.record(DIV().html(
                                DIV(STYLE='float:left;').html(
                                     admin.trigger(
                                         BUTTON(CLASS='btn-success btn-xs', STYLE='margin:0px;padding:0px 5px;width:60px;font-size:11px;').html('Install'),
                                        'repo_exp_view', 'exp::' + repo['name'])),
                                SPAN(STYLE='float:left;margin-left:5px;').html(repo['name'])
                             ),
                             repo['description'])
            else:
                table.record(DIV().html(
                                DIV(STYLE='float:left;').html(
                                    admin.trigger(
                                        BUTTON(CLASS='btn-danger btn-xs', STYLE='margin:0px;padding:0px 5px;width:60px;font-size:11px;').html('Uninstall'),
                                        'install_module_view', repo['name'])),
                                SPAN(STYLE='flow:left;margin-left:5px;').html(repo['name'])
                             ),
                             repo['description'], ' ')
