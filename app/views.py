import models
import json
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def _get_votes_from_user_and_story_ids(user, story_ids):
    curr_upvotes = []
    curr_downvotes = []
    if user.is_authenticated():
        curr_upvotes = [u.story_id for u in models.UpVote.objects.filter(story__id__in=story_ids, user=user)]
        curr_downvotes = [d.story_id for d in models.DownVote.objects.filter(story__id__in=story_ids, user=user)]
    return curr_upvotes, curr_downvotes


def frontpage(request):
    stories = [wiki_hotness.story for wiki_hotness in models.WikiHotness.objects.order_by('-hotness')[:50]]
    curr_upvotes, curr_downvotes = _get_votes_from_user_and_story_ids(request.user, [s.id for s in stories])
    print curr_upvotes, curr_downvotes
    return render_to_response('frontpage.html',
                              dict(stories=stories[:50], curr_downvotes=curr_downvotes, curr_upvotes=curr_upvotes),
                              context_instance=RequestContext(request))


def subwikia(request, subdomain):
    try:
        wiki = models.Wiki.objects.get(subdomain=subdomain)
    except ObjectDoesNotExist:
        return four_oh_four(request)
    stories = wiki.stories.get_queryset().order_by('-last_updated')
    curr_upvotes, curr_downvotes = _get_votes_from_user_and_story_ids(request.user, [s.id for s in stories])
    return render_to_response('subwikia.html',
                              dict(wiki=wiki, stories=stories, curr_downvotes=curr_downvotes, curr_upvotes=curr_upvotes),
                              context_instance=RequestContext(request))


def comments(request, subdomain, story_id):
    pass


"""
It's a freaking hackathon, and these are vulnerable to CSRF, and I don't caaaaaaare
"""

@require_POST
@login_required
@csrf_exempt
def upvote(request, story_id):
    try:
        story = models.Story.objects.get(id=story_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'message': 'Story not found'}), status=404)
    try:
        current_downvote = models.DownVote.objects.get(story=story, user=request.user)
        current_downvote.delete()
    except ObjectDoesNotExist:
        pass
    try:
        current_upvote = models.UpVote.objects.get(story=story, user=request.user)
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
@csrf_exempt
def downvote(request, story_id):
    try:
        story = models.Story.objects.get(id=story_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'message': 'Story not found'}), status=404)
    try:
        current_upvote = models.UpVote.objects.get(story=story, user=request.user)
        current_upvote.delete()
    except ObjectDoesNotExist:
        pass
    try:
        current_downvote = models.DownVote.objects.get(story=story, user=request.user)
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