from django.shortcuts import render, redirect
from .models import User, File_Upload, Category
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request):
    all_files = File_Upload.objects.all().order_by('-id')
    paginator = Paginator(all_files, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})

def login(request):
    if 'user' not in request.session:
        if request.method == 'POST':
            email = request.POST['email']
            pwd = request.POST['pwd']
            userExists = User.objects.filter(email=email, pwd=pwd)
            if userExists.exists():
                request.session["user"] = email
                return redirect('index')
            else:
                messages.warning(request, "Wrong user or details.")
        return render(request, 'login.html')
    else:
        return redirect('index')

def logout(request):
    del request.session['user']
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        pwd = request.POST['pwd']
        gender = request.POST['gender']
        if not User.objects.filter(email=email).exists():
            create_user = User.objects.create(name=name, email=email, pwd=pwd, gender=gender)
            create_user.save()
            messages.success(request, "Your account is created successfully!")
            return redirect('login')
        else:
            messages.warning(request, "Email is already registered!")
    return render(request, 'signup.html')

@login_required
def file_upload(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Только администратор может загружать файлы")

    if request.method == 'POST':
        title_name = request.POST['title']
        description_name = request.POST['description']
        file_name = request.FILES['file_to_upload']
        category_id = request.POST.get('category', None)

        category_obj = None
        if category_id:
            category_obj = Category.objects.get(id=category_id)

        new_file = File_Upload.objects.create(
            user=request.user,
            title=title_name,
            description=description_name,
            file_field=file_name,
            category=category_obj
        )
        messages.success(request, "File is uploaded successfully!")
        new_file.save()

    categories = Category.objects.all()
    return render(request, 'file_upload.html', {'categories': categories})

def settings(request):
    if 'user' in request.session:
        user_obj = User.objects.get(email=request.session['user'])
        user_files = File_Upload.objects.filter(user=user_obj)

        img_list, audio_list, videos_list, pdfs_list = [], [], [], []

        for file in user_files:
            if str(file.file_field)[-3:] == 'mp3':
                audio_list.append(file)
            elif str(file.file_field)[-3:] in ['mp4', 'mkv']:
                videos_list.append(file)
            elif str(file.file_field)[-3:] in ['jpg', 'png', 'jpeg']:
                img_list.append(file)
            elif str(file.file_field)[-3:] == 'pdf':
                pdfs_list.append(file)

        data = {
            'user_files': user_files,
            'videos': len(videos_list),
            'audios': len(audio_list),
            'images': len(img_list),
            'pdf': len(pdfs_list),
            'img_list': img_list,
            'audio_list': audio_list,
            'videos_list': videos_list,
            'pdfs_list': pdfs_list
        }
        return render(request, 'settings.html', data)

def delete_file(request, id):
    if 'user' in request.session:
        file_obj = File_Upload.objects.get(id=id)
        file_obj.delete()
        return redirect('settings')
    else:
        return redirect('login')

def get_file_icon(file_path):
    file_icons = {
        'pdf': 'fa-file-pdf',
        'docx': 'fa-file-word',
        'doc': 'fa-file-word',
        'ppt': 'fa-file-powerpoint',
        'pptx': 'fa-file-powerpoint',
        'xls': 'fa-file-excel',
        'xlsx': 'fa-file-excel',
        'txt': 'fa-file-alt',
        'mp3': 'fa-file-audio',
        'mp4': 'fa-file-video',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'png': 'fa-file-image',
        'gif': 'fa-file-image',
        'csv': 'fa-file-csv',
        'zip': 'fa-file-archive',
        'rar': 'fa-file-archive',
        '7z': 'fa-file-archive',
        'html': 'fa-file-code',
        'js': 'fa-file-code',
        'css': 'fa-file-code',
        'json': 'fa-file-code',
        # Добавьте другие типы файлов и их иконки по необходимости
    }
    extension = file_path.split('.')[-1].lower()  # Получаем расширение файла
    return file_icons.get(extension, 'fa-file')  # Возвращаем класс иконки или стандартный, если не найден
