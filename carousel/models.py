from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _


class CarouselModel(models.Model):
    title = models.CharField(max_length=400, verbose_name=_('title'))
    descriptions = RichTextUploadingField(verbose_name=_('descriptions'))
    background_image = models.FileField(upload_to='carousel-image', verbose_name=_('background_image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('carousel')
        verbose_name_plural = _('carousels')
        ordering = ['title']