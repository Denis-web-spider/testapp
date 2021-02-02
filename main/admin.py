from django.contrib import admin

from .models import Tests, Questions, Answers



class QuestionsInline(admin.TabularInline):
    model = Questions

class AnswersInline(admin.TabularInline):
    model = Answers

@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ['test_name', 'test_text']
    inlines = [QuestionsInline]

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]
