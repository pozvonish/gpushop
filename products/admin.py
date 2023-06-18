from django.contrib import admin
from django.db import transaction
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

    actions = ['swap_records']

    def swap_records(self, request, queryset):
        # Проверка, что выбрано ровно две записи
        if queryset.count() != 2:
            self.message_user(request, "Выберите две записи для обмена.", level='error')
            return

        record1, record2 = queryset

        with transaction.atomic():
            record1.name, record2.name = record2.name, record1.name
            record1.save()
            record2.save()

        self.message_user(request, "Записи успешно обменяны.")

    swap_records.short_description = "Обменять записи"

    class Meta:
        model=ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines=[ProductImageInline]
    class Meta:
        model=Product

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model=ProductImage

admin.site.register(ProductImage, ProductImageAdmin)