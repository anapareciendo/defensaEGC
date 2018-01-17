from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.inicio', name='inicio'),
    url(r'^nuevavotacion/','principal.views.nueva_votacion'),
    url(r'^votacionesfuturas/','principal.views.votaciones_futuras'),
    url(r'^nuevapregunta/(?P<poll_id>\d+)/','principal.views.nueva_pregunta'),
    url(r'^nuevaopcion/(?P<question_id>\d+)/','principal.views.nueva_opcion'),
    url(r'^(?P<poll_id>\d+)/','principal.views.detalles_votacion'),
    url(r'^votacionestodas/','principal.views.listar_todas_votaciones'),
    # url(r'^admvotes/', include('admvotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
