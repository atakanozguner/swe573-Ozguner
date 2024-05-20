"""
URL configuration for swe573project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from swe573app.views import (
    homepage,
    register,
    user_login,
    user_logout,
    communities,
    create_community,
    community_detail,
    follow_community,
    edit_description,
    make_moderator,
    remove_moderator,
    delete_community,
    activate_community,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="homepage"),
    path("register", register, name="register"),
    path("user_login", user_login, name="user_login"),
    path("user_logout", user_logout, name="user_logout"),
    path("communities", communities, name="communities"),
    path("communities/create", create_community, name="create_community"),
    path("communities/<int:community_id>/", community_detail, name="community_detail"),
    path(
        "communities/<int:community_id>/follow",
        follow_community,
        name="follow_community",
    ),
    path(
        "communities/<int:community_id>/edit_description/",
        edit_description,
        name="edit_description",
    ),
    path(
        "communities/<int:community_id>/make_moderator/<int:user_id>/",
        make_moderator,
        name="make_moderator",
    ),
    path(
        "communities/<int:community_id>/remove_moderator/<int:user_id>/",
        remove_moderator,
        name="remove_moderator",
    ),
    path(
        "communities/<int:community_id>/delete/",
        delete_community,
        name="delete_community",
    ),
    path(
        "community/<int:community_id>/activate/",
        activate_community,
        name="activate_community",
    ),
]
