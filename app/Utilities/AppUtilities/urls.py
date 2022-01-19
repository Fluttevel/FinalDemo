from django.urls import path

from . import views


urlpatterns = [
    path("", views.HomePageListView.as_view(), name="user_home"),

    # Authentication #
    path("sign-in/", views.SignInLoginView.as_view(), name="page_sign_in"),
    path("pre-sign-up/", views.PreSignUpCreateView.as_view(), name="page_pre_sign_up"),
    path("sign-up/", views.SignUpCreateView.as_view(), name="page_sign_up"),
    path("sign-up-last-cr/", views.SignUpLastCRCreateView.as_view(), name="sign_up_last_cr"),
    path("sign-up-services/", views.SignUpServicesCreateView.as_view(), name="sign_up_services"),
    path("logout/", views.UserLogoutView.as_view(), name="def_logout"),

    # Pass counter reading #
    path("pass/gas/", views.GasPassCRCreateView.as_view(), name="page_g_pass"),
    path("pass/water/", views.WaterPassCRCreateView.as_view(), name="page_w_pass"),
    path("pass/electricity/", views.ElectricityPassCRCreateView.as_view(), name="page_e_pass"),

    # History #
    path("history/gas/", views.GasHistoryListView.as_view(), name="page_g_history"),
    path("history/electricity/", views.ElectricityHistoryListView.as_view(), name="page_e_history"),
    path("history/water/", views.WaterHistoryListView.as_view(), name="page_w_history"),

    # Personal area
    path("personal-area/user-data/<int:pk>/", views.PersonalAreaUserDataUpdateView.as_view(), name="page_pa_user"),
    path("personal-area/services/<int:pk>/", views.PersonalAreaServicesUpdateView.as_view(), name="page_pa_services")

    # Instance: Detail Create Update Delete #
    # path("pass-detail/<slug:slug>/", views.PagePassCRDetailView.as_view(), name="page_pass_cr"),
    # path("history/electricity/", views.ElectricityPassCRCreateView.as_view(), name="page_e_history"),
    # path("history/electricity/update/<int:pk>/", views.ECRUpdateView.as_view(), name="page_update_e_history"),
    # path("history/electricity/delete/<int:pk>/", views.ECRDeleteView.as_view(), name="def_delete_e_history"),
    # Old path
    # path("history/electricity/old/", views.utility_history, name="page_utility_history"),
    # path("history/electricity/<int:pk>/", views.history_update, name="page_utility_history_update"),
    # path("history/electricity/delete/<int:pk>/", views.history_delete, name="def_utility_history_delete")
]
