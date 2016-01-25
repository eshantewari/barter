from django.contrib import admin

# Register your models here.
from .models import User, Category, SearchField, Item, Image, User, Address

class AddressInline(admin.TabularInline):
    model = Address

class AccountCategoryInline(admin.TabularInline):
    model = Category.users.through
    extra = 1

class SearchFieldInline(admin.TabularInline):
    model = SearchField
    extra = 1

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information',               {'fields': ['username','first_name', 'last_name', 'email']}),
        ('Account Information', {'fields':['reputation',]}),
        ('Boolean Fields', {'fields':['is_active', 'is_staff']}),
    ]
    inlines = [AddressInline, ]
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_filter=['username']
    search_fields = ['username']

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','description']}),
    ]

    inlines = [ItemInline, AccountCategoryInline,]
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','owner','description', 'category']}),
    ]

    inlines = [ImageInline]
    list_display = ('name', 'owner', 'category')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
