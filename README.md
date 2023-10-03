# Network Automation Konfigurasi Cluster Ceph

Requirement :
1. Install Python Latest
2. Install PIP
3. Install Django
4. Install virtualenv (optional)
5. install mysqlclient

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
3. dont forget create database with the name 'network_automation'
4. python manage.py migrate
5. puthon manage.py makemigrations
6. table is automatically created in PHPmyadmin if used xampp

