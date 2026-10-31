from django.urls import path
from vinyl import views

urlpatterns = [
    path("artists/", views.ArtistList.as_view(), name="artist-list"),
    path("artists/<int:pk>/", views.ArtistDetail.as_view(), name="artist-detail"),
    path("artists/<int:pk>/records/", views.ArtistRecords.as_view(), name="artist-records"),
    
    path("labels/", views.LabelList.as_view(), name="label-list"),
    path("labels/<int:pk>/", views.LabelDetail.as_view(), name="label-detail"),

    path("records/", views.RecordList.as_view(), name="record-list"),
    path("records/<int:pk/", views.RecordDetail.as_view(), name="record-detail")
]
