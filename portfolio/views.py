from django.shortcuts import render

from myportfolio import settings


def home(request):
    context = {
        "profile_image_path": settings.PROFILE_IMAGE_PATH
    }
    return render(request, 'portfolio/home.html', context)

def technology(request):
    context = {
        "python_image_path": settings.PYTHON_IMAGE_PATH,
        "selenium_image_path": settings.SELENIUM_IMAGE_PATH,
        "powerautomate_image_path": settings.POWERAUTOMATE_IMAGE_PATH,
        "uipath_image_path": settings.UIPATH_IMAGE_PATH,
        "powerplatform_image_path": settings.POWERPLATFORM_IMAGE_PATH,
        "genai_image_path": settings.GENAI_IMAGE_PATH,
        "langchain_image_path": settings.LANGCHAIN_IMAGE_PATH,
        "bert_image_path": settings.BERT_IMAGE_PATH,
        "django_image_path": settings.DJANGO_IMAGE_PATH,
        "flask_image_path": settings.FLASK_IMAGE_PATH,
        "html_image_path": settings.HTML_IMAGE_PATH,
        "tailwind_image_path": settings.TAILWIND_IMAGE_PATH,
        "git_image_path": settings.GIT_IMAGE_PATH,
        "github_image_path": settings.GITHUB_IMAGE_PATH,
        "linux_image_path": settings.LINUX_IMAGE_PATH,
        "windows_image_path": settings.WINDOWS_IMAGE_PATH,
        "docker_image_path": settings.DOCKER_IMAGE_PATH,
        "kubernetes_image_path": settings.KUBERNETES_IMAGE_PATH,
        "jenkins_image_path": settings.JENKINS_IMAGE_PATH,
        "devops_image_path": settings.DEVOPS_IMAGE_PATH,
        "pandas_image_path": settings.PANDAS_IMAGE_PATH,
        "numpy_image_path": settings.NUMPY_IMAGE_PATH,
        "threading_image_path": settings.THREADING_IMAGE_PATH,
        "multiprocessing_image_path": settings.MULTIPROCESSING_IMAGE_PATH,
        "beautifulsoup_image_path": settings.BEAUTIFULSOUP_IMAGE_PATH,
        "tensorflow_image_path": settings.TENSORFLOW_IMAGE_PATH,
        "pillow_image_path": settings.PILLOW_IMAGE_PATH,
        "poppler_image_path": settings.POPPLER_IMAGE_PATH,
        "fitz_image_path": settings.FITZ_IMAGE_PATH,
        "postman_image_path": settings.POSTMAN_IMAGE_PATH
    }
    return render(request, 'portfolio/technology.html',context)

def projects(request):
    return render(request, 'portfolio/projects.html')

def contact(request):
    context = {
        "rpa_resume_path": settings.RPA_RESUME_PATH,
        "qa_resume_path": settings.QA_RESUME_PATH
    }
    return render(request, 'portfolio/contact.html',context)
