from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
            ],
            options={
                "verbose_name": "Тема",
                "verbose_name_plural": "Темы",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255, verbose_name="Текст вопроса")),
                ("correct_answer", models.IntegerField(verbose_name="Правильный ответ")),
                (
                    "format_type",
                    models.CharField(
                        choices=[("test", "Тест"), ("task", "Задание")],
                        max_length=10,
                        verbose_name="Формат",
                    ),
                ),
                ("order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="trainer.topic",
                        verbose_name="Тема",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
                "ordering": ("topic", "format_type", "order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=255, verbose_name="Вопрос")),
                ("answer", models.CharField(max_length=255, verbose_name="Ответ")),
                ("order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cards",
                        to="trainer.topic",
                        verbose_name="Тема",
                    ),
                ),
            ],
            options={
                "verbose_name": "Карточка",
                "verbose_name_plural": "Карточки",
                "ordering": ("topic", "order", "id"),
            },
        ),
        migrations.CreateModel(
            name="TestVariant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.IntegerField(verbose_name="Значение")),
                ("order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="trainer.question",
                        verbose_name="Вопрос",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вариант ответа",
                "verbose_name_plural": "Варианты ответов",
                "ordering": ("question", "order", "id"),
            },
        ),
    ]
