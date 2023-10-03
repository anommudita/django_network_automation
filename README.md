# Network Automation Konfigurasi Cluster Ceph

Requirement :
1. Install Python Latest Version
2. Install PIP
3. Install Django
```bash
  pip install django
```
4. Install virtualenv (optional)
```bash
  virtualenv env
```
5. install mysqlclient
```bash
  pip install mysqlclient
```

Steps :
1. folder config/settings.py , follow the method below :
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'network_automation',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
3. dont forget create database with the name `network_automation` on PHPMYADMIN
4. migrate database
```bash
  python manage.py migrate
```
5. table is automatically created in PHPmyadmin

