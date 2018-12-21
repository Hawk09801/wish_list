"""lista_prezentow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.views.static import serve
from wish_list.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login$', LoginUserView.as_view(), name='login'),	# strona do logowania
    url(r'^logout$', LogoutView.as_view()),     # wylogowanie
    url(r'^add_account$', AddUserView.as_view()),   # tworzenie konta
    url(r'^(?P<pk>(\d)+)/add_list$', AddGiftListView.as_view()),          # tworzenie listy prezentów
    url(r'^(?P<user_id>(\d)+)/(?P<list_id>(\d)+)/addGift$', AddGiftToListView.as_view()),
    url(r'^(?P<user_id>(\d)+)/(?P<list_id>(\d)+)$', ListDetailView.as_view(), name='showList'),           # szczegóły listy prezentów
    url(r'^showUser/(?P<user_id>(\d)+)$', ShowUserView.as_view(), name='showUser'),
    url(r'^(?P<user_id>(\d)+)/(?P<list_id>(\d)+)/(?P<gift_id>(\d)+)$', EditGiftView.as_view()),
    url(r'^(?P<user_id>(\d)+)/(?P<list_id>(\d)+)/(?P<gift_id>(\d)+)/delete$', DeleteGiftView.as_view()),
    url(r'^take/(?P<user_id>(\d)+)/(?P<list_id>(\d)+)/(?P<gift_id>(\d)+)$', TakeGiftView.as_view()),
    url(r'^leave/(?P<user_id>(\d)+)/(?P<list_id>(\d)+)/(?P<gift_id>(\d)+)$', LeaveGiftView.as_view()),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^search$', SearchView.as_view()),
    url(r'^edit/(?P<user_id>(\d)+)$', EditUserView.as_view()),
    url(r'^edit/(?P<user_id>(\d)+)/editPassword$', EditPasswordView.as_view()),
    url(r'^(?P<user_id>(\d)+)/(?P<list_id>(\d)+)/delete$', DeleteListView.as_view()),
    url(r'^(?P<user_id>(\d)+)/addFundraiser$', AddFundraiserView.as_view()),
    url(r'^(?P<user_id>(\d)+)/fundraiser/(?P<fundraiser_id>(\d)+)$', FundraiserDetailView.as_view()),
    url(r'^(?P<user_id>(\d)+)/fundraiser/(?P<fundraiser_id>(\d)+)/addDonor$', AddDonorView.as_view()),
    url(r'^(?P<user_id>(\d)+)/fundraiser/(?P<fundraiser_id>(\d)+)/delete$', DeleteFundraiserView.as_view()),
    url(r'^(?P<user_id>(\d)+)/fundraiser/(?P<fundraiser_id>(\d)+)/(?P<donor_id>(\d)+)$', CancelDonorView.as_view()),
    url(r'^(?P<user_id>(\d)+)/fundraiser/(?P<fundraiser_id>(\d)+)/edit$', EditFundraiserView.as_view()),
    url(r'^(?P<user_id>(\d)+)/fundraiser/(?P<fundraiser_id>(\d)+)/(?P<donor_id>(\d)+)/edit$', EditDonorView.as_view()),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/favicon.ico')),


]

#w trybie debug możemy dodać ten adres do naszych ścieżek url
if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
