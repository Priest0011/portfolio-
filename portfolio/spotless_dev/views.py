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