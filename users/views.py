import asyncio

import telegram
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from OnlineStore.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from checkout.models import Order
from .forms import CreationForm, FeedbackForm
from .models import Feedback


@login_required
def user_orders(request):

    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('store:home')
    template_name = 'users/signup.html'



async def send_telegram_message(message):

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = TELEGRAM_CHAT_ID
    await bot.send_message(chat_id=chat_id, text=message)


def feedback_processing(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                feedback_name=form.cleaned_data['feedback_name'],
                feedback_email=form.cleaned_data['feedback_email'],
                feedback_message=form.cleaned_data['feedback_message'],
            )
            feedback.save()

            message = f"Новое сообщение от {feedback.feedback_name} ({feedback.feedback_email}): {feedback.feedback_message}"
            asyncio.run(send_telegram_message(message))

            return render(request, 'users/feedback_success.html')
    return render(request, 'users/feedback_failed.html')

# views.py
from django.shortcuts import render
from .models import Product
import numpy as np
import joblib

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search(request):
    query = request.GET.get('q')
    if query:
        vectorizer = joblib.load('vectorizer.pkl')
        query_vector = vectorizer.vectorize(query)

        products = Product.objects.all()
        product_vectors = [(product, vectorizer.vectorize(product.description)) for product in products]

        results = sorted(product_vectors, key=lambda x: cosine_similarity(query_vector, x[1]), reverse=True)
        results = [product[0] for product in results]

        return render(request, 'search_results.html', {'results': results})
    return render(request, 'search.html')
