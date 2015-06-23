from fabric.api import cd, env, prompt, put, run, sudo, task


env.use_ssh_config = True


@task
def install_packages():
    packages = [
        'nginx',
        'git',
        'python-dev',
        'python-pip',
        'python-virtualenv',
        'php5-fpm',
        'php5-gd'
    ]
    sudo('apt-get install -y %s' % ' '.join(packages))


@task
def bootstrap():
    update_os(restart_nginx=False)
    install_packages()

    login = 'mccutchen'
    add_user(login)

    web_root = '/var/www/'
    run('mkdir -p {}'.format(web_root))
    run('chown {}:www-data {}'.format(login, web_root))

    configure_nginx()
    configure_php()
    restart_nginx()


@task
def add_user(login):
    password = prompt('Password for user {}@{}?'.format(login, env.host))
    run('adduser --disabled-password --gecos "" {}'.format(login))
    run('echo "{}:{}" | chpasswd'.format(login, password))
    run('echo "{}\tALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers'.format(login))
    # the following assumes a key was added to this instance when created
    ssh_dir = '/home/{}/.ssh'.format(login)
    run('mkdir -p {}'.format(ssh_dir))
    run('cp ~/.ssh/authorized_keys {}'.format(ssh_dir))


@task
def configure_nginx():
    sudo('rm -f /etc/nginx/sites-available/default')
    put('nginx/sites-available/*', '/etc/nginx/sites-available', use_sudo=True)
    with cd('/etc/nginx/sites-enabled'):
        sudo('rm -f default')
        sudo('ln -sf ../sites-available/* .')


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


@task
def update_os():
    sudo('apt-get update && apt-get -y upgrade')
