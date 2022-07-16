from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _


class HelpCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('help_category')
        verbose_name_plural = _('help_categories')


class HelpSubcategory(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    category = models.ForeignKey(HelpCategory, on_delete=models.PROTECT, verbose_name=_('category'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Help_subcategory')
        verbose_name_plural = _('Help_subcategories')


class HelpModel(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    category = models.ForeignKey(HelpCategory, on_delete=models.PROTECT, verbose_name=_('category'))
    descriptions = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Help_model')
        verbose_name_plural = _('Help_models')
