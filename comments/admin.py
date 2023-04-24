from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'content', 'created_at', 'parent_comment')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
