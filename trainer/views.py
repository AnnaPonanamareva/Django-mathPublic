from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Card, Question, Topic


def _get_test_session_key(topic_slug: str) -> str:
    return f"tests_current_index_{topic_slug}"


def _get_task_session_key(topic_slug: str) -> str:
    return f"tasks_current_index_{topic_slug}"


def _get_card_session_key(topic_slug: str) -> str:
    return f"cards_current_index_{topic_slug}"


def index(request: HttpRequest) -> HttpResponse:
    topics = Topic.objects.all()
    return render(request, "trainer/index.html", {"topics": topics})


def topic(request: HttpRequest, slug: str) -> HttpResponse:
    current_topic = get_object_or_404(Topic, slug=slug)
    formats = [
        {
            "badge": "Режим 1",
            "title": "Тесты",
            "description": "Выбор правильного ответа из нескольких вариантов.",
            "url_name": "trainer:tests",
            "button_text": "Открыть тесты",
            "is_available": True,
            "status": "Доступно",
        },
        {
            "badge": "Режим 2",
            "title": "Задания",
            "description": "Самостоятельный ввод числового ответа в форму.",
            "url_name": "trainer:tasks",
            "button_text": "Открыть задания",
            "is_available": True,
            "status": "Доступно",
        },
        {
            "badge": "Режим 3",
            "title": "Карточки",
            "description": "Повторение вопроса и ответа по теме в карточках.",
            "url_name": "trainer:cards",
            "button_text": "Открыть карточки",
            "is_available": True,
            "status": "Доступно",
        },
    ]
    context = {
        "topic": current_topic,
        "formats": formats,
    }
    return render(request, "trainer/topic.html", context)


def tests(request: HttpRequest, slug: str) -> HttpResponse:
    current_topic = get_object_or_404(Topic, slug=slug)
    questions = list(
        current_topic.questions.filter(
            format_type=Question.FORMAT_TEST
        ).prefetch_related("variants")
    )
    session_key = _get_test_session_key(current_topic.slug)
    current_index = request.session.get(session_key, 0)
    if current_index >= len(questions):
        current_index = 0
        request.session[session_key] = current_index

    phase = "answer"
    feedback_class = ""
    feedback_message = ""
    selected_variant = None

    if request.method == "POST" and questions:
        action = request.POST.get("action")
        if action == "next":
            request.session[session_key] = (current_index + 1) % len(questions)
            request.session.modified = True
            return redirect("trainer:tests", slug=current_topic.slug)

        current_question = questions[current_index]
        submitted_question_id = request.POST.get("question_id", "")
        if str(current_question.id) != submitted_question_id:
            return redirect("trainer:tests", slug=current_topic.slug)

        if action == "answer":
            chosen_value = request.POST.get("variant")
            if not chosen_value:
                feedback_class = "error"
                feedback_message = "Выберите один вариант ответа."
            else:
                selected_variant = int(chosen_value)
                if selected_variant == current_question.correct_answer:
                    phase = "correct"
                    feedback_class = "success"
                    feedback_message = "Верно, молодец"
                else:
                    phase = "incorrect"
                    feedback_class = "error"
                    feedback_message = "Неверно"
        elif action == "show_answer":
            phase = "revealed"
            feedback_class = "error"
            feedback_message = f"Правильный ответ: {current_question.correct_answer}"

    current_question = questions[current_index] if questions else None
    context = {
        "topic": current_topic,
        "question": current_question,
        "questions_count": len(questions),
        "current_number": current_index + 1 if questions else 0,
        "phase": phase,
        "feedback_class": feedback_class,
        "feedback_message": feedback_message,
        "selected_variant": selected_variant,
    }
    return render(request, "trainer/tests.html", context)


def tasks(request: HttpRequest, slug: str) -> HttpResponse:
    current_topic = get_object_or_404(Topic, slug=slug)
    questions = list(current_topic.questions.filter(format_type=Question.FORMAT_TASK))
    session_key = _get_task_session_key(current_topic.slug)
    current_index = request.session.get(session_key, 0)
    if current_index >= len(questions):
        current_index = 0
        request.session[session_key] = current_index

    phase = "answer"
    feedback_class = ""
    feedback_message = ""
    entered_value = ""

    if request.method == "POST" and questions:
        action = request.POST.get("action")
        if action == "next":
            request.session[session_key] = (current_index + 1) % len(questions)
            request.session.modified = True
            return redirect("trainer:tasks", slug=current_topic.slug)

        current_question = questions[current_index]
        submitted_question_id = request.POST.get("question_id", "")
        if str(current_question.id) != submitted_question_id:
            return redirect("trainer:tasks", slug=current_topic.slug)

        if action == "answer":
            entered_value = request.POST.get("answer", "").strip()
            if not entered_value:
                feedback_class = "error"
                feedback_message = "Введите число перед отправкой."
            else:
                try:
                    numeric_answer = int(entered_value)
                except ValueError:
                    entered_value = ""
                    feedback_class = "error"
                    feedback_message = "Введите целое число."
                else:
                    if numeric_answer == current_question.correct_answer:
                        phase = "correct"
                        feedback_class = "success"
                        feedback_message = "Верно"
                    else:
                        entered_value = ""
                        phase = "incorrect"
                        feedback_class = "error"
                        feedback_message = "Неверно"
        elif action == "show_answer":
            phase = "revealed"
            entered_value = str(current_question.correct_answer)
            feedback_class = "error"
            feedback_message = f"Правильный ответ: {current_question.correct_answer}"

    current_question = questions[current_index] if questions else None
    context = {
        "topic": current_topic,
        "question": current_question,
        "questions_count": len(questions),
        "current_number": current_index + 1 if questions else 0,
        "phase": phase,
        "feedback_class": feedback_class,
        "feedback_message": feedback_message,
        "entered_value": entered_value,
    }
    return render(request, "trainer/tasks.html", context)


def cards(request: HttpRequest, slug: str) -> HttpResponse:
    current_topic = get_object_or_404(Topic, slug=slug)
    cards_list = list(Card.objects.filter(topic=current_topic).order_by("order", "id"))
    session_key = _get_card_session_key(current_topic.slug)
    current_index = request.session.get(session_key, 0)
    if current_index >= len(cards_list):
        current_index = 0
        request.session[session_key] = current_index

    phase = "question"
    if request.method == "POST" and cards_list:
        action = request.POST.get("action")
        if action == "next":
            request.session[session_key] = (current_index + 1) % len(cards_list)
            request.session.modified = True
            return redirect("trainer:cards", slug=current_topic.slug)
        if action == "show_answer":
            phase = "revealed"

    current_card = cards_list[current_index] if cards_list else None
    context = {
        "topic": current_topic,
        "card": current_card,
        "cards_count": len(cards_list),
        "current_number": current_index + 1 if cards_list else 0,
        "phase": phase,
    }
    return render(request, "trainer/cards.html", context)
