from django.contrib import admin
from .models import Question, Choice

# customize how the admin form looks and works: 
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# create a model admin class, 
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    # Choice objects are edited on the Question admin page. By default, provide enough fields for 3 choices.
    inlines = [ChoiceInline]
    # a list of field names to display, as columns, on the change list page for the object
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # adds a “Filter” sidebar that lets people filter the change list by the pub_date field
    list_filter = ["pub_date"]
    # adds a search box at the top of the change list
    search_fields = ["question_text"]

# then pass it as the second argument to admin.site.register()
admin.site.register(Question, QuestionAdmin)


