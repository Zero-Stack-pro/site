import markdown
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import CommentForm, ContactForm
from .models import Comment, LearningArticle, Product, RelatedProduct

# Create your views here.


def home(request):
    latest_products = Product.objects.all()[:3]
    latest_articles = LearningArticle.objects.filter(is_published=True)[:3]
    return render(
        request,
        "core/home.html",
        {"latest_products": latest_products, "latest_articles": latest_articles},
    )


def about(request):
    return render(request, "core/about.html")


def services(request):
    return render(request, "core/services.html")


def products(request):
    products = Product.objects.prefetch_related("images").all()
    return render(request, "core/products.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = (
        Product.objects.filter(to_products__from_product=product)
        .prefetch_related("images")
        .order_by("to_products__order")
    )

    return render(
        request,
        "core/product_detail.html",
        {"product": product, "related_products": related_products},
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику отправки сообщения
            return render(request, "core/contact.html", {"form": form, "success": True})
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


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

    context = {
        "article": article,
        "content_html": content_html,
        "comments": comments,
        "form": form,
        "related_articles": related_articles,
    }
    return render(request, "core/learning_detail.html", context)


class LearningArticleListView(ListView):
    model = LearningArticle
    template_name = "core/learning.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return LearningArticle.objects.all().order_by("-created_at")


class LearningDetailView(DetailView):
    model = LearningArticle
    template_name = "core/learning_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return LearningArticle.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context["article"]
        # Convert Markdown to HTML
        context["content_html"] = markdown.markdown(
            article.content, extensions=["extra", "codehilite"]
        )
        return context
