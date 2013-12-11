from app.models import Wiki


def run():
    for wiki in Wiki.objects.all():
        print wiki.title
        wiki.seed_stories()