from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime

from news.models import News,Category
from NewsPaper import settings


@shared_task
def send_notifications(preview,pk,title,subscribers ):
    html_content = render_to_string('post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg=EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content,'text/html')
    msg.send()

@shared_task
def weekly_news():
    today=datetime.datetime.now()
    last_week=today - datetime.timedelta(days=7)
    news=News.objects.filter(dateCreation__gte=last_week)
    categories = set(news.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email',flat=True))

    html_content=render_to_string(
        'news_last_week.html',
        {
            'link':settings.SITE_URL,
            'news': news,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за последнюю неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content,'text/html')
    msg.send()




