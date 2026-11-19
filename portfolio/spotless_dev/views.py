from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .models import Project, Skill, About, Blog, Contact
from .forms import ContactForm
from django.conf import settings
from django.core.paginator import Paginator

def home(request):
    projects = Project.objects.all()
    skills = Skill.objects.all()
    blogs = Blog.objects.order_by('-created_at')[:3]
    abouts = About.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message to the database
            contact = form.save()

            # Prepare HTML email
            subject = f"New message from {contact.name}"
            html_message = f"""
                <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #4CAF50;">📩 New Contact Message</h2>
                    
                    <p><strong>Name:</strong> {contact.name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{contact.email}" style="color: #4CAF50;">{contact.email}</a></p>
                    
                    <p><strong>Message:</strong></p>
                    <div style="margin-left: 20px; padding: 10px; background: #f9f9f9; border-left: 4px solid #4CAF50;">
                        {contact.message}
                    </div>
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    
                    <p style="font-size: 0.9em; color: #777;">
                        You received this message from your portfolio contact form.<br>
                        Sent at: {contact.sent_at.strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                    
                    <p style="font-size: 0.85em; color: #aaa; margin-top: 40px;">
                        <strong>Spotless Dev Portfolio</strong><br>
                        <a href="mailto:{contact.email}" style="color: #4CAF50;">Reply to {contact.email}</a>
                        <p><strong>WhatsApp:</strong> <a href="https://wa.me/{contact.phone_number}" style="color: #4CAF50;">Chat on WhatsApp</a></p>
                    </p>
                </div>
            """

            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['kingsleyspotless44@gmail.com']

            try:
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    to_email,
                    html_message=html_message,
                    fail_silently=False
                )
                messages.success(request, "Your message has been sent successfully.")
            except Exception as e:
                print("Email sending error:", e)
                messages.error(request, "Message saved, but failed to send email.")
            
            return redirect('home')
        else:
            messages.error(request, "There was an error. Please check the form.")
    else:
        form = ContactForm()

    return render(request, 'portfolio.html', {
        'projects': projects,
        'blogs': blogs,
        'abouts': abouts,
        'form': form,
        'skills': skills,
    })

def all_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    paginator = Paginator(projects, 8)  # 6 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'all_project.html',
    context={
        'projects': projects,
        'page_obj': page_obj,
    })
    
# Put this in your views.py BELOW the public views (home, all_projects).
# DELETE the old admin_dashboard, admin_blog, admin_project_*, admin_skill_list,
# admin_login, admin_logout and admin_about_list functions — they are all replaced here.

import re

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .decorators import admin_required
from .forms import AboutForm, BlogForm, ProjectForm, SkillForm
from .models import About, Blog, Contact, Project, Skill


# ───────────────────────── helpers ─────────────────────────

def _sidebar_counts():
    """Counts shown in the sidebar on every admin page."""
    return {
        "total_projects": Project.objects.count(),
        "total_skills": Skill.objects.count(),
        "total_blogs": Blog.objects.count(),
        "total_about": About.objects.count(),
        "total_contacts": Contact.objects.count(),
    }


def _paginate(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(request.GET.get("page"))
    return {
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
    }


def _form_view(request, form_class, *, instance=None, title, subtitle,
               success_msg, redirect_to, back_label, active):
    """One add/edit view for every model."""
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, success_msg)
            return redirect(redirect_to)
    else:
        form = form_class(instance=instance)

    context = {
        "form": form,
        "object": instance,
        "title": title,
        "subtitle": subtitle,
        "back_url": redirect_to,
        "back_label": back_label,
        "active": active,
        **_sidebar_counts(),
    }
    return render(request, "admin/admin_form.html", context)


def _delete_view(request, obj, *, object_type, label, success_msg, redirect_to, active):
    """One delete-confirmation view for every model."""
    if request.method == "POST":
        obj.delete()
        messages.success(request, success_msg)
        return redirect(redirect_to)

    context = {
        "object_type": object_type,
        "label": label,
        "cancel_url": redirect_to,
        "active": active,
        **_sidebar_counts(),
    }
    return render(request, "admin/admin_confirm_delete.html", context)


# ───────────────────────── auth ─────────────────────────

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    next_url = request.POST.get("next") or request.GET.get("next") or ""
    # Block open-redirects (?next=https://evil.com)
    if not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        next_url = "admin_dashboard"

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect(next_url)
            messages.error(request, "This account doesn't have admin access.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "admin/admin_login.html", {"form": form, "next": next_url})


def admin_logout(request):
    logout(request)
    return redirect("admin_login")


@admin_required
def admin_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps you logged in after the change
            messages.success(request, "Password changed successfully.")
            return redirect("admin_dashboard")
    else:
        form = PasswordChangeForm(request.user)

    for field in form.fields.values():
        field.widget.attrs.setdefault("class", "form-control")

    return render(request, "admin/admin_form.html", {
        "form": form,
        "title": "Change Password",
        "subtitle": "Use a strong password you don't use anywhere else.",
        "submit_label": "Update Password",
        "back_url": "admin_dashboard",
        "back_label": "Back to Dashboard",
        "active": "password",
        **_sidebar_counts(),
    })


# ───────────────────────── dashboard ─────────────────────────

@admin_required
def admin_dashboard(request):
    context = {
        **_sidebar_counts(),
        "active": "dashboard",
        "recent_projects": Project.objects.order_by("-created_at")[:5],
        "recent_contacts": Contact.objects.order_by("-sent_at")[:5],
        "recent_blogs": Blog.objects.order_by("-created_at")[:5],
    }
    return render(request, "admin/dashboard.html", context)


# ───────────────────────── projects ─────────────────────────

@admin_required
def admin_project_list(request):
    query = request.GET.get("q", "").strip()
    projects = Project.objects.all().order_by("-created_at")
    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(category__icontains=query)
            | Q(technologies__icontains=query)
        )
    page = _paginate(request, projects)
    return render(request, "admin/admin_project_list.html", {
        "projects": page["page_obj"], **page, "active": "projects", **_sidebar_counts(),
    })


@admin_required
def admin_project_add(request):
    return _form_view(
        request, ProjectForm, title="Add Project",
        subtitle="Add a new project to your portfolio.",
        success_msg="Project added successfully.",
        redirect_to="admin_project_list", back_label="Back to Projects", active="projects",
    )


@admin_required
def admin_project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return _form_view(
        request, ProjectForm, instance=project, title="Edit Project",
        subtitle="Update the details for this project.",
        success_msg="Project updated successfully.",
        redirect_to="admin_project_list", back_label="Back to Projects", active="projects",
    )


@admin_required
def admin_project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return _delete_view(
        request, project, object_type="project", label=project.title,
        success_msg="Project deleted.", redirect_to="admin_project_list", active="projects",
    )


# ───────────────────────── skills ─────────────────────────

@admin_required
def admin_skill_list(request):
    return render(request, "admin/admin_skill_list.html", {
        "skills": Skill.objects.all().order_by("-proficiency"),
        "active": "skills", **_sidebar_counts(),
    })


@admin_required
def admin_skill_add(request):
    return _form_view(
        request, SkillForm, title="Add Skill",
        subtitle="Add a new skill to showcase your expertise.",
        success_msg="Skill added successfully.",
        redirect_to="skill", back_label="Back to Skills", active="skills",
    )


@admin_required
def admin_skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return _form_view(
        request, SkillForm, instance=skill, title="Edit Skill",
        subtitle="Update this skill.",
        success_msg="Skill updated successfully.",
        redirect_to="skill", back_label="Back to Skills", active="skills",
    )


@admin_required
def admin_skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return _delete_view(
        request, skill, object_type="skill", label=skill.name,
        success_msg="Skill deleted.", redirect_to="skill", active="skills",
    )


# ───────────────────────── blog ─────────────────────────

@admin_required
def admin_blog_list(request):
    query = request.GET.get("q", "").strip()
    blogs = Blog.objects.all().order_by("-created_at")
    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(summary__icontains=query)
        )
    page = _paginate(request, blogs)
    return render(request, "admin/admin_blog_list.html", {
        "blogs": page["page_obj"], **page, "active": "blog", **_sidebar_counts(),
    })


@admin_required
def admin_blog_add(request):
    return _form_view(
        request, BlogForm, title="New Blog Post",
        subtitle="Write and publish a new blog post.",
        success_msg="Blog post published.",
        redirect_to="blog", back_label="Back to Blog", active="blog",
    )


@admin_required
def admin_blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return _form_view(
        request, BlogForm, instance=blog, title="Edit Blog Post",
        subtitle="Update this blog post.",
        success_msg="Blog post updated.",
        redirect_to="blog", back_label="Back to Blog", active="blog",
    )


@admin_required
def admin_blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return _delete_view(
        request, blog, object_type="blog post", label=blog.title,
        success_msg="Blog post deleted.", redirect_to="blog", active="blog",
    )


# ───────────────────────── about ─────────────────────────

@admin_required
def admin_about_list(request):
    return render(request, "admin/about_list.html", {
        "abouts": About.objects.all(), "active": "about", **_sidebar_counts(),
    })


@admin_required
def admin_about_add(request):
    return _form_view(
        request, AboutForm, title="Add About Image",
        subtitle="Upload an image for your About section.",
        success_msg="About image added.",
        redirect_to="admin_about_list", back_label="Back to About", active="about",
    )


@admin_required
def admin_about_edit(request, pk):
    about = get_object_or_404(About, pk=pk)
    return _form_view(
        request, AboutForm, instance=about, title="Edit About Image",
        subtitle="Replace this About image.",
        success_msg="About image updated.",
        redirect_to="admin_about_list", back_label="Back to About", active="about",
    )


@admin_required
def admin_about_delete(request, pk):
    about = get_object_or_404(About, pk=pk)
    return _delete_view(
        request, about, object_type="About image", label=f"About image #{about.pk}",
        success_msg="About image deleted.", redirect_to="admin_about_list", active="about",
    )


# ───────────────────────── messages (Contact) ─────────────────────────

@admin_required
def admin_message_list(request):
    query = request.GET.get("q", "").strip()
    contacts = Contact.objects.all().order_by("-sent_at")
    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(message__icontains=query)
        )
    page = _paginate(request, contacts)
    return render(request, "admin/admin_message_list.html", {
        "contacts": page["page_obj"], **page, "active": "messages", **_sidebar_counts(),
    })


@admin_required
def admin_message_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "admin/admin_message_detail.html", {
        "contact": contact,
        "wa_number": re.sub(r"\D", "", contact.phone_number or ""),  # digits only for wa.me
        "active": "messages", **_sidebar_counts(),
    })


@admin_required
def admin_message_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return _delete_view(
        request, contact, object_type="message", label=f"message from {contact.name}",
        success_msg="Message deleted.", redirect_to="admin_message_list", active="messages",
    )