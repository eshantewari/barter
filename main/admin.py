from django.contrib import admin

# Register your models here.
from .models import Account, Category, SearchField, Item, Image

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
    
    
class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username','account_id','address', 'reputation']}),
    ]

    inlines = [ItemInline, AccountCategoryInline,]
    list_display = ('username','account_id','address', 'reputation')
    list_filter = ['username']
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
        (None,               {'fields': ['name','owner','description']}),
    ]

    inlines = [ImageInline]
    list_display = ('name', 'owner')
    list_filter = ['name']
    search_fields = ['name']
   
admin.site.register(Account, AccountAdmin) 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)

    





