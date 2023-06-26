from django.contrib import messages
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import FeedbackForm
from .models import FeedbackFileModel
from .services.email_view import PrerenderTemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"
    extra_context = {
        "author_photos": [
            static("pages/img/home/cards/1.jpg"),
            static("pages/img/home/cards/2.jpeg"),
            static("pages/img/home/cards/3.jpg"),
            static("pages/img/home/cards/4.jpeg"),
            static("pages/img/home/cards/5.jpg"),
        ],
        "feedback_photos": [
            static("pages/img/home/feedback/1.jpg"),
            static("pages/img/home/feedback/2.jpg"),
            static("pages/img/home/feedback/3.jpg"),
            static("pages/img/home/feedback/4.jpg"),
            static("pages/img/home/feedback/5.jpg"),
            static("pages/img/home/feedback/6.jpg"),
            static("pages/img/home/feedback/7.jpg"),
            static("pages/img/home/feedback/8.jpg"),
            static("pages/img/home/feedback/9.jpg"),
        ],
        "points_cards": [
            "У тебя нет времени заниматься в тренажёрном или спортивном зале",
            "Удобно заниматься спортом дома",
            "Нравится танцевать или хочешь научиться красиво двигаться",
            "Хочешь повысить свою физическую активность",
            "Желаешь сбросить лишние кг и улучшить качество тела",
            "Не хочешь изнурять себя тренировками в тренажёрном зале, а ищешь интересный спорт по душе",
            "Желаешь отвлечься от проблем и забот и чаще посвящать время себе",
            "Не хватает заряда энергии, положительных эмоций и поддержки",
        ],
        "marathon_cards": [
            "8 огненных тренировок ",
            "Специальная программа, разработанная для домашних условий",
            "Для тренировок понадобится только телефон или ноутбук",
            "Подходит для людей, которые решили заниматься спортом с нуля",
            "В программе сочетается 2 фитнес направления: Zumba и Body sculpt",
            "Бонусом после занятия идёт растяжка на все группы мышц",
        ],
        "results_cards": [
            "30 танцев под разные музыкальные направления",
            "Повысите выносливость и силу",
            "Сбросите лишние килограммы",
            "Улучшите состояние здоровья как физического, так и психического",
            "Сделаете тело более стройным и подтянутым",
            "Улучшите подвижность суставов и опорно-двигательного аппарата",
            "Получите багаж разных упражнений на все группы мышц",
            "Зарядитесь огромным количеством энергии, позитива и хорошего настроения",
            "Сможете заниматься спортом в удовольствие",
        ],
    }


class PolicyPageView(TemplateView):
    template_name = 'pages/policy.html'


class OfferPageView(TemplateView):
    template_name = 'pages/offer.html'


class FeedbackFormView(CreateView):
    template_name = 'pages/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        request = self.request

        files = request.FILES.getlist('files')  # field name in model
        feedback_instance = form.save(commit=False)
        feedback_instance.save()
        for file in files:
            file_instance = FeedbackFileModel(file=file, feedback=feedback_instance)
            file_instance.save()

        messages.add_message(
            request=self.request,
            level=messages.INFO,
            message="Ваш запрос отправлен в службу поддержки. Спасибо!"
        )
        return HttpResponseRedirect(self.success_url)


class ForbiddenDirectPageView(TemplateView):
    template_name = 'pages/forbidden_direct.html'
