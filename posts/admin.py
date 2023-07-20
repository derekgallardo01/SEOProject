from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Author, Category, Post, Comment, PostView, Help
from django.utils.html import format_html

class HelpAdmin(admin.ModelAdmin ):
    list_per_page = 20
    list_display = ('title', 'overview', 'all_actions')
    
    def all_actions(self,obj):
        return format_html('<span class="changelink"><a href="{url}">Edit</a></span>', url='/admin/posts/help/'+str(obj.id)+'/change')
    all_actions.short_description = 'actions'

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Help, HelpAdmin)
#admin.site.register(Author)
#admin.site.register(Category)
#admin.site.register(Post)
#admin.site.register(Comment)
#admin.site.register(PostView)