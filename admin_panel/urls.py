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
    path('order_list',views.order_list,name='order_list'),
    path('editorder/<product_id>',views.editorder,name='editorder'),
    path('cancelorder/<order_product_id>',views.cancelorder,name='editorder'),
    path('order_history',views.order_history,name='order_history'),
    path('product_offer',views.product_offer,name='product_offer'),
    path('editproductoffer/<int:offer_id>',views.editproductoffer,name='editproductoffer'),
    path('deleteproductoffer/<int:offer_id>',views.deleteproductoffer,name='deleteproductoffer'),
    path('add_productoffer',views.add_productoffer,name="add_productoffer"),

    path('category_offer',views.category_offer,name="category_offer"),
    path('deletecategoryoffer/<int:offer_id>',views.deletecategoryoffer,name='deletecategoryoffer'),
    path('editcategoryoffer/<int:offer_id>',views.editcategoryoffer,name="editcategoryoffer"),
    path('add_categoryoffer',views.add_categoryoffer,name='add_categoryoffer'),



]
