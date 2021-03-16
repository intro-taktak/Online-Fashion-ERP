from django.db import models
from uuid import uuid4
from django.utils import timezone


def upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 결합 후 return
    return '/'.join([ymd_path + '/' + uuid_name, filename, ])


class RegisteredPrograms(models.Model):
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=400)
    progress = models.CharField(max_length=100)
    rating = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    content = models.TextField()
    manual = models.TextField()
    writer = models.CharField(max_length=100)
    parent_id = models.CharField(max_length=100)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class Menus(models.Model):
    m_id = models.CharField(max_length=300)
    parent = models.CharField(max_length=500)
    menu_name = models.CharField(max_length=400)
    parent_url = models.CharField(max_length=200)


class Files(models.Model):
    board = models.CharField(max_length=300)
    p_id = models.CharField(max_length=300)
    file = models.FileField(upload_to=upload_to)


class RegisteredProgramsCheckIns(models.Model):
    p_id = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    writer = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)


class RegistereddevNotice(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    writer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class devNoticeCheckIns(models.Model):
    p_id = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    writer = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100)
