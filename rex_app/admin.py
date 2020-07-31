from django.contrib import admin

from .models import *

class FriendAdditionalDetailInline(admin.TabularInline):
	model = FriendAdditionalDetail
	extra = 1

# Register your models here.
class UserAttributeAdmin(admin.ModelAdmin):
	inlines = (FriendAdditionalDetailInline,)
class QuestionAdmin(admin.ModelAdmin):
	pass
class AnswerAdmin(admin.ModelAdmin):
	pass
class CommentAdmin(admin.ModelAdmin):
	pass
class DirectMessageAdmin(admin.ModelAdmin): 
	pass	
class TagAdmin(admin.ModelAdmin):
	pass	

admin.site.register(UserAttribute, UserAttributeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)
admin.site.register(Tag, TagAdmin)
