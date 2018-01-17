from principal.models import *
from principal.forms import *
from django.shortcuts import render_to_response, get_list_or_404
#Para autenticacion
from django.contrib.auth import authenticate
#Para usar Formularios
#from principal.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from datetime import datetime

import json
import urllib2 


URL_COOKIE="https://g1login.egc.duckdns.org/cookies/"

def inicio(request):
    session_id=request.COOKIES.get('session_id')
    if session_id is not None:
        response = urllib2.urlopen(URL_COOKIE+session_id).read()
        data = json.loads(response)
        if data['codigo'] == 1:
            return listar_votaciones(data," ")
        else:
            return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    else:
        return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')

def nueva_votacion(request):
    session_id=request.COOKIES.get('session_id')
    if session_id is not None:
        response = urllib2.urlopen(URL_COOKIE+session_id).read()
        data = json.loads(response)
        if data['codigo'] == 1:
            if data['usuario']['role_id'] == 1:
                if request.method=='POST':
                    formulario = PollForm(request.POST, request.FILES)
                    if formulario.is_valid():
                        formulario.save()
                        return HttpResponseRedirect('/')
                else:
                    formulario = PollForm()
                    return render_to_response('nuevavotacion.html',{'formulario':formulario}, context_instance=RequestContext(request))
            else:
                return listar_votaciones(data, "Solo administradores pueden editar votaciones")
        else:
            return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    else:
        return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    
def votaciones_futuras(request):
    session_id=request.COOKIES.get('session_id')
    if session_id is not None:
        response = urllib2.urlopen(URL_COOKIE+session_id).read()
        data = json.loads(response)
        if data['codigo'] == 1:
            if data['usuario']['role_id'] == 1:
                now = datetime.today().date()    
                votaciones = Poll.objects.filter(startDate__range=[now, "2050-01-31"])
                return render_to_response("lista.html",{"votaciones":votaciones, "preguntas":True})
            else:
                return listar_votaciones(data, "Solo administradores pueden editar votaciones")
        else:
            return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    else:
        return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    
def nueva_pregunta(request, poll_id):
    session_id=request.COOKIES.get('session_id')
    if session_id is not None:
        response = urllib2.urlopen(URL_COOKIE+session_id).read()
        data = json.loads(response)
        if data['codigo'] == 1: 
            if data['usuario']['role_id'] == 1:
                if request.method=='POST':
                    formulario = QuestionForm(request.POST, request.FILES)
                    if formulario.is_valid():
                        poll = Poll.objects.get(id=poll_id)
                        Question.objects.create(title=formulario.cleaned_data['title'], description=formulario.cleaned_data['description'], optional=formulario.cleaned_data['optional'], multiple=formulario.cleaned_data['multiple'], poll=poll)
                        return HttpResponseRedirect('/')
                else:
                    formulario = QuestionForm()
                    return render_to_response('nuevapregunta.html',{'formulario':formulario}, context_instance=RequestContext(request))
            else:
                return listar_votaciones(data, "Solo administradores pueden editar votaciones")
        else:
            return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    else:
        return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')

def detalles_votacion(request, poll_id):
    session_id=request.COOKIES.get('session_id')
    if session_id is not None:
        response = urllib2.urlopen(URL_COOKIE+session_id).read()
        data = json.loads(response)
        if data['codigo'] == 1:
            votacion = Poll.objects.get(id=poll_id)
            preguntas = Question.objects.filter(poll=votacion)
            opciones = []
            admin = False
            session_id=request.COOKIES.get('session_id')
            if  data['usuario']['role_id'] == 1:
                admin = True
            for pregunta in preguntas:
                for opcion in Option.objects.filter(question=pregunta):
                    opciones.append(opcion)
            return render_to_response("detallesvotacion.html",{"votacion":votacion, "preguntas":preguntas, "opciones":opciones, 'admin':admin})
        else:
            return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    else:
        return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')

def nueva_opcion(request, question_id):
    session_id=request.COOKIES.get('session_id')
    if session_id is not None:
        response = urllib2.urlopen(URL_COOKIE+session_id).read()
        data = json.loads(response)
        if data['codigo'] == 1:
            if data['usuario']['role_id'] == 1:
                if request.method == 'POST':
                    formulario = OptionForm(request.POST, request.FILES)
                    if formulario.is_valid():
                        question = Question.objects.get(id=question_id)
                        Option.objects.create(description=formulario.cleaned_data['description'], question=question)
                        return HttpResponseRedirect('/')
                else:
                    formulario = OptionForm()
                    return render_to_response('nuevaopcion.html',{'formulario':formulario}, context_instance=RequestContext(request))
            else:
                return listar_votaciones(data, "Solo administradores pueden editar votaciones")
        else:
            return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    else:
        return HttpResponseRedirect('https://g1login.egc.duckdns.org/login')
    
def listar_votaciones(data, message):
    uaid = data['usuario']['id']
    useraccount = UserAccount.objects.get(id = uaid)
    userpercensus = UserPerCensus.objects.filter(useraccount = useraccount)
    censos = []
    votaciones = []
    ca = User.objects.get(useraccount=useraccount).ca
    for relation in userpercensus:
        censos.append(relation.census)
    for votacion in Poll.objects.all():
        if votacion.census.ca == ca:
            votaciones.append(votacion)
        else:
            for censo in censos:
                if censo == votacion.census:
                    votaciones.append(votacion)
    return render_to_response("lista.html",{"votaciones":votaciones, "inicio":True, 'mensaje':message})