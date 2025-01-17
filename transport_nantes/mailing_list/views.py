import logging
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        LoginRequiredMixin)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import ListView, FormView

from asso_tn.views import AssoView
from .forms import (MailingListSignupForm, QuickMailingListSignupForm,
                    QuickPetitionSignupForm,
                    FirstStepQuickMailingListSignupForm)
from .models import MailingList, Petition
from .events import (user_subscribe_count, subscriber_count,
                     subscribe_user_to_list)

logger = logging.getLogger("django")


class MailingListSignup(FormView):
    template_name = 'mailing_list/signup_m.html'
    merci_template = 'mailing_list/merci_m.html'
    form_class = MailingListSignupForm
    # success_url = reverse_lazy('mailing_list:list_ok')

    # We don't currently populate this form with the user's current
    # subscriptions.  If the user is logged in, we should.  This then
    # becomes the edit form as well.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = ('asso_tn/images-libres/'
                                 'black-and-white-bridge-children-194009-1000'
                                 '.jpg')
        context['hero_title'] = 'Newsletter'
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        subscribe = False
        user = form.save(commit=False)
        try:
            user.refresh_from_db()
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            pass            # I'm not sure this can ever happen.
        if user is None or user.pk is None:
            user = User.objects.filter(
                email=form.cleaned_data['email']).first()
            if user is None:
                user = User()   # New user.
                user.username = get_random_string(20)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
        user.save()
        user.profile.commune = form.cleaned_data['commune']
        user.profile.code_postal = form.cleaned_data['code_postal']
        user.profile.save()
        for newsletter in form.cleaned_data['newsletters']:
            subscribe_user_to_list(user, newsletter)
            # At some point we should also store the last known
            # subscription state in a table with foreign key user.  If
            # the user is in that table, we use it, otherwise we look
            # up in mailing_list_events.  (We'll always need this
            # extra lookup, because a newly created list won't
            # populate users' current (unsubscribed) state.
            #
            # We should wait until this is a performance issue, however.
            subscribe = True
        if subscribe:
            template_name = "mailing_list/merci_m.html"
            return render(self.request, template_name, {'user': user})
        return super(MailingListSignup, self).form_valid(form)


class QuickMailingListSignup(FormView):
    template_name = 'mailing_list/quick_signup_m.html'
    form_class = FirstStepQuickMailingListSignupForm

    def form_valid(self, form):
        self.good_form = form
        if isinstance(form, FirstStepQuickMailingListSignupForm):
            form = QuickMailingListSignupForm()
            form["email"].initial = self.good_form.cleaned_data['email']
            form["mailinglist"].initial = \
                self.good_form.cleaned_data['mailinglist']
            return render(self.request, self.template_name, {"form": form})
        elif isinstance(form, QuickMailingListSignupForm):
            self.template_name = "mailing_list/merci_m.html"
            """Process a valid MailingListSignupForm.

            This method is called when valid form data has been POSTed.
            It returns an HttpResponse.
            """
            # Get user or None.
            user = User.objects.filter(
                email=form.cleaned_data['email']).first()
            if user is None:
                user = User()   # New user.
                user.username = get_random_string(20)
                user.email = form.cleaned_data['email']
                logger.info(f"Created new user with email {user.email}")
                user.save()
            mailing_list = form.cleaned_data['mailinglist']
            # If we don't find this, we should 500.
            try:
                mailing_list_obj = MailingList.objects.get(
                    mailing_list_token=mailing_list)
            except ObjectDoesNotExist:
                logger.info(
                    f"Failed to find mailing_list_token={mailing_list}")
                return HttpResponseServerError()
            subscribe_user_to_list(user, mailing_list_obj)
            return render(self.request, self.template_name, {})

        return HttpResponseServerError()

    def form_invalid(self, form):
        """Display the correct form.
        This is actually a bit of a hack.  We should build the correct
        form, extract the email address from the incoming form, and
        then display the correct thing.  I think.
        """
        if isinstance(form, QuickMailingListSignupForm):
            form["email"].initial = self.request.POST["email"]
            form["mailinglist"].initial = self.request.POST["mailinglist"]
            return render(self.request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = FirstStepQuickMailingListSignupForm()
        self.kwargs['mailinglist'] = request.GET.get('mailinglist')
        if self.kwargs['mailinglist']:
            form["mailinglist"].initial = self.kwargs['mailinglist']
        else:
            return redirect(f"{reverse_lazy('index')}#newsletter")
        return render(self.request, self.template_name, {"form": form})

    def get_form_class(self, *args, **kwargs):
        post_data = dict(self.request.POST)
        is_captcha_form = post_data.get("captcha_0", None)
        if is_captcha_form:
            return QuickMailingListSignupForm
        else:
            return FirstStepQuickMailingListSignupForm


class QuickPetitionSignup(FormView):
    template_name = 'mailing_list/quick_signup_m.html'
    # This needs to be parameterised by petition.
    merci_template = 'mailing_list/merci_petition.html'
    form_class = QuickPetitionSignupForm
    success_url = reverse_lazy('mailing_list:list_ok')
    # We don't currently populate this form with the user's current
    # subscriptions.  If the user is logged in, we should.  This then
    # becomes the edit form as well.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = ('asso_tn/images-libres/'
                                 'black-and-white-bridge-children-194009-1000'
                                 '.jpg')
        context['hero_title'] = 'Newsletter'
        return context

    def form_valid(self, form):
        """Process a valid QuickPetitionSignup.

        This method is called when valid form data has been POSTed.
        It returns an HttpResponse.
        """
        user = User.objects.filter(email=form.cleaned_data['email']).first()
        if user is None:
            user = User()   # New user.
            user.username = get_random_string(20)
            user.first_name = form.cleaned_data['first_name'] or 'firstname'
            user.last_name = form.cleaned_data['last_name'] or 'lastname'
            user.email = form.cleaned_data['email']
            user.save()
        # user.profile.commune = form.cleaned_data['commune']
        # user.profile.code_postal = form.cleaned_data['code_postal']
        # user.profile.save()

        petition = MailingList.objects.filter(
            mailing_list_token=form.cleaned_data['petition_name'])
        if len(petition) == 0:
            return HttpResponseNotFound("Pétition inconnu")
        subscribe_user_to_list(user, petition[0])
        return render(self.request, self.merci_template, {})


class PetitionView(AssoView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Need to look up petition here.
        # Fetch Markdown for entire petition.
        # Add to context.
        petition = get_object_or_404(Petition, slug=kwargs['petition_slug'])
        petition.set_context(context)
        context['body_text_1'] = petition.petition1_md
        context['body_text_2'] = petition.petition2_md
        context['body_text_3'] = petition.petition3_md
        context['body_text_4'] = petition.petition4_md
        context['petition'] = petition
        context['petition_token'] = petition.mailing_list.mailing_list_token
        # context['hero_image'] = 'asso_tn/traffic-1600.jpg'
        context['page'] = {'hero_image': 'asso_tn/traffic-1600.jpg',
                           'hero_title': "C'est l'heure de changer"}
        return context


class MailingListListView(LoginRequiredMixin,
                          PermissionRequiredMixin, ListView):
    permission_required = 'mailing_list.view_mailinglist'
    model = MailingList
    template_name = "mailing_list/mailing_list_list_view.html"
    queryset = MailingList.objects.all()
    oder_by = ['is_petition', 'mailing_list_name']
    context_object_name = 'mailing_lists_base'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lists = self.get_queryset()
        context['mailing_lists'] = [(list, user_subscribe_count(list))
                                    for list in lists if not list.is_petition]
        context['petitions_lists'] = [(list, subscriber_count(list))
                                      for list in lists if list.is_petition]
        return context
