from django.utils.html import mark_safe
from django.template.loader import render_to_string
from easy_thumbnails.files import get_thumbnailer
from selectable.base import ModelLookup
from selectable.registry import registry
from alibrary.models import *

THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


class BaseLookup(ModelLookup):
    template_name = None
    def get_item_label(self, object):
        return mark_safe(render_to_string(self.template_name, {'object': object}))


class ReleaseNameLookup(BaseLookup):
    model = Release
    search_fields = ['name__icontains', 'catalognumber__istartswith']
    template_name = 'alibrary/lookups/_release.html'

registry.register(ReleaseNameLookup)


class ArtistLookup(BaseLookup):
    model = Artist
    search_fields = ['name__icontains',]
    template_name = 'alibrary/lookups/_artist.html'

registry.register(ArtistLookup)





"""
TODO: refactor lookup toi use generic class & templates
"""
class PlaylistSeriesLookup(ModelLookup):
    model = Series
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html = ''
        html += '<span>%s</span>' % item.name

        return mark_safe(html)
    
    
    
registry.register(PlaylistSeriesLookup)



class ReleaseLabelLookup(ModelLookup):
    model = Label
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html += '<span>%s</span>' % item.name

        return mark_safe(html)



registry.register(ReleaseLabelLookup)


class ParentLabelLookup(ReleaseLabelLookup):
    pass

registry.register(ParentLabelLookup)




class LabelLookup(ModelLookup):
    model = Label
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html += '<span>%s</span>' % item.name

        return mark_safe(html)
    
registry.register(LabelLookup)


class LicenseLookup(ModelLookup):
    model = License
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        return mark_safe(u'%s (%s) <span class="%s">%s</span>' % (item.name, item.restricted, item.key, item.key))
    
    
registry.register(LicenseLookup)
