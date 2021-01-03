from django.urls import path
# from django.views.generic.base import RedirectView
from .views import AssoView

app_name = 'asso_m'
urlpatterns = [

    path('nous-contacter', AssoView.as_view(
        title="Nous contacter",
        meta_descr="""<meta name="description" content="Les Mobilitains oeuvrent pour une mobilité plus sécurisée, plus fluide et plus vertueuse."/>""",
        twitter_title = "Qui sommes-nous ? | Mobilitains",
        twitter_descr = "Les Mobilitains oeuvrent pour une mobilité plus sécurisée, plus fluide et plus vertueuse.",
        template_name='asso_tn/contact.html',
        hero_image="asso_tn/happy-folks-1000.jpg"),
         name='contact'),

    # This has a first commit in #12, then some emails exchanged with Julien.
    # What's here is a place holder.
    path('mentions-legales', AssoView.as_view(title="Mentions Légales",
                                              template_name='asso_tn/mentions_legales.html'),
         name='TC'),

    ## Copyright page needed.

    path('jobs', AssoView.as_view(title="Jobs",
                                  template_name='asso_tn/jobs.html',),
         name='jobs'),
]
