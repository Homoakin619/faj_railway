from core import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.HomepageView.as_view(),name='home'),
    path('login/',views.LoginRegisterView.as_view(),name='login'),
    path('create/',views.AdminAddPostView.as_view(),name='create_post'),
    path('edit/<int:pk>',views.AdminEditPostView.as_view(),name='edit_post'),
    path('dashboard/',views.AdminDashboardView.as_view(),name='dashboard'),
    path('all_posts/',views.AdminAllPosts.as_view(),name='all_posts'),
    path('user/<int:pk>/',views.AdminEditUserView.as_view(),name='edit_user'),
    path('logout/',views.logout_user,name='logout'),
    path('not_verified/',views.RedirectPage.as_view(),name='not_verified'),
    path('contents/<int:pk>/',views.PostDetail.as_view(),name='post_detail'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)