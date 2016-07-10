from django.db import models


# Create your models here.
class Gallery(models.Model):
    class Meta:
        verbose_name_plural = '게시판'
    title = models.CharField('제목', max_length=50)
    detail = models.TextField('내용')
    created_date = models.DateTimeField()
    categorys = models.ForeignKey('Categorys', verbose_name='카테고리', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/detail/%i/" % self.id


class Image(models.Model):
    class Meta:
        verbose_name_plural = '이미지'
    file = models.FileField('이미지', upload_to='images/')
    gallery = models.ForeignKey('Gallery', related_name='images', blank=True, null=True)
    thumbnail = models.BooleanField('썸네일 지정', default=0)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]


class Categorys(models.Model):
    class Meta:
        verbose_name_plural = '카테고리'
    name = models.CharField('카테고리명', max_length=10)

    def __str__(self):
        return self.name
