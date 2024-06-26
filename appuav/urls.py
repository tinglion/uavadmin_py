"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.urls import include, path, re_path

# from drf_spectacular import openapi
# from drf_spectacular.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from appuav import dispatch, settings
from uavadmin.system.views.dictionary import InitDictionaryViewSet
from uavadmin.system.views.login import (
    ApiLogin,
    CaptchaView,
    LoginTokenView,
    LoginView,
    LogoutView,
)
from uavadmin.system.views.system_config import InitSettingsViewSet
from uavadmin.utils.swagger import CustomOpenAPISchemaGenerator

# from rest_framework.authentication import BasicAuthentication


# =========== 初始化系统配置 =================
dispatch.init_system_config()
dispatch.init_dictionary()
# =========== 初始化系统配置 =================

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # generator_class=CustomOpenAPISchemaGenerator,
    # authentication_classes=(JWTAuthentication,)
)

urlpatterns = (
    [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            r"redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        path("api/system/", include("uavadmin.system.urls")),
        path("api/login/", LoginView.as_view(), name="token_obtain_pair"),
        path("api/logout/", LogoutView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        re_path(
            r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")
        ),
        path("api/captcha/", CaptchaView.as_view()),
        path("api/init/dictionary/", InitDictionaryViewSet.as_view()),
        path("api/init/settings/", InitSettingsViewSet.as_view()),
        path("apiLogin/", ApiLogin.as_view()),
        # 仅用于开发，上线需关闭
        path("api/token/", LoginTokenView.as_view()),
        # 数据集
        path("api/dataset/", include("uavadmin.dataset.urls")),
        # UAV
        path("api/uav/", include("uavadmin.uav.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    + [
        re_path(ele.get("re_path"), include(ele.get("include")))
        for ele in settings.PLUGINS_URL_PATTERNS
    ]
)
