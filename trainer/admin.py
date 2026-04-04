from django.contrib import admin

from .models import Card, Question, TestVariant, Topic


class TestVariantInline(admin.TabularInline):
    model = TestVariant
    extra = 1


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "topic", "format_type", "correct_answer", "order")
    list_filter = ("format_type", "topic")
    search_fields = ("text",)
    ordering = ("topic", "format_type", "order", "id")
    inlines = [TestVariantInline]


@admin.register(TestVariant)
class TestVariantAdmin(admin.ModelAdmin):
    list_display = ("question", "value", "order")
    list_filter = ("question__topic",)
    ordering = ("question", "order", "id")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("question", "topic", "order")
    list_filter = ("topic",)
    search_fields = ("question", "answer")
    ordering = ("topic", "order", "id")
