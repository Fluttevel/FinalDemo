from django. urls import path


url_patterns = [
    path("", views.HomePageListView.as_view(), name="provider_home"),
    path("sign-in/", views.SignInLoginView.as_view(), name="page_prov_sign_in"),
    path("upload/", views.UploadView.as_view(), name="page_upload"),
    path("download/", views.DownloadViews.as_view(), name="page_download")
]