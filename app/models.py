from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from pytz import utc
from django.db.utils import IntegrityError
import math
import time
import requests
import datetime


class Wiki(models.Model):
    wordmark = models.URLField(max_length=1024, null=True)
    title = models.TextField(null=True)
    wam_score = models.FloatField(default=0)
    desc = models.TextField(null=True)
    subdomain = models.TextField(unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    url = models.URLField(max_length=1024, null=True)
    headline = models.TextField(null=True)
    edits = models.IntegerField(null=True)
    articles = models.IntegerField(null=True)
    pages = models.IntegerField(null=True)
    users = models.IntegerField(null=True)
    active_users = models.IntegerField(null=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def seed_data(cls, wiki_id):
        try:
            wiki = cls.objects.get(id=wiki_id)
        except ObjectDoesNotExist:
            wiki = cls()
            wiki.id = wiki_id
        response = requests.get('http://www.wikia.com/api/v1/Wikis/Details', params={'ids': wiki_id})
        if response.status_code is not 200:
            return False
        resp = response.json()
        if len(resp['items']) == 0:
            return False
        data = resp['items'][str(wiki_id)]
        subdomain = wiki.url_to_subdomain(data['url'])
        if subdomain.startswith('qatestwiki'):
            if wiki.id is not None:
                wiki.delete()
            return False
        wiki.title = data['title']
        wiki.desc = data['desc']
        wiki.wordmark = data['wordmark']
        wiki.wam_score = float(data['wam_score'])
        wiki.url = data['url']
        wiki.subdomain = subdomain
        wiki.headline = data.get('headline')
        stats = data.get('stats', {})
        wiki.edits = stats.get('edits')
        wiki.articles = stats.get('articles')
        wiki.pages = stats.get('pages')
        wiki.users = stats.get('users')
        wiki.active_users = stats.get('activeUsers')
        top_user_ids = data.get('topUsers', [])
        try:
            wiki.save()
        except IntegrityError:
            return False  #screw it, we don't really use the ID after this -- just the URL
        if len(top_user_ids):
            map(lambda x: x.delete(), wiki.top_users.all())
            posish = 1
            for wikia_user in filter(lambda x: x, wiki.get_wikia_users([int(uid) for uid in top_user_ids])):
                top = TopWikiaUsers()
                top.wiki = wiki
                top.position = posish
                top.wikia_user = wikia_user
                top.save()
                posish += 1
        return True

    def get_top_users(self):
        return [tu.wikia_user for tu in self.top_users.get_queryset().order_by('position')]

    @classmethod
    def url_to_subdomain(cls, url):
        splt = url.replace('http://', '').split('.')
        if splt[1] != 'wikia':
            return splt[1]
        return splt[0]

    def get_wikia_user(self, user_id):
        try:
            user = WikiaUser.objects.get(wikia_user_id=user_id, wiki=self)
        except ObjectDoesNotExist:
            response = requests.get(self.url+'/api/v1/User/Details', params={'ids': user_id})
            if response.status_code is not 200:
                return None
            items = response.json()['items']
            data = items[0]
            if len(items) == 0:
                return None
            user = WikiaUser()
            user.wikia_user_id = user_id
            user.name = data['name']
            user.url = data['url']
            user.avatar = data['avatar']
            user.wiki = self
            user.save()
        return user

    def get_wikia_users(self, user_ids):
        users = []
        missing_ids = []
        for user_id in user_ids:
            try:
                users += [WikiaUser.objects.get(wikia_user_id=user_id, wiki=self)]
            except ObjectDoesNotExist:
                missing_ids += [user_id]
        if len(missing_ids) > 0:
            response = requests.get(self.url+'/api/v1/User/Details',
                                    params={'ids': ','.join([str(uid) for uid in missing_ids])})
            if response.status_code is not 200:
                return users
            try:
                items = response.json()['items']
            except ValueError:
                return users
            if len(items) == 0:
                return users
            for data in items:
                user = WikiaUser()
                user.wikia_user_id = int(data['user_id'])
                user.name = data['name']
                user.url = data['url']
                user.avatar = data['avatar']
                user.wiki = self
                user.save()
                users += [user]
        return users

    def seed_stories(self):
        activity_params = {'limit': 50, 'namespaces': '0', 'allowDuplicates': 'false'}
        activity_response = requests.get(self.url+'/api/v1/Activity/LatestActivity', params=activity_params)
        if activity_response.status_code is not 200:
            print activity_response.content
            return False
        activity_items = activity_response.json()['items']
        if len(activity_items) == 0:
            return False
        detail_params = {'ids': ','.join([str(item['article']) for item in activity_items]),
                         'abstract': 120, 'width': 200, 'height': 200}
        detail_response = requests.get(self.url+'/api/v1/Articles/Details', params=detail_params)
        if detail_response.status_code is not 200:
            return False
        detail_items = detail_response.json()['items']
        map(self._story_from_detail, detail_items.values())
        return True

    def _story_from_detail(self, detail):
        try:
            story = Story.objects.get(article_id=int(detail['id']))
        except ObjectDoesNotExist:
            story = Story()
            story.article_id = int(detail['id'])
        story.title = detail['title']
        story.url = detail['url']
        story.wiki = self
        story.abstract = detail['abstract']
        story.last_editor = self.get_wikia_user(detail['revision']['user_id'])
        story.last_updated = datetime.datetime.fromtimestamp(int(detail['revision']['timestamp']), tz=utc)
        story.thumbnail = detail['thumbnail']
        story.save()

    def update_hotness(self):
        hottest_story = self.stories.order_by('-hotness').first()
        if not hottest_story:
            self.hotness_updated = True
            return
        try:
            hotness = WikiHotness.objects.get(wiki=self)
        except ObjectDoesNotExist:
            hotness = WikiHotness()
            hotness.wiki = self

        hotness.story = hottest_story
        hotness.hotness = hottest_story.hotness
        hotness.save()
        self.hotness_updated = True

    def save(self, *args, **kwargs):
        if not hasattr(self, 'hotness_updated'):
            self.update_hotness()
        super(Wiki, self).save()


class WikiaUser(models.Model):
    name = models.TextField()
    url = models.TextField()
    avatar = models.URLField(max_length=1024)
    wikia_user_id = models.IntegerField(null=True)
    wiki = models.ForeignKey(Wiki, related_name='wikia_users')

    class Meta:
        unique_together = ('wikia_user_id', 'wiki')


class TopWikiaUsers(models.Model):
    position = models.IntegerField()
    wikia_user = models.ForeignKey(WikiaUser)
    wiki = models.ForeignKey(Wiki, related_name='top_users')

    class Meta:
        unique_together = ('position', 'wikia_user', 'wiki')


class Story(models.Model):
    article_id = models.IntegerField()
    wiki = models.ForeignKey(Wiki, related_name='stories')
    title = models.TextField()
    thumbnail = models.URLField(max_length=1024, null=True)
    abstract = models.TextField(null=True)
    total_upvotes = models.IntegerField(default=0)
    total_downvotes = models.IntegerField(default=0)
    last_editor = models.ForeignKey(WikiaUser, related_name='edits', null=True)
    last_updated = models.DateTimeField()
    hotness = models.FloatField(null=True)

    class Meta:
        unique_together = ('article_id', 'wiki')

    def __unicode__(self):
        return self.title

    def update_hotness(self):
        karma_total = self.upvotes.count() - self.downvotes.count() + (self.wiki.wam_score / 100)
        seconds = int(time.mktime(self.last_updated.timetuple())) - 1134028003
        sign = 0
        order = math.log(max([abs(karma_total), 1]), 10)
        if karma_total > 0:
            sign = 1
        elif karma_total < 0:
            sign = -1
        self.hotness = round(order + sign * seconds / 45000, 7)
        self.hotness_updated = True

    def get_score(self):
        return int(self.upvotes.count() - self.downvotes.count())

    def save(self, *args, **kwargs):
        if not hasattr(self, 'hotness_updated'):
            self.update_hotness()
        super(Story, self).save()


class UpVote(models.Model):
    story = models.ForeignKey(Story, related_name='upvotes')
    user = models.ForeignKey(User, related_name='upvotes')


class DownVote(models.Model):
    story = models.ForeignKey(Story, related_name='downvotes')
    user = models.ForeignKey(User, related_name='downvotes')


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name='comments')
    parent = models.ForeignKey('self', related_name='children')


class WikiHotness(models.Model):
    wiki = models.OneToOneField(Wiki, related_name='hotness')
    story = models.OneToOneField(Story, related_name='wiki_hotness')
    hotness = models.FloatField()
