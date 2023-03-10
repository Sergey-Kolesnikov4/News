from django.db.models.signals import m2m_changed
from django.dispatch import receiver



from news.models import News
from .tasks import send_notifications




@receiver(m2m_changed,sender=News.category.through)
def notify_about_new_post(sender,instance, **kwargs):
    if kwargs['action']=='post_add':
        categories=instance.category.all()
        subscribers:list[str]=[]
        for category in categories:
            subscribers+=category.subscribers.all()

        subscribers=[s.email for s in subscribers]

        send_notifications.delay(instance.preview(),instance.pk,instance.title,subscribers)