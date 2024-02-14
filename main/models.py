from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    pwd = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Определение класса Category перед использованием в File_Upload
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class File_Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    # Сделать поле category допускающим null временно для миграции
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='files', null=True)
    file_field = models.FileField(upload_to="")

    def __str__(self):
        return self.title

class File(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    # Другие поля по необходимости

    def get_icon_class(self):
        extension = self.file.name.split('.')[-1].lower()
        if extension in ['pdf']:
            return 'fas fa-file-pdf'
        elif extension in ['doc', 'docx']:
            return 'fas fa-file-word'
        elif extension in ['jpg', 'jpeg', 'png', 'gif']:
            return 'fas fa-file-image'
        elif extension in ['mp4', 'avi']:
            return 'fas fa-file-video'
        # Добавьте другие условия для разных типов файлов
        else:
            return 'fas fa-file'
