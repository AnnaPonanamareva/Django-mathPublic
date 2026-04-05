from django import forms


class TestAnswerForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput)
    variant = forms.TypedChoiceField(
        choices=(),
        coerce=int,
        empty_value=None,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Выберите один вариант ответа.",
            "invalid_choice": "Выберите корректный вариант ответа.",
        },
    )

    def __init__(self, *args, variants: list[tuple[int, int]] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["variant"].choices = variants or []


class TaskAnswerForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput)
    answer = forms.IntegerField(
        label="Ваш ответ",
        widget=forms.NumberInput(
            attrs={
                "class": "number-input",
                "inputmode": "numeric",
            }
        ),
        error_messages={
            "required": "Введите число перед отправкой.",
            "invalid": "Введите целое число.",
        },
    )
