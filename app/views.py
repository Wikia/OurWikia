import models
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.db.models import Max


def frontpage(request):
    stories = [wiki_hotness.story for wiki_hotness in models.WikiHotness.objects.order_by('-hotness')[:50]]

    return render_to_response('frontpage.html',
                              dict(stories=stories[:50]),
                              context_instance=RequestContext(request))


def subwikia(request, subdomain):
    try:
        wiki = models.Wiki.objects.get(subdomain=subdomain)
    except ObjectDoesNotExist:
        return four_oh_four(request)
    stories = wiki.stories.get_queryset().order_by('-last_updated')
    return render_to_response('subwikia.html',
                              dict(wiki=wiki, stories=stories),
                              context_instance=RequestContext(request))


def comments(request, subdomain, story_id):
    pass


def upvote(request, story_id):
    pass


def downvote(request, story_id):
    pass


def four_oh_four(request):
    return render_to_response('404.html')