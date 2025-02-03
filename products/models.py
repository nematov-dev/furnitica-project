from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from common.models import BaseModel


UserModel = get_user_model()


class ProductCategoryModel(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('title'))
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='children',
        verbose_name=_('parent')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class ProductTagModel(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product tag')
        verbose_name_plural = _('product tags')

class ProductSizeModel(BaseModel):
    title = models.CharField(max_length=128, verbose_name=_('title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product size')
        verbose_name_plural = _('product sizes')

class ProductManufactureModel(BaseModel):
    logo = models.ImageField(upload_to='brends',null=True,blank=True,verbose_name='logo')
    name = models.CharField(max_length=128, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product manufacture')
        verbose_name_plural = _('product manufactures')

class ProductColorModel(BaseModel):
    code = models.CharField(max_length=7,verbose_name=_('code'))
    title = models.CharField(max_length=64, verbose_name=_('title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product color')
        verbose_name_plural = _('product colors')

class ProductModel(BaseModel):
    image1 = models.ImageField(upload_to='products', verbose_name=_('image1'))
    image2 = models.ImageField(upload_to='products', verbose_name=_('image2'))
    title = models.CharField(max_length=128, verbose_name=_('title'))
    short_description = models.TextField(verbose_name=_('short description'))
    long_description = models.TextField(verbose_name=_('long description'))
    sku = models.CharField(max_length=7,verbose_name=_('sku'))
    in_stock = models.BooleanField(default=True,verbose_name=_('in_stock'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('quantity'))
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name=_('price'),validators=[MinValueValidator(0)])
    discount = models.SmallIntegerField(
        verbose_name=_('discount'), null=True, blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)])
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name=_('discount_price'),
        null=True, blank=True
    )


    colors = models.ManyToManyField(ProductColorModel,verbose_name=_('colors'),related_name='products')
    sizes = models.ManyToManyField(ProductSizeModel,verbose_name=_('sizes'),related_name='products')
    tags = models.ManyToManyField(ProductTagModel,verbose_name=_('tags'),related_name='products')
    colors = models.ManyToManyField(ProductColorModel,verbose_name=_('colors'),related_name='products')
    categories = models.ManyToManyField(ProductCategoryModel,verbose_name=_('categories'),related_name='products')

    brands = models.ForeignKey(
        ProductManufactureModel,
        on_delete=models.PROTECT,
        verbose_name=_('brands'),
        related_name='products'
        )

class ProductCommentModel(BaseModel):
    comment = models.CharField(max_length=128, verbose_name=_('comment'))
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='product_comments',
        verbose_name=_('user')
    )
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('product')
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('product comment')
        verbose_name_plural = _('product comments')


class ProductImageModel(models.Model):
    image = models.ImageField(upload_to='products',verbose_name=_('image'))
    products = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='images',verbose_name=_('products'))
