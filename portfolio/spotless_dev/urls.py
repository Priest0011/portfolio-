from django.urls import path
from . import views

urlpatterns = [
    # Public
    path("", views.home, name="home"),
    path("projects/", views.all_projects, name="projects"),

    # Auth
    path("admin_dashboard/login/", views.admin_login, name="admin_login"),
    path("admin_dashboard/logout/", views.admin_logout, name="admin_logout"),
    path("admin_dashboard/password/", views.admin_change_password, name="admin_change_password"),

    # Dashboard
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Projects
    path("admin_dashboard/projects/", views.admin_project_list, name="admin_project_list"),
    path("admin_dashboard/projects/add/", views.admin_project_add, name="admin_project_add"),
    path("admin_dashboard/projects/<int:pk>/edit/", views.admin_project_edit, name="admin_project_edit"),
    path("admin_dashboard/projects/<int:pk>/delete/", views.admin_project_delete, name="admin_project_delete"),

    # Skills (url name 'skill' kept so existing links don't break)
    path("admin_dashboard/skills/", views.admin_skill_list, name="skill"),
    path("admin_dashboard/skills/add/", views.admin_skill_add, name="admin_skill_add"),
    path("admin_dashboard/skills/<int:pk>/edit/", views.admin_skill_edit, name="admin_skill_edit"),
    path("admin_dashboard/skills/<int:pk>/delete/", views.admin_skill_delete, name="admin_skill_delete"),

    # Blog (url name 'blog' kept)
    path("admin_dashboard/blog/", views.admin_blog_list, name="blog"),
    path("admin_dashboard/blog/add/", views.admin_blog_add, name="admin_blog_add"),
    path("admin_dashboard/blog/<int:pk>/edit/", views.admin_blog_edit, name="admin_blog_edit"),
    path("admin_dashboard/blog/<int:pk>/delete/", views.admin_blog_delete, name="admin_blog_delete"),

    # About
    path("admin_dashboard/about/", views.admin_about_list, name="admin_about_list"),
    path("admin_dashboard/about/add/", views.admin_about_add, name="admin_about_add"),
    path("admin_dashboard/about/<int:pk>/edit/", views.admin_about_edit, name="admin_about_edit"),
    path("admin_dashboard/about/<int:pk>/delete/", views.admin_about_delete, name="admin_about_delete"),

    # Messages
    path("admin_dashboard/messages/", views.admin_message_list, name="admin_message_list"),
    path("admin_dashboard/messages/<int:pk>/", views.admin_message_detail, name="admin_message_detail"),
    path("admin_dashboard/messages/<int:pk>/delete/", views.admin_message_delete, name="admin_message_delete"),
]