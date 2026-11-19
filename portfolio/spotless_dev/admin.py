from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Skill, Contact, Blog, About


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category_badge', 'tech_tags', 'project_url_link', 'created_at', 'display_image')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_per_page = 20
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'description', 'category', 'technologies')
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Links', {
            'fields': ('project_url',),
            'classes': ('collapse',)
        }),
    )

    def category_badge(self, obj):
        colors = {
            'web': '#00d4ff',
            'app': '#ff3366',
            'ecom': '#b829dd',
            'uiux': '#f9d423',
            'other': '#8a8a9e',
        }
        color = colors.get(obj.category, '#8a8a9e')
        display = obj.get_category_display()
        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:100px; font-size:0.8rem; font-weight:600;">{}</span>',
            color, display
        )
    category_badge.short_description = 'Category'

    def tech_tags(self, obj):
        techs = obj.get_technologies_list()
        if not techs:
            return format_html('<span style="color:#666;">—</span>')
        tags = ''.join([
            format_html('<span style="background:rgba(255,255,255,0.05); color:var(--text-muted); padding:2px 8px; border-radius:4px; font-size:0.75rem; margin-right:4px; border:1px solid var(--card-border);">{}</span>', tech)
            for tech in techs[:3]
        ])
        if len(techs) > 3:
            tags += format_html('<span style="color:#666; font-size:0.75rem;">+{}</span>', len(techs) - 3)
        return format_html('<div style="display:flex; gap:4px; flex-wrap:wrap;">{}</div>', tags)
    tech_tags.short_description = 'Tech Stack'

    def project_url_link(self, obj):
        if obj.project_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#00d4ff;"><i class="fas fa-external-link-alt"></i> View</a>',
                obj.project_url
            )
        return format_html('<span style="color:#666;">—</span>')
    project_url_link.short_description = 'URL'

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px; height:40px; object-fit:cover; border-radius:6px;" />',
                obj.image.url
            )
        return format_html('<span style="color:#666;">No image</span>')
    display_image.short_description = 'Preview'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'proficiency_bar')
    search_fields = ('name',)
    list_per_page = 25
    ordering = ('-proficiency',)

    def proficiency_bar(self, obj):
        width = obj.proficiency if obj.proficiency else 0
        color = '#00ff88' if width >= 80 else '#ff3366' if width < 50 else '#f9d423'
        return format_html(
            '<div style="background:#1a1a2e; border-radius:100px; width:120px; height:8px; overflow:hidden;">'
            '<div style="background:{}; width:{}%; height:100%; border-radius:100px;"></div></div> '
            '<span style="color:{}; font-size:0.8rem; font-weight:600;">{}%</span>',
            color, width, color, width
        )
    proficiency_bar.short_description = 'Proficiency'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'message_preview', 'sent_at', 'actions_col')
    search_fields = ('name', 'email', 'message')
    list_per_page = 20
    ordering = ('-sent_at',)
    date_hierarchy = 'sent_at'
    readonly_fields = ('sent_at',)

    fieldsets = (
        ('Sender Info', {
            'fields': ('name', 'email', 'phone_number')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Sent At', {
            'fields': ('sent_at',),
            'classes': ('collapse',)
        }),
    )

    def message_preview(self, obj):
        if obj.message:
            return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
        return '—'
    message_preview.short_description = 'Message Preview'

    def actions_col(self, obj):
        return format_html(
            '<a href="{}/change/" style="color:#00d4ff; margin-right:10px;"><i class="fas fa-eye"></i></a>'
            '<a href="{}/delete/" style="color:#ff3366;"><i class="fas fa-trash"></i></a>',
            obj.pk, obj.pk
        )
    actions_col.short_description = 'Actions'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'display_image', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'summary', 'content')
    list_per_page = 15
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'author', 'summary')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px; height:40px; object-fit:cover; border-radius:6px;" />',
                obj.image.url
            )
        return format_html('<span style="color:#666;">No image</span>')
    display_image.short_description = 'Preview'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_image')

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return format_html('<span style="color:#666;">No image</span>')
    display_image.short_description = 'Profile Photo'