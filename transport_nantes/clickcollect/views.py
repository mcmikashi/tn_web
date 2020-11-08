from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from .forms import ClickCollectForm
from .models import ClickableCollectable, ClickAndCollect

# Create your views here.

class GiletReserveView(FormView):
    template_name = 'clickcollect/reserve.html'
    form_class = ClickCollectForm
    #success_url = reverse('click_collect:gilet_reserved')
    success_url = "gr2"         # Why didn't this work with reverse?

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = '/static/asso_tn/images-quentin-boulegon/vélopolitain-1.jpg'
        self.success_url = reverse('click_collect:gilet_reserved')
        context['success_url'] = reverse('click_collect:gilet_reserved')
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        print("Form is valid")
        # print(reverse('click_collect:gilet_reserved'))
        user = form.save(commit=False)
        try:
            user.refresh_from_db()
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            print((user, user.id, user.pk,))
            pass            # I'm not sure this can ever happen.
        print((user, user.pk,))
        if user is None or user.pk is None:
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user is None:
                user = User()   # New user.
                user.username = get_random_string(20)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
        print((user, user.pk,))
        gilet = ClickableCollectable.objects.get(collectable_token='gilet-transport-nantes')
        click_and_collect = ClickAndCollect.objects.create(user=user, collectable=gilet)
        click_and_collect.save()
        print((click_and_collect, click_and_collect.pk,))
        return super(GiletReserveView, self).form_valid(form)

class GiletReservedView(TemplateView):
    template_name = 'clickcollect/reserved.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = '/static/asso_tn/images-quentin-boulegon/vélopolitain-1.jpg'
        # Argument passed is the slug.  This should become a db lookup instead.
        # For the moment, all slugs lead to the laboratoire.
        return context