"""
Denormalizes hottest story per wiki
"""
from app import models


def run():
    for wiki in models.Wiki.objects.order_by('-wam_score').all():
        wiki.update_hotness()
        wiki.save()