from fabric.api import cd, env, put, sudo, task


env.use_ssh_config = True


@task
def bootstrap():
    web_root = '/var/www/'
    sudo('apt-get update')
    sudo('apt-get install nginx git php5-fpm php5-gd')
    sudo('mkdir -p {}'.format(web_root))
    sudo('chown mccutchen:www-data {}'.format(web_root))
    configure_nginx()
    configure_php()
    restart_nginx()


@task
def configure_nginx():
    with cd('/etc/nginx/sites-available'):
        run('rm -f default')
        put('nginx/sites-available/*', '.')
    with cd('/etc/nginx/sites-enabled'):
        run('rm -f default')
        sudo('ln -s ../sites-available/* .')


@task
def configure_php():
    # php configuration tweaks come from here:
    # https://www.digitalocean.com/community/articles/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-12-04 # noqa
    with cd('/etc/php5/fpm'):
        put('php/php.ini', '.', use_sudo=True)
        put('php/www.conf', 'pool.d/', use_sudo=True)


@task
def restart_nginx():
    sudo('service nginx restart')
