from django.db import models
from django.utils import timezone

class File(models.Model):
    name = models.CharField(max_length=255)  # Название файла
    file_type = models.CharField(max_length=50)  # Тип файла (png, jpg, docx и т.д.)
    path = models.FileField(upload_to='uploads/')  # Путь к файлу в папке 'uploads/'
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время добавления
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время изменения
    url = models.URLField(max_length=200, blank=True, null=True)  # Ссылка на файл

    def __str__(self):
        return self.name
