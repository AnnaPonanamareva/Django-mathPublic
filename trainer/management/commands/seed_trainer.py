from django.core.management.base import BaseCommand

from trainer.models import Card, Question, TestVariant, Topic


class Command(BaseCommand):
    help = "Создает стартовые данные для тренажера по математике."

    def handle(self, *args, **options):
        topic, _ = Topic.objects.update_or_create(
            slug="arithmetic",
            defaults={
                "name": "Арифметические действия",
                "description": (
                    "Тренировка сложения, вычитания, умножения и деления "
                    "в формате тестов, заданий и карточек."
                ),
            },
        )

        test_questions = [
            {"order": 1, "text": "2 + 2", "correct_answer": 4, "variants": [3, 4, 5, 6]},
            {"order": 2, "text": "2 * 2", "correct_answer": 4, "variants": [2, 4, 6, 8]},
            {"order": 3, "text": "10 - 3", "correct_answer": 7, "variants": [6, 7, 8, 9]},
            {"order": 4, "text": "12 / 3", "correct_answer": 4, "variants": [3, 4, 5, 6]},
            {"order": 5, "text": "7 + 5", "correct_answer": 12, "variants": [10, 11, 12, 13]},
        ]
        for payload in test_questions:
            self._create_test_question(topic, payload)

        task_questions = [
            {"order": 1, "text": "2 + 2", "correct_answer": 4},
            {"order": 2, "text": "2 / 2", "correct_answer": 1},
            {"order": 3, "text": "5 + 6", "correct_answer": 11},
            {"order": 4, "text": "9 - 4", "correct_answer": 5},
            {"order": 5, "text": "3 * 4", "correct_answer": 12},
        ]
        for payload in task_questions:
            self._create_task_question(topic, payload)

        cards = [
            ("Что означает знак + ?", "Сложение"),
            ("Что означает знак - ?", "Вычитание"),
            ("Что означает знак * ?", "Умножение"),
            ("Что означает знак / ?", "Деление"),
            ("Сколько будет 10 / 2?", "5"),
        ]
        for order, (question, answer) in enumerate(cards, start=1):
            Card.objects.update_or_create(
                topic=topic,
                order=order,
                defaults={
                    "question": question,
                    "answer": answer,
                },
            )

        self.stdout.write(self.style.SUCCESS("Стартовые данные созданы или обновлены."))

    def _create_test_question(self, topic: Topic, payload: dict):
        question, _ = Question.objects.update_or_create(
            topic=topic,
            format_type=Question.FORMAT_TEST,
            order=payload["order"],
            defaults={
                "text": payload["text"],
                "correct_answer": payload["correct_answer"],
            },
        )
        for variant_order, value in enumerate(payload["variants"], start=1):
            TestVariant.objects.update_or_create(
                question=question,
                order=variant_order,
                defaults={"value": value},
            )

    def _create_task_question(self, topic: Topic, payload: dict):
        Question.objects.update_or_create(
            topic=topic,
            format_type=Question.FORMAT_TASK,
            order=payload["order"],
            defaults={
                "text": payload["text"],
                "correct_answer": payload["correct_answer"],
            },
        )
