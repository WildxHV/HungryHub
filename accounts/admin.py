from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import admin_thumbnails
# from products.actions import export_selected_as_csv
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name', 'phone_number', 'role',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    list_display = ( 'email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined','role', 'is_active')
    list_display_links = ('email', 'first_name','last_name')
    readonly_fields = ('last_login', 'date_joined') 
    ordering = ('-date_joined',)
    search_fields = User.SearchableFields
    list_filter = ('role', 'is_active', 'date_joined')
    # actions = [export_selected_as_csv]
    
    
    
    filter_horizontal= ()
    list_filter = ()
    fieldsets = (
        ( None, {
            'fields': ('email','username', 'first_name', 'last_name', 'phone_number', 'role', 'password')
            }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active','is_superadmin' ,'groups', 'user_permissions', )
        }),
        
        
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2'),
        }),
        
    )
    

@admin_thumbnails.thumbnail('profile_picture')
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'pincode', 'created_at')
    search_fields = UserProfile.SearchableFields
    list_filter = ('created_at', 'user__is_active')
    # actions = [export_selected_as_csv]


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(User,CustomUserAdmin)