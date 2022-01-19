from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages

from .models import Profile, ServiceProviders, Services, LastCounterReading,\
    HistoryGasCR, HistoryElectricityCR, HistoryWaterCR
from .forms import PersonalAreaUserDataForm, PersonalAreaServicesForm,\
    ElectricityPassCRForm, GasPassCRForm, WaterPassCRForm

# Authentication #
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import SignInUserForm, SignUpUserForm, SignUpLastCRForm

# Transliterate
from transliterate import translit, slugify, get_available_language_codes


class HomePageListView(LoginRequiredMixin, ListView):
    """Главная страница"""

    model = ServiceProviders
    queryset = ServiceProviders.objects.all()
    template_name = "utilities/user-homepage.html"
    context_object_name = "providers"

    def get_context_data(self, **kwargs):
        kwargs['user_data'] = Profile.objects.get(login=self.request.user)
        kwargs['services'] = Services.objects.get(username=self.request.user)
        kwargs['history_g'] = HistoryGasCR.objects.filter(username=self.request.user).order_by('-id_reading')[:1]
        kwargs['history_e'] = HistoryElectricityCR.objects.filter(username=self.request.user).order_by('-id_reading')[:1]
        kwargs['history_w'] = HistoryWaterCR.objects.filter(username=self.request.user).order_by('-id_reading')[:1]
        kwargs['last_cr'] = LastCounterReading.objects.get(username=self.request.user)
        return super().get_context_data(**kwargs)


# Mixin #
class CustomSuccessMessageMixin:
    """Абстрактный класс уведомлений"""

    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class MixinHistory(CustomSuccessMessageMixin):
    """Класс уведомлений история передачи показаний"""

    # Для подсвечивания редактируемого элемента
    def get_success_url(self):
        return "%s?id=%s" % (self.success_url, self.object.id_reading)


# Authentication
class SignInLoginView(LoginView):
    """Страница вход пользователя на сайт"""

    template_name = 'utilities/user-signin.html'
    form_class = SignInUserForm
    success_url = reverse_lazy("user_home")

    def get_success_url(self):
        return self.success_url


class PreSignUpCreateView(CreateView):
    """Страница регистрации пользователя"""

    model = User
    template_name = 'utilities/user-signup.html'
    form_class = SignUpUserForm
    success_url = reverse_lazy('page_sign_up')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class SignUpCreateView(CreateView):
    """Страница личного кабинета пользовательских данных"""

    model = Profile
    template_name = 'utilities/user-signup.html'
    form_class = PersonalAreaUserDataForm
    success_url = reverse_lazy('sign_up_last_cr')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.login = self.request.user
        self.object.save()
        return super().form_valid(form)


class SignUpLastCRCreateView(CreateView):
    """Промежуточная вьюшка для добавления таблицы последней передачи показаний"""

    model = LastCounterReading
    template_name = 'utilities/user-signup.html'
    form_class = SignUpLastCRForm
    success_url = reverse_lazy('sign_up_services')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        self.object.save()
        return super().form_valid(form)


class SignUpServicesCreateView(CustomSuccessMessageMixin, CreateView):
    """Промежуточная вьюшка для добавления услуг к новому пользователю"""

    model = Services
    template_name = 'utilities/user-signup.html'
    form_class = PersonalAreaServicesForm
    success_url = reverse_lazy('user_home')
    success_msg = "Вы были успешно зарегестрированы!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        self.object.save()
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Функционал выхода пользователя из аккаунта"""

    next_page = reverse_lazy('page_sign_in')


# Pass counter reading #
class ProvidersPassCRCreateView(MixinHistory, CreateView):
    """
    Абстрактный класс

    поставщиков услуг,
    с общими для всех полями и функциями
    """

    template_name = 'utilities/pass-counter-reading.html'
    success_msg = 'Показания успешно переданы!'

    def get_context_data(self, **kwargs):
        kwargs['user_data'] = Profile.objects.get(login=self.request.user)
        kwargs['providers'] = ServiceProviders.objects.all()
        kwargs['services'] = Services.objects.get(username=self.request.user)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        # Дополнительные данные о лицевых считах
        self.object.save()
        return super().form_valid(form)


class GasPassCRCreateView(ProvidersPassCRCreateView):
    """Передача показаний Газ"""

    model = HistoryGasCR
    form_class = GasPassCRForm
    success_url = reverse_lazy('write_last_cr_gas')

    def get_context_data(self, **kwargs):
        kwargs['provider'] = ServiceProviders.objects.get(id_provider=1)
        kwargs['token'] = 'Gas'
        return super().get_context_data(**kwargs)


class ElectricityPassCRCreateView(ProvidersPassCRCreateView):
    """Передача показаний Электричество"""

    model = HistoryElectricityCR
    form_class = ElectricityPassCRForm
    success_url = reverse_lazy('page_e_history')

    def get_context_data(self, **kwargs):
        kwargs['provider'] = ServiceProviders.objects.get(id_provider=2)
        kwargs['token'] = 'Electricity'
        return super().get_context_data(**kwargs)


class WaterPassCRCreateView(ProvidersPassCRCreateView):
    """Передача показаний Вода"""

    model = HistoryWaterCR
    form_class = WaterPassCRForm
    success_url = reverse_lazy('page_w_history')

    def get_context_data(self, **kwargs):
        kwargs['provider'] = ServiceProviders.objects.get(id_provider=3)
        kwargs['token'] = 'Water'
        return super().get_context_data(**kwargs)


# History #
class ProvidersHistoryListView(ListView):
    """
    Абстрактный класс

    поставщиков услуг,
    с общими для всех полями и функциями
    """

    queryset = ServiceProviders.objects.all()
    template_name = 'utilities/utility-history.html'
    context_object_name = 'providers'

    def get_context_data(self, **kwargs):
        kwargs['user_data'] = Profile.objects.get(login=self.request.user)
        kwargs['services'] = Services.objects.get(username=self.request.user)
        return super().get_context_data(**kwargs)


class GasHistoryListView(ProvidersHistoryListView):
    """История передачи показаний Газ"""

    model = HistoryGasCR

    def get_context_data(self, **kwargs):
        kwargs['history'] = HistoryGasCR.objects.filter(username=self.request.user).order_by('-id_reading')
        kwargs['token'] = 'Gas'
        return super().get_context_data(**kwargs)


class ElectricityHistoryListView(ProvidersHistoryListView):
    """История передачи показаний Электричество"""

    model = HistoryElectricityCR

    def get_context_data(self, **kwargs):
        kwargs['history'] = HistoryElectricityCR.objects.filter(username=self.request.user).order_by('-id_reading')
        kwargs['token'] = 'Electricity'
        return super().get_context_data(**kwargs)


class WaterHistoryListView(ProvidersHistoryListView):
    """История передачи показаний Вода"""

    model = HistoryWaterCR

    def get_context_data(self, **kwargs):
        kwargs['history'] = HistoryWaterCR.objects.filter(username=self.request.user).order_by('-id_reading')
        kwargs['token'] = 'Water'
        return super().get_context_data(**kwargs)


# Personal area #
class PersonalAreaUserDataUpdateView(CustomSuccessMessageMixin, UpdateView):
    """Страница личного кабинета пользовательских данных"""

    model = Profile
    template_name = 'utilities/user-personal-area.html'
    form_class = PersonalAreaUserDataForm
    success_url = reverse_lazy('user_home')
    success_msg = "Личные данные успешно изменены!"

    def get_context_data(self, **kwargs):
        kwargs['personal_user_data'] = True

        kwargs['user_data'] = Profile.objects.get(login=self.request.user)
        kwargs['providers'] = ServiceProviders.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.login = self.request.user
        self.object.save()
        return super().form_valid(form)

    # def get_form_kwargs(self): !!!


class PersonalAreaServicesUpdateView(CustomSuccessMessageMixin, UpdateView):
    """Страница личного кабинета услуг пользователя"""

    model = Services
    template_name = 'utilities/user-personal-area.html'
    form_class = PersonalAreaServicesForm
    success_url = reverse_lazy('user_home')  # Переход на эту же страницу + модальное окно
    success_msg = "Ваши услуги успешно изменены!"

    def get_context_data(self, **kwargs):
        kwargs['personal_user_data'] = False

        kwargs['user_data'] = Profile.objects.get(login=self.request.user)
        kwargs['providers'] = ServiceProviders.objects.all()
        return super().get_context_data(**kwargs)

    def from_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        self.object.save()
        return super().form_valid(form)

    # def get_form_kwargs(self): !!! Для защиты чужих данных


# Instance: Detail Create Update Delete Views #
# class PagePassCRDetailView(LoginRequiredMixin, DetailView):
#     """Страница передачи показаний"""
#
#     model = ServiceProviders
#     slug_field = "url"
#     template_name = "utilities/pass-counter-reading.html"
#     context_object_name = "provider"
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_data'] = Profile.objects.get(login=self.request.user)
#         kwargs['providers'] = ServiceProviders.objects.all()
#         return super().get_context_data(**kwargs)
#
#
# class PassCRCreateView(CustomSuccessMessageMixin, CreateView):
#     """Передача показаний Электричество"""
#
#     model = HistoryElectricityCR
#     template_name = 'utilities/utility-history.html'
#     form_class = ElectricityPassCRForm
#     success_url = reverse_lazy('page_e_history')
#     success_msg = "Показания успешно переданы"
#
#     def get_context_data(self, **kwargs):
#         kwargs['history'] = HistoryElectricityCR.objects.all()
#
#         kwargs['electricity_name'] = "Свет"  # !!! МОЖНО ДОПОЛНИТЕЛЬНО ПЕРЕДАВАТЬ МОДЕЛИ !!! ЗАЕБИСЬ !!!
#         kwargs['user_data'] = Profile.objects.get(login=self.request.user)
#         # kwargs['providers'] = ServiceProviders.objects.all()
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.username = self.request.user  # Дополнительный параметр
#         # Добавить параметры лицевого счета подгружая с бд услуги
#         self.object.save()
#         return super().form_valid(form)
#
#
# class ECRUpdateView(CustomSuccessMessageMixin, UpdateView):
#     """Обновление показания Электричество"""
#
#     model = HistoryElectricityCR
#     template_name = 'utilities/utility-history.html'
#     form_class = ElectricityPassCRForm
#     success_url = reverse_lazy('page_e_history')
#     success_msg = "Показания успещно обновлены"
#
#     def get_context_data(self, **kwargs):
#         kwargs['flag_update'] = True
#
#         kwargs['user_data'] = Profile.objects.get(login=self.request.user)
#         kwargs['providers'] = ServiceProviders.objects.all()
#         return super().get_context_data(**kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#
#         if self.request.user != kwargs['instance'].username:
#             return self.handle_no_permission()
#         return kwargs
#
#
# class ECRDeleteView(DeleteView):
#     """Удаление показания Электричество"""
#
#     model = HistoryElectricityCR
#     template_name = 'utilities/utility-history.html'
#     success_url = reverse_lazy('page_e_history')
#     success_msg = "Показания успешно удалены"
#
#     def post(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_msg)
#         return super().post(request)
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         if self.request.user != self.object.username:
#             return self.handle_no_permission()
#
#         success_url = self.get_success_url()
#         self.object.delete()
#         return HttpResponseRedirect(success_url)


# Old views
# class HomePageView(LoginRequiredMixin, View):
#     """Главная страница"""
#     def get(self, request):
#         providers = ServiceProviders.objects.all()
#         return render(request, "utilities/user-homepage.html", {"providers": providers})


# class PagePassCRView(LoginRequiredMixin, View):
#     """Страница передачи показаний"""
#
#     def get(self, request, slug):
#         provider = ServiceProviders.objects.get(url=slug)
#         providers = ServiceProviders.objects.all()
#         return render(request, "utilities/pass-counter-reading.html", {"providers": providers, "provider": provider})


# def utility_history(request):
#     """Страница истории передачи показаний"""
#
#     if request.method == 'POST':
#         form = EPassCRForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#     template = 'utilities/utility-history.html'
#
#     context = {
#         'history': HistoryElectricityCR.objects.all(),
#         'form': EPassCRForm()
#     }
#
#     return render(request, template, context)


# def history_update(request, pk):
#     """Редактирование данных в истории"""
#
#     get_history = HistoryElectricityCR.objects.get(id_reading=pk)
#
#     if request.method == 'POST':
#         form = EPassCRForm(request.POST, instance=get_history)
#         if form.is_valid():
#             form.save()
#
#     template = 'utilities/utility-history.html'
#
#     context = {
#         'get_history': get_history,
#         'update': True,
#         'form': EPassCRForm(instance=get_history)
#     }
#
#     return render(request, template, context)


# def history_delete(request, pk):
#     """Удаление данных в истории"""
#
#     get_history = HistoryElectricityCR.objects.get(id_reading=pk)
#
#     get_history.delete()
#
#     return redirect(reverse("page_utility_history"))


# request - вся информация присланная от нашего клиента ( в моем случае браузер )
