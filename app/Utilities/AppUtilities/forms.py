from django import forms
from datetime import date

from .models import Profile, Services, LastCounterReading, HistoryElectricityCR, HistoryWaterCR, HistoryGasCR

# AUTH #
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# AUTH #


# Authentication #
class SignInUserForm(AuthenticationForm, forms.ModelForm):
    """Форма для входа пользователя на сайт"""

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'txt-green form-control'


class SignUpUserForm(forms.ModelForm):
    """Форма регистрация пользователя на сайт"""

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Пароль:"
    )

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'txt-green form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SignUpLastCRForm(forms.ModelForm):
    """Форма регистрации пользователя таблицы передачи показаний"""

    class Meta:
        model = LastCounterReading
        fields = ("account_electricity_night", "account_electricity")


# Pass counter reading forms
class ProvidersPassCRForm(forms.ModelForm):
    """
    Абстрактная форма

    поставщиков услуг,
    с общими для всех полями и функциями
    """

    date_cr = forms.DateField(
        widget=forms.TextInput(attrs={"class": "txt-green w-75", "onclick": "xCal(this)", "onkeyup": "xCal()"}),
        label="Дата передачи показаний", initial=date.today, help_text="Формат: День.Месяц.Год"
    )
    first_cr = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "txt-green w-75", "placeholder": "99999"}),
        label="Счетчик", min_value=1, max_value=99999, help_text="Число от 1 до 99999"
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'txt-green form-control'


class GasPassCRForm(ProvidersPassCRForm):
    """Форма передачи показаний Газ"""

    class Meta:
        model = HistoryGasCR
        fields = ('date_cr', 'first_cr')


class ElectricityPassCRForm(ProvidersPassCRForm):
    """Форма передачи показаний Электричество"""

    first_cr = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "txt-green w-75", "placeholder": "99999"}),
        label="Дневной счетчик", min_value=1, max_value=99999, help_text="Число от 1 до 99999"
    )
    second_cr = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "txt-green w-75", "placeholder": "99999"}),
        label="Ночной счетчик", min_value=1, max_value=99999, required=False, help_text="Число от 1 до 99999"
    )

    class Meta:
        model = HistoryElectricityCR
        fields = ('date_cr', 'first_cr', 'second_cr')


class WaterPassCRForm(ProvidersPassCRForm):
    """Форма передачи показаний Вода"""

    first_cr = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "txt-green w-75", "placeholder": "99999"}),
        label="Счетчик питьевой воды", min_value=1, max_value=99999, help_text="Число от 1 до 99999"
    )
    second_cr = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "txt-green w-75", "placeholder": "99999"}),
        label="Счетчик вода для полива", min_value=1, max_value=99999, required=False, help_text="Число от 1 до 99999"
    )

    class Meta:
        model = HistoryWaterCR
        fields = ('date_cr', 'first_cr', 'second_cr')


# Personal area forms
class PersonalAreaUserDataForm(forms.ModelForm):
    """Форма смены данных пользователя в личном кабинете"""

    sur_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-sur-name"}),
        label="Фамилия"
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-name"}),
        label="Имя"
    )
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-patronymic"}),
        label="Отчество"
    )
    gender = forms.ChoiceField(
        choices=(("Не указано", "Не указано"), ("Мужской", "Мужской"), ("Женский", "Женский")),
        widget=forms.Select(attrs={"class": "txt-green w-100 ud-gender"}),
        label="Пол"
    )
    region = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-region"}),
        label="Область"
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-city"}),
        label="Город/Село"
    )
    street = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-street"}),
        label="Улица/Переулок/Проспект"
    )
    house = forms.IntegerField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-house"}),
        label="Номер дома"
    )
    prefix_house = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-prefix-house"}),
        label="Приставка к адресу", required=False
    )
    flat = forms.IntegerField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-flat"}),
        label="Номер квартиры", required=False
    )
    tel_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-tel-number"}),
        label="Номер телефона"
    )
    tel_number_extra = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-tel-number-extra"}),
        label="Доп. номер телефона", required=False
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "txt-green w-80 ud-email"}),
        label="Эл. почта", required=False
    )

    class Meta:
        model = Profile
        fields = ("sur_name", "name", "patronymic", "gender",
                  "region", "city", "street", "house", "prefix_house", "flat",
                  "tel_number", "tel_number_extra", "email")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'txt-green form-control'


class PersonalAreaServicesForm(forms.ModelForm):
    """Форма смены услуг пользователя в личном кабинете"""

    # Поля Газ
    availability_gas = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
        label="Наличие счетчика Газ", required=False, help_text="start_div"
    )
    account_gas = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-20"}),
        label="Лицевой счет Газ", required=False, help_text="end_div"
    )

    # Поля Электричество
    availability_electricity = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
        label="Наличие дневного счетчика Электричество", required=False, help_text="start_div"
    )
    account_electricity = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-20"}),
        label="Лицевой счет Элестричество", required=False, help_text="end_div"
    )
    availability_electricity_night = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
        label="Наличие ночного счетчика Электричество", required=False, help_text="start_div"
    )
    account_electricity_night = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-20"}),
        label="Лицевой счет ночное Электричество", required=False, help_text="end_div"
    )

    # Поля Вода
    availability_water = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
        label="Наличие счетчика питьевой Воды", required=False, help_text="start_div"
    )
    account_water = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-20"}),
        label="Лицевой счет Вода", required=False, help_text="end_div"
    )
    availability_water_irrigation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
        label="Наличие счетчика Воды для полива", required=False, help_text="start_div"
    )
    account_water_irrigation = forms.CharField(
        widget=forms.TextInput(attrs={"class": "txt-green w-20"}),
        label="Лицевой счет вода для полива", required=False, help_text="end_div"
    )

    class Meta:
        model = Services
        fields = ("availability_electricity", "account_electricity",
                  "availability_electricity_night", "account_electricity_night",
                  "availability_water", "account_water",
                  "availability_water_irrigation", "account_water_irrigation",
                  "availability_gas", "account_gas")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'txt-green form-control'
