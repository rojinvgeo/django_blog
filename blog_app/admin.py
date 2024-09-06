from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from .models import Post

class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinymce/js/tinymce/tinymce.min.js',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={
                    'height': 500,
                    'width': 800,
                    'menubar': False,
                    'plugins': 'advlist autolink lists link image charmap print preview anchor',
                    'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
                }
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Post, PostAdmin)

# Register your models here.
admin.site.register( Category)
# admin.site.register(Post)
admin.site.register(Comment)