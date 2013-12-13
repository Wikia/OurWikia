import models
import json
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


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


"""
It's a freaking hackathon, and these are vulnerable to CSRF, and I don't caaaaaaare
"""

@require_POST
@login_required
def upvote(request, story_id):
    try:
        story = models.Story.get(id=story_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'message': 'Story not found'}), status=404)
    try:
        current_downvote = request.user.downvotes.get(story_id=story_id)
        current_downvote.delete()
    except ObjectDoesNotExist:
        pass
    try:
        current_upvote = request.user.upvotes.get(story_id=story_id)
        if request.POST.get('delete'):
            current_upvote.delete()
            return HttpResponse(json.dumps({'message': 'Upvote deleted'}), status=200)
        return HttpResponse(json.dumps({'message': 'Already upvoted'}), status=200)
    except ObjectDoesNotExist:
        if not request.POST.get('delete'):
            new_upvote = models.UpVote()
            new_upvote.story = story
            new_upvote.user = request.user
            new_upvote.save()
    return HttpResponse(json.dumps({'message': 'Upvote successful'}), status=200)




@require_POST
@login_required
def downvote(request, story_id):
    try:
        story = models.Story.get(id=story_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'message': 'Story not found'}), status=404)
    try:
        current_upvote = request.user.upvotes.get(story_id=story_id)
        current_upvote.delete()
    except ObjectDoesNotExist:
        pass
    try:
        current_downvote = request.user.downvotes.get(story_id=story_id)
        if request.POST.get('delete'):
            current_downvote.delete()
            return HttpResponse(json.dumps({'message': 'Downvote deleted'}), status=200)
        return HttpResponse(json.dumps({'message': 'Already Downvoted'}), status=200)
    except ObjectDoesNotExist:
        if not request.POST.get('delete'):
            new_downvote = models.DownVote()
            new_downvote.story = story
            new_downvote.user = request.user
            new_downvote.save()
    return HttpResponse(json.dumps({'message': 'Downvote successful'}), status=200)


def four_oh_four(request):
    return render_to_response('404.html')