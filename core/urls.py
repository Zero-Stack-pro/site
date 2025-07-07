from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("products/", views.products, name="products"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("contact/", views.contact, name="contact"),
    path("learning/", views.LearningArticleListView.as_view(), name="learning"),
    path("learning/<slug:slug>/", views.learning_detail, name="learning_detail"),
]
 