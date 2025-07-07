import markdown
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from meta.views import Meta

from .forms import CommentForm, ContactForm
from .models import LearningArticle, Product

# Create your views here.


def home(request):
    latest_products = Product.objects.all()[:3]
    latest_articles = LearningArticle.objects.filter(is_published=True)[:3]
    meta = Meta(
        title="ZeroStack — Промышленная автоматизация",
        description="Инновационные решения для автоматизации и оптимизации промышленных процессов.",
        keywords=["промышленная автоматизация", "zerostack", "продукты", "услуги"],
        url=request.build_absolute_uri(),
    )
    return render(
        request,
        "core/home.html",
        {
            "latest_products": latest_products,
            "latest_articles": latest_articles,
            "meta": meta,
        },
    )


def about(request):
    meta = Meta(
        title="О компании ZeroStack",
        description="О компании ZeroStack: опыт, миссия, ценности.",
        keywords=["о компании", "zerostack", "автоматизация"],
        url=request.build_absolute_uri(),
    )
    return render(request, "core/about.html", {"meta": meta})


def services(request):
    meta = Meta(
        title="Услуги ZeroStack",
        description="Комплексные услуги по автоматизации и оптимизации бизнеса.",
        keywords=["услуги", "автоматизация", "zerostack"],
        url=request.build_absolute_uri(),
    )
    return render(request, "core/services.html", {"meta": meta})


def products(request):
    products = Product.objects.prefetch_related("images").all()
    meta = Meta(
        title="Продукты ZeroStack",
        description="Инновационные продукты для промышленной автоматизации.",
        keywords=["продукты", "автоматизация", "zerostack"],
        url=request.build_absolute_uri(),
    )
    return render(
        request,
        "core/products.html",
        {"products": products, "meta": meta},
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = (
        Product.objects.filter(to_products__from_product=product)
        .prefetch_related("images")
        .order_by("to_products__order")
    )
    meta = Meta(
        title=product.title,
        description=product.description[:160],
        keywords=[product.title, "промышленная автоматизация", "zerostack"],
        image=product.images.first().image.url if product.images.exists() else None,
        url=request.build_absolute_uri(),
        og_type="product",
        object_type="product",
    )
    return render(
        request,
        "core/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "meta": meta,
        },
    )


def contact(request):
    meta = Meta(
        title="Контакты ZeroStack",
        description="Контактная информация ZeroStack: адрес, телефон, email.",
        keywords=["контакты", "zerostack", "связаться"],
        url=request.build_absolute_uri(),
    )
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Email отправка временно отключена
            return render(
                request,
                "core/contact.html",
                {"form": form, "success": True, "meta": meta},
            )
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form, "meta": meta})


def learning_detail(request, slug):
    article = get_object_or_404(LearningArticle, slug=slug)
    comments_list = article.comments.filter(is_active=True).order_by("created_at")

    # Пагинация комментариев
    paginator = Paginator(comments_list, 5)  # 5 комментариев на страницу
    page_number = request.GET.get("page")

    # Если страница не указана, показываем последнюю
    if not page_number:
        page_number = paginator.num_pages

    comments = paginator.get_page(page_number)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request, "Ваш комментарий успешно добавлен!")
            # После добавления комментария перенаправляем на последнюю страницу
            return redirect("core:learning_detail", slug=slug)
    else:
        form = CommentForm()

    # Конвертируем Markdown в HTML
    content_html = markdown.markdown(
        article.content, extensions=["extra", "codehilite"]
    )

    # Получаем связанные статьи
    related_articles = article.get_related_articles()

    meta = Meta(
        title=article.title,
        description=article.excerpt or article.content[:160],
        keywords=[article.title, "статья", "zerostack"],
        image=None,
        url=request.build_absolute_uri(),
        og_type="article",
        object_type="article",
    )

    context = {
        "article": article,
        "content_html": content_html,
        "comments": comments,
        "form": form,
        "related_articles": related_articles,
        "meta": meta,
    }
    return render(request, "core/learning_detail.html", context)


class LearningArticleListView(ListView):
    model = LearningArticle
    template_name = "core/learning.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return LearningArticle.objects.all().order_by("-created_at")


class LearningArticleDetailView(DetailView):
    model = LearningArticle
    template_name = "core/learning_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        meta = Meta(
            title=article.title,
            description=article.excerpt or article.content[:160],
            keywords=[article.title, "статья", "zerostack"],
            image=None,
            url=self.request.build_absolute_uri(),
            og_type="article",
            object_type="article",
        )
        context["meta"] = meta
        return context
