#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# author: antonio hinojo

from fabric.api import sudo
from fabric.api import cd
from fabric.api import run
from fabric.api import env
from fabric.contrib.files import upload_template
from fabric.contrib.files import exists


def install(conf_folder):
    sudo("apt-get -y install nginx")


def copy_conf_files(conf_folder, deploy_folder):
    with cd(deploy_folder):
        run('mkdir -p nginx')

        upload_template('%s/nginx/host_conf' % conf_folder,\
            'nginx', context=env)
        upload_template('%s/nginx/nginx.conf' % conf_folder,\
            'nginx', context=env)
        upload_template('%s/nginx/proxy.conf' % conf_folder,\
            'nginx', context=env)
        upload_template('%s/apache/apache_with_nginx' % conf_folder,\
            'apache2', context=env)

        #nginx stuff
        #if exists('/etc/nginx/nginx.conf'):
        #    sudo('rm -vf /etc/nginx/nginx.conf')

        #if exists('/etc/nginx/proxy.conf'):
        #    sudo('rm -vf /etc/nginx/proxy.conf')

        sudo('cp nginx/nginx.conf /etc/nginx/nginx.conf')
        sudo('cp nginx/proxy.conf /etc/nginx/proxy.conf')

        sudo('cp nginx/host_conf /etc/nginx/sites-enabled/%(host)s' % env)
        sudo('chmod a+r /etc/nginx/sites-enabled/%(host)s' % env)

        if not exists('/etc/nginx/sites-available/%(host)s' % env):
            sudo(\
            'ln -fs /etc/nginx/sites-enabled/%(host)s'\
            ' /etc/nginx/sites-available/%(host)s' % env)

        #apache stuff
        sudo('cp apache2/apache_with_nginx'\
            ' /etc/apache2/sites-available/%(host)s' % env)
        sudo('chmod a+r /etc/apache2/sites-available/%(host)s' % env)
        if not exists('/etc/apache2/sites-enabled/00-%(host)s' % env):
            sudo('ln -s /etc/apache2/sites-available/%(host)s'\
                ' /etc/apache2/sites-enabled/00-%(host)s' % env)


def start():
    sudo("/etc/init.d/nginx start")


def stop():
    sudo("/etc/init.d/nginx stop")


def restart():
    sudo("/etc/init.d/nginx restart")
