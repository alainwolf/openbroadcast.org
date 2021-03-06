from django.db import models
from django.utils import timezone

from easy_thumbnails import utils, signal_handlers
from easy_thumbnails.conf import settings


class FileManager(models.Manager):

    def get_file(self, storage, name, create=False, update_modified=None,
                 check_cache_miss=False, **kwargs):
        kwargs.update(dict(storage_hash=utils.get_storage_hash(storage),
                           name=name))

        if create:
            if update_modified:
                defaults = kwargs.setdefault('defaults', {})
                defaults['modified'] = update_modified
            try:
                obj, created = self.get_or_create(**kwargs)
            except:
                # hack - don't ask me why this happens...
                return None
        else:
            created = False
            kwargs.pop('defaults', None)
            try:
                manager = self._get_thumbnail_manager()
                obj = manager.get(**kwargs)
            except self.model.DoesNotExist:

                if check_cache_miss and storage.exists(name):
                    # File already in storage, update cache
                    obj = self.create(**kwargs)
                    created = True
                else:
                    return

        if update_modified and not created:
            if obj.modified != update_modified:
                self.filter(pk=obj.pk).update(modified=update_modified)

        return obj

    def _get_thumbnail_manager(self):
        if settings.THUMBNAIL_CACHE_DIMENSIONS:
            return self.select_related("dimensions")
        return self


class File(models.Model):
    storage_hash = models.CharField(max_length=40, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    modified = models.DateTimeField(default=timezone.now)

    objects = FileManager()

    class Meta:
        abstract = True
        unique_together = (('storage_hash', 'name'),)

    def __unicode__(self):
        return self.name


class Source(File):
    pass


class Thumbnail(File):
    source = models.ForeignKey(Source, related_name='thumbnails')

    class Meta:
        unique_together = (('storage_hash', 'name', 'source'),)


class ThumbnailDimensions(models.Model):
    thumbnail = models.OneToOneField(Thumbnail, related_name="dimensions")
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return "%sx%s" % (self.width, self.height)

    @property
    def size(self):
        return self.width, self.height


models.signals.pre_save.connect(signal_handlers.find_uncommitted_filefields)
models.signals.post_save.connect(signal_handlers.signal_committed_filefields)
