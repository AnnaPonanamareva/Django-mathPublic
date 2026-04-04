from django.db import models


class Topic(models.Model):
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("Слаг", unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self) -> str:
        return str(self.name)


class Question(models.Model):
    FORMAT_TEST = "test"
    FORMAT_TASK = "task"
    FORMAT_CHOICES = [
        (FORMAT_TEST, "Тест"),
        (FORMAT_TASK, "Задание"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тема",
    )
    text = models.CharField("Текст вопроса", max_length=255)
    correct_answer = models.IntegerField("Правильный ответ")
    format_type = models.CharField("Формат", max_length=10, choices=FORMAT_CHOICES)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ("topic", "format_type", "order", "id")
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return str(self.text)


class TestVariant(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Вопрос",
    )
    value = models.IntegerField("Значение")
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ("question", "order", "id")
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self) -> str:
        return f"{self.question}: {self.value}"


class Card(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name="Тема",
    )
    question = models.CharField("Вопрос", max_length=255)
    answer = models.CharField("Ответ", max_length=255)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ("topic", "order", "id")
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self) -> str:
        return str(self.question)
