from django.contrib import admin

from .models import *

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
	pass
class AnswerAdmin(admin.ModelAdmin):
	pass
class CommentAdmin(admin.ModelAdmin):
	pass
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)