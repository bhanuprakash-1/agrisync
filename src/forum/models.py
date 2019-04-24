from oauth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.urls import reverse


class TopicQuery(models.query.QuerySet):
    def search(self, query):
        if query:
            return self.filter(
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__icontains=query) |
                Q(answer__content__icontains=query)
            ).distinct()
        else:
            return self.none()


class TopicManager(models.Manager):
    def get_topic_queryset(self):
        return TopicQuery(self.model, using=self._db)

    def search(self, query):
        return self.get_topic_queryset().search(query)


class Topic(models.Model):
    CAT_CHOICES = (
        ('Q', 'Question'),
        ('I', 'Improvement'),
        ('S', 'Suggestion'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author of topic")
    category = models.CharField(max_length=3, choices=CAT_CHOICES, default='Q')
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=60, blank=True, null=True, default=None)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    objects = TopicManager()

    @property
    def number_of_answers(self):
        return self.answer_set.count()

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'slug': self.slug})

    def tags_as_list(self):
        if self.tags == '' or not self.tags:
            return ''
        return sorted(self.tags.split(','))

    def __str__(self):
        return self.title


def topic_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(topic_pre_save_receiver, sender=Topic)


class Answer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="topic of answer")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author of the answer")
    # content = RichTextUploadingField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return self.topic.get_absolute_url()

    def __str__(self):
        return "On: " + str(self.topic.title) + " by " + str(self.author.first_name) + " " + str(
            self.author.last_name)
