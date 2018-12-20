from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import *
from .models import *



# Logowanie użytkownika
class LoginUserView(View):

    def get(self, request):
        form = LoginUserForm()
        return render(request, 'wish_list/loginUser.html', {'form': form})

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                return redirect('main')
        else:
            return render(request, 'wish_list/loginUser.html', {'form': form})       # info dlaczego i przekierowanie


# wylogowanie
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)                  # wyloguj
            return redirect("main")
        return render (request, 'wish_list/loginUser.html')


# tworzenie użytkownika
class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'wish_list/addUser.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('email')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            return redirect("/login")
        return render(request, 'wish_list/addUser.html', {'form': form})


# tworzenie listy
class AddGiftListView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = List
    fields = ['name']

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(AddGiftListView, self).form_valid(form)

    def get_success_url(self):
        user_id = self.request.user.pk
        list_id = self.object.pk
        return reverse_lazy("showList", kwargs={'user_id': user_id, 'list_id': list_id})


# dodawanie prezentów do listy
class AddGiftToListView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id):
        user = User.objects.get(pk=user_id)
        wish_list = List.objects.get(pk=list_id)
        if user != request.user:
            return redirect('main')
        else:
            form = AddGiftToListForm()
            return render(request, 'wish_list/addGift.html', {'form': form, 'user_id': user, 'list_id': wish_list})

    def post(self, request, user_id, list_id):
        form = AddGiftToListForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            desciption = form.cleaned_data.get('desciption')
            shop = form.cleaned_data.get('shop')
            file = form.cleaned_data.get('file')
            wish_list = List.objects.get(pk=list_id)
            Gifts.objects.create(name=name, desciption=desciption, shop=shop, file=file, wish_list=wish_list)
            cxt = {'user': User.objects.get(pk=user_id), 'wish_list': wish_list, 'gifts': Gifts.objects.filter(wish_list=wish_list)}
        return render(request, 'wish_list/listDetail.html', cxt)


# widok listy prezentów
class ListDetailView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id):
        user = User.objects.get(pk=user_id)
        wish_list = List.objects.get(pk=list_id)
        gifts = Gifts.objects.filter(wish_list=wish_list)
        cxt = {'user': user, 'wish_list': wish_list, 'gifts': gifts}
        return render(request, 'wish_list/listDetail.html', cxt)


# widok osoby
class ShowUserView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        lists = List.objects.filter(user=user)
        fundraisers = Fundraiser.objects.filter(user=user)
        return render(request, 'wish_list/showUser.html', {'user': user, 'lists': lists, 'fundraisers': fundraisers})



# edycja prezentu
class EditGiftView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id, gift_id):
        user = User.objects.get(pk=user_id)
        gift = Gifts.objects.get(pk=gift_id)
        form = EditGiftForm(instance=gift)
        if user != request.user:
            return redirect('main')
        else:
            return render(request, 'wish_list/editGift.html', {'form': form})

    def post(self, request, user_id, list_id, gift_id):
        gift = Gifts.objects.get(pk=gift_id)
        form = EditGiftForm(request.POST, request.FILES, instance=gift)
        if form.is_valid():
            form.save()
        return redirect("/%s/%s" % (user_id, list_id))


# Usuwanie prezentu
class DeleteGiftView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id, gift_id):
        user = User.objects.get(pk=user_id)
        gift = Gifts.objects.get(pk=gift_id)
        if user != request.user:
            return redirect('main')
        else:
            gift.delete()
            return redirect("/%s/%s" % (user_id, list_id))


# zapisywanie się na prezent
class TakeGiftView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id, gift_id):
        gift = Gifts.objects.get(pk=gift_id)
        gift.person = request.user
        gift.save()
        return redirect("/%s/%s" % (user_id, list_id))

# wypisywanie się z prezentu
class LeaveGiftView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id, gift_id):
        gift = Gifts.objects.get(pk=gift_id)
        gift.person = None
        gift.save()
        return redirect("/%s/%s" % (user_id, list_id))


# strona główna
class MainView(View):
    def get(self, request):
        return render(request, 'wish_list/main.html')


# wyszukiwarka
class SearchView(View):
    def get(self, request):
        form = SearchForm()
        return render(request, 'wish_list/search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        users = []
        if form.is_valid():
            last_name = form.cleaned_data.get("last_name")
            users = User.objects.filter(last_name__icontains=last_name)
        return render(request, 'wish_list/search.html', {'form': form, 'users': users})


# edycja użytkownika
class EditUserView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id):
        person = User.objects.get(pk=user_id)
        if person != request.user:
            return redirect('main')
        else:
            form = EditUserForm(instance=person)
            return render(request, 'wish_list/editUser.html', {'form': form})

    def post(self, request, user_id):
        form = EditUserForm(request.POST)
        user = User.objects.get(pk=user_id)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
        return redirect('/showUser/%s' % user.id)


# zmiana hasła
class EditPasswordView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        if user != request.user:
            return redirect('main')
        else:
            form = EditPasswordForm()
            return render(request, "wish_list/editPassword.html", {'form': form})

    def post(self, request, user_id):
        form = EditPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            u = User.objects.get(pk=user_id)
            u.set_password(new_password)
            u.save()
            return redirect('/showUser/%s' % u.id)
        return render(request, "wish_list/editPassword.html", {'form': form})


# usunięcie listy prezentów
class DeleteListView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, list_id):
        u = User.objects.get(pk=user_id)
        if u != request.user:
            return redirect('main')
        else:
            wish_list = List.objects.get(pk=list_id)
            wish_list.delete()
            return redirect('/showUser/%s' % u.id)


# dodanie zbiórki pieniędzy
class AddFundraiserView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id):
        form = AddFundraiserForm()
        user = User.objects.get(pk=user_id)
        if user != request.user:
            return redirect('main')
        else:
            return render(request, 'wish_list/addFundraiser.html', {'form': form})

    def post(self, request, user_id):
        form = AddFundraiserForm(request.POST)
        if form.is_valid():
            goal = form.cleaned_data.get('goal')
            desciption = form.cleaned_data.get('desciption')
            amount = form.cleaned_data.get('amount')
            user = User.objects.get(pk=user_id)
            new_fundraiser = Fundraiser.objects.create(goal=goal, desciption=desciption, amount=amount, user=user)
        return redirect('/%s/fundraiser/%s' % (user_id, new_fundraiser.id))

# wyświetlenie widoku zbiórki
class FundraiserDetailView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, fundraiser_id):
        user = User.objects.get(pk=user_id)
        fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        donors = Donors.objects.filter(fundraiser=fundraiser_id)
        result = 0
        for donor in donors:
            result += donor.amount
        return render(request, 'wish_list/showFundraiser.html', {'user': user, 'fundraiser': fundraiser, 'donors':donors, 'result':result})


# dodawanie składki od osoby
class AddDonorView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, fundraiser_id):
        fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        form = AddDonorForm()
        return render(request, 'wish_list/addDonor.html', {'form': form, 'fundraiser': fundraiser})

    def post(self, request, user_id, fundraiser_id):
        form = AddDonorForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            user = request.user
            fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
            Donors.objects.create(amount=amount, user=user, fundraiser=fundraiser)
        return redirect('/%s/fundraiser/%s' % (user_id, fundraiser_id))


# usunięcie zbiórki
class DeleteFundraiserView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, fundraiser_id):
        u = User.objects.get(pk=user_id)
        if u != request.user:
            return redirect('main')
        else:
            fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
            fundraiser.delete()
            return redirect('/showUser/%s' % u.id)


# anulowanie składki
class CancelDonorView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, fundraiser_id, donor_id):
        donor = Donors.objects.get(pk=donor_id)
        donor.delete()
        return redirect("/%s/fundraiser/%s" % (user_id, fundraiser_id))

# edycja zrzutki
class EditFundraiserView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, fundraiser_id):
        user = User.objects.get(pk=user_id)
        fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        form = AddFundraiserForm(instance=fundraiser)
        if user != request.user:
            return redirect('main')
        else:
            return render(request, 'wish_list/addFundraiser.html', {'form': form})

    def post(self, request, user_id, fundraiser_id):
        fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        form = AddFundraiserForm(request.POST, instance=fundraiser)
        if form.is_valid():
            form.save()
        return redirect("/%s/fundraiser/%s" % (user_id, fundraiser_id))


# edycja składki
class EditDonorView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id, fundraiser_id, donor_id):
        donor = Donors.objects.get(pk=donor_id)
        if donor.user != request.user:
            return redirect('main')
        else:
            form = AddDonorForm(instance=donor)
            return render(request, 'wish_list/addDonor.html', {'form': form})

    def post(self, request, user_id, fundraiser_id, donor_id):
        donor = Donors.objects.get(pk=donor_id)
        form = AddDonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
        return redirect("/%s/fundraiser/%s" % (user_id, fundraiser_id))


