from django.contrib import admin

from .models import LearningArticle, Product, ProductImage, RelatedProduct


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'title', 'description', 'order', 'is_main')
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"


class RelatedProductInline(admin.TabularInline):
    model = RelatedProduct
    fk_name = "from_product"
    extra = 1
    verbose_name = "Связанный продукт"
    verbose_name_plural = "Связанные продукты"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline, RelatedProductInline]

    fieldsets = (
        ("Основная информация", {"fields": ("title", "slug", "description")}),
        ("Детали", {"fields": ("features", "specifications")}),
        (
            "Метаданные",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "title", "is_main", "order", "created_at")
    list_filter = ("is_main", "created_at")
    search_fields = ("product__title", "title", "description")
    list_editable = ("order", "is_main")
    ordering = ("product", "order", "-is_main")


@admin.register(RelatedProduct)
class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ("from_product", "to_product", "order")
    list_filter = ("from_product", "to_product")
    search_fields = ("from_product__title", "to_product__title")
    ordering = ("order",)


@admin.register(LearningArticle)
class LearningArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at", "is_published", "order")
    list_filter = ("is_published", "created_at", "updated_at")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "is_published",
                    "order",
                )
            },
        ),
    )
