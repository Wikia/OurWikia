"""
Updates the hotness of all stories
"""

from app.models import Story


def run():
    for story in Story.objects.all().order_by('-last_updated'):
        story.update_hotness()
        story.save()