from django.contrib import admin

from .models import *

# Register your models here.
class UserAttributeAdmin(admin.ModelAdmin):
	pass
class QuestionAdmin(admin.ModelAdmin):
	pass
class AnswerAdmin(admin.ModelAdmin):
	pass
class CommentAdmin(admin.ModelAdmin):
	pass
class DirectMessageAdmin(admin.ModelAdmin):
	pass	
admin.site.register(UserAttribute, UserAttributeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)