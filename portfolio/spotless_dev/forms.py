from django import forms
from .models import Contact,Project

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control', 'required': True}),
            'phone_number': forms.NumberInput(attrs={'placeholder': 'Phone Number (Optional)', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'required': True}),
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "technologies",
            "description",
            "image",
            "project_url",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. E-commerce Dashboard"}),
            "technologies": forms.TextInput(
                attrs={"placeholder": "Comma-separated, e.g. Django, React, Firebase"}
            ),
            "description": forms.Textarea(attrs={"placeholder": "What this project is about..."}),
            "project_url": forms.URLInput(attrs={"placeholder": "https://... (optional)"}),
        }
# ADD to your existing forms.py (keep ContactForm and ProjectForm as they are)
from django import forms
from .models import Skill, Blog, About


class StyledModelForm(forms.ModelForm):
    """Adds a 'form-control' class to every input so your admin CSS can style them."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.ClearableFileInput)):
                continue
            field.widget.attrs.setdefault("class", "form-control")


class SkillForm(StyledModelForm):
    class Meta:
        model = Skill
        fields = ["name", "proficiency"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Django"}),
            "proficiency": forms.NumberInput(attrs={"min": 1, "max": 100}),
        }

    def clean_proficiency(self):
        value = self.cleaned_data["proficiency"]
        if not 1 <= value <= 100:
            raise forms.ValidationError("Enter a value between 1 and 100.")
        return value


class BlogForm(StyledModelForm):
    class Meta:
        model = Blog
        fields = ["title", "author", "image", "summary", "content"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3, "maxlength": 300}),
            "content": forms.Textarea(attrs={"rows": 14}),
        }


class AboutForm(StyledModelForm):
    class Meta:
        model = About
        fields = ["image"]