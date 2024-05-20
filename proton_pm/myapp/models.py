from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    file = models.FileField(upload_to='upldfile/')
    unique_url = models.CharField(max_length=6, unique=True, blank=True, null=True)
    file_extension = models.CharField(max_length=10, blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'files'

    def __str__(self):
        return f"File: {self.file_extension}"


class Terminal(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'terminals'

    def __str__(self):
        return self.name

class Actions(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=255)

    class Meta:
        db_table = 'actions'

    def __str__(self):
        return self.name

class Terminal_status(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=255)

    class Meta:
        db_table = 'terminal_status'

    def __str__(self):
        return self.name


class Role(models.Model):
    display_name = models.CharField(max_length=255)
    role_id = models.IntegerField(unique=True)  # Переименуйте поле
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return f"Role: {self.display_name} (ID: {self.role_id})"


from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childrens')

    # Добавляем поля для хранения ссылок на изображения
    image1 = models.ImageField(upload_to='upldfile', blank=True, null=True)
    image2 = models.ImageField(upload_to='upldfile', blank=True, null=True)
    image3 = models.ImageField(upload_to='upldfile', blank=True, null=True)

    # Уникальный URL

    class Meta:
        db_table = 'content'

    def __str__(self):
        return self.title




from django.db import models
from django.contrib.auth.models import User
from .models import Content

class ContentChild(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Content, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class AccessToContent(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    actions = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'access_to_content'
        constraints = [
            models.UniqueConstraint(fields=['content', 'role'], name='unique_content_role')
        ]

    def __str__(self):
        return f"Access to {self.content} for role {self.role}: {self.actions}"


class Publication(models.Model):
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        db_table = 'publication'

    def __str__(self):
        return f"Publication in terminal {self.terminal} with content {self.content} and file {self.file}"


