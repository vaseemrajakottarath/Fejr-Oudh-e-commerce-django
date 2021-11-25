from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin, name='adminlogin'),
    path('admindash',views.admindash, name='admindash'),
    path('category',views.category,name='category'),
    path('product',views.product,name='product'),
    path('deletecategory/<cat_id>', views.deletecategory,name='deletecategory'),
    path('deleteproduct/<cat_id>', views.deleteproduct,name='deleteproduct'),
    path('editcat/<cat_id>', views.editcat,name='editcat'),
    path('addcat',views.addcat,name='addcat'),
    path('editproduct/<cat_id>', views.editproduct,name='editproduct'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('brand',views.brand,name='brand'),
    path('deletebrand/<cat_id>', views.deletebrand,name='deletebrand'),
    path('editbrand/<cat_id>',views.editbrand,name='editbrand'),
    path('addbrand',views.addbrand,name='addbrand'),
    path('usermanage',views.usermanage,name='usermanage'),
    path('deleteuser/<user_id>', views.deleteuser,name='deleteuser'),
    path('blockuser/<user_id>', views.blockuser,name='blockuser'),
    path('unblockuser/<user_id>', views.unblockuser,name='unblockuser'),


]
