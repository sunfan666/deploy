"""restfuldemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from rest_framework.documentation import include_docs_urls
# from rest_framework.authtoken import views

from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from books.views import PublishViewSet, AuthorViewSet, BookViewSet
from users.router import users_router
from workorder.router import workorder_router
from autotask.router import task_router
from release.router import deploy_router


router = DefaultRouter()
router.registry.extend(users_router.registry)
router.registry.extend(workorder_router.registry)
router.registry.extend(task_router.registry)
router.registry.extend(deploy_router.registry)

router.register(r'publish', PublishViewSet, base_name='publish')
router.register(r'author', AuthorViewSet, base_name='author')
router.register(r'book', BookViewSet, base_name='book')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title="图书管理系统")),
    url('^projects/', include('projects.urls', namespace='projects')),
    url(r'^login/', obtain_jwt_token),
    url(r'^jwt-refresh/', refresh_jwt_token),
    # url(r'^api-token-auth/', views.obtain_auth_token),     # drf 自定义token认证
]

