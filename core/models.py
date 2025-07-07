import json

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from meta.models import ModelMeta

# Create your models here.


class Product(ModelMeta, models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Описание")
    features = models.JSONField(default=list, verbose_name="Возможности")
    specifications = models.JSONField(
        default=dict, verbose_name="Технические характеристики"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    related_products = models.ManyToManyField(
        "self",
        through="RelatedProduct",
        symmetrical=False,
        blank=True,
        verbose_name="Связанные продукты",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product_detail", kwargs={"slug": self.slug})

    def is_new(self):
        """Проверяет, является ли продукт новым (младше 6 месяцев)"""
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        return self.created_at > six_months_ago

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_meta(self, request=None):
        image_url = self.images.first().image.url if self.images.exists() else None
        url = (
            request.build_absolute_uri(self.get_absolute_url())
            if request
            else f"{settings.SITE_DOMAIN}{self.get_absolute_url()}"
        )
        return {
            "title": self.title,
            "description": self.description[:160],
            "keywords": [self.title, "промышленная автоматизация", "zerostack"],
            "image": image_url,
            "url": url,
            "og_type": "product",
            "object_type": "product",
        }


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Продукт"
    )
    image = models.ImageField(
        upload_to="products/%Y/%m/%d/", verbose_name="Изображение"
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"
        ordering = ["order", "-is_main", "-created_at"]

    def __str__(self):
        return f"{self.product.title} - {self.title or 'Изображение'}"

    def save(self, *args, **kwargs):
        if self.is_main:
            # Сбрасываем флаг is_main у других изображений этого продукта
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(
                pk=self.pk
            ).update(is_main=False)
        super().save(*args, **kwargs)


class RelatedProduct(models.Model):
    from_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="from_products",
        verbose_name="Основной продукт",
    )
    to_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="to_products",
        verbose_name="Связанный продукт",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Связанный продукт"
        verbose_name_plural = "Связанные продукты"
        ordering = ["order"]
        unique_together = ["from_product", "to_product"]

    def __str__(self):
        return f"{self.from_product.title} -> {self.to_product.title}"


class LearningArticle(ModelMeta, models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание (Markdown)")
    excerpt = models.TextField(
        verbose_name="Краткое описание", blank=True, help_text="Краткое описание статьи"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:learning_detail", kwargs={"slug": self.slug})

    def get_related_articles(self, limit=3):
        """Возвращает похожие статьи, исключая текущую"""
        return (
            LearningArticle.objects.filter(is_published=True)
            .exclude(id=self.id)
            .order_by("-created_at")[:limit]
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_meta(self, request=None):
        url = (
            request.build_absolute_uri(self.get_absolute_url())
            if request
            else f"{settings.SITE_DOMAIN}{self.get_absolute_url()}"
        )
        return {
            "title": self.title,
            "description": self.excerpt or self.content[:160],
            "keywords": [self.title, "статья", "zerostack"],
            "image": None,
            "url": url,
            "og_type": "article",
            "object_type": "article",
        }


class Comment(models.Model):
    article = models.ForeignKey(
        "LearningArticle",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Статья",
    )
    author_name = models.CharField(max_length=100, verbose_name="Имя автора")
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Комментарий от {self.author_name} к статье {self.article.title}"
