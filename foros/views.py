# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory

from .models import *
from agendas.models import *
from notas.models import *
from contrapartes.models import *
from notas.forms import *
from .forms import *

from tagging.models import Tag
from tagging.models import TaggedItem

import thread
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
@login_required
def perfil(request, template='admin/perfil.html'):
    usuario = request.user.id
    user_profile = get_object_or_404(UserProfile, user = usuario)
    contraparte = get_object_or_404(Contraparte, id = user_profile.contraparte.id)

    #foros = Foros.objects.filter(contraparte_id=request.user.id)
    agendas = Agendas.objects.filter(user_id=request.user.id).count()
    notas = Notas.objects.filter(user_id=request.user.id).count()
    aportes = Aportes.objects.filter(user_id=request.user.id).count()

    lista_documentos_aporte = []
    lista_imagen_aporte = []
    lista_videos_aporte = []
    lista_audios_aporte = []

    for aporte in Aportes.objects.filter(user_id=request.user.id):
        for documento in aporte.adjuntos.all():
            lista_documentos_aporte.append(documento)
        for imagen in aporte.fotos.all():
            lista_imagen_aporte.append(imagen)
        for video in aporte.video.all():
            lista_videos_aporte.append(video)
        for audio in aporte.audio.all():
            lista_audios_aporte.append(audio)

    multimedia = len(lista_documentos_aporte) + len(lista_imagen_aporte) + \
                             len(lista_videos_aporte) + len(lista_audios_aporte)

    return render(request, template, locals())

@login_required
def notas_personales(request, template='admin/notas.html'):
    object_list = Notas.objects.filter(user_id=request.user.id)

    return render(request, template, locals())

@login_required
def notas_personales_editar(request, id, template='admin/notas_form.html'):
    object = get_object_or_404(Notas, id=id)
    ForoImgFormSet = generic_inlineformset_factory(Imagen, extra=5, max_num=5)
    ForoDocuFormSet = generic_inlineformset_factory(Documentos, extra=5, max_num=5)

    if request.method == 'POST':
        form = NotasForms(request.POST, request.FILES, instance=object)
        form2 = ForoImgFormSet(data=request.POST, files=request.FILES, instance=object)
        form3 = ForoDocuFormSet(data=request.POST, files=request.FILES, instance=object)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            form_uncommited = form.save()
            form_uncommited.user = request.user
            form_uncommited.save()

            form2.save()
            form3.save()

            return redirect('notas-personales')
    else:
        form = NotasForms(instance=object)
        form2 = ForoImgFormSet(instance=object)
        form3 = ForoDocuFormSet(instance=object)

    return render(request, template, locals())

@login_required
def eliminar_notas_contraparte(request, id):
    nota = Notas.objects.filter(id = id).delete()
    return redirect('notas-personales')

@login_required
def agenda_personales(request, template='admin/agendas.html'):
    object_list = Agendas.objects.filter(user_id=request.user.id)

    return render(request, template, locals())

@login_required
def documento(request, template='admin/documentos.html'):
    documentos = Documentos.objects.all()
    tags = []
    for docu in Documentos.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_doc):
            tags.append(tag)

    query = request.GET.get('q', '')
    if query:
        result_documento = Documentos.objects.filter(nombre_doc__icontains=query)
        result_tags = Tag.objects.filter(name__icontains=query)
        lista = []
        tags_lista = []
        for n in result_documento:
            lista.append(n)
        for rtag in result_tags:
            TaggedItems = TaggedItem.objects.get_by_model(Documentos, rtag.name)
            if not rtag.items.all().count() == 0:
                li = []
                for it in rtag.items.all():
                    if it.object:
                        li.append(it)
                tags_lista.append({'name':rtag.name, 'count': len(li)})
            for item in TaggedItems:
                lista.append(item)
        #tags.sort(key=operator.itemgetter('count'), reverse=True)
        documentos = list(set(lista))

    return render(request, template, locals())

@login_required
def busqueda_tag(request, tags):
    tag_sel = get_object_or_404(Tag, name=tags)
    tags = []
    for docu in Documentos.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_doc):
            tags.append(tag)
    todos = TaggedItem.objects.get_by_model(Documentos, tag_sel.name)
    return render(request, 'admin/documentos_tag.html', locals())


@login_required
def multimedia_fotos(request, template='admin/fotos.html'):
    imagenes = Imagen.objects.all()
    tags = []
    for docu in Imagen.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_img):
            tags.append(tag)

    query = request.GET.get('q', '')
    if query:
        result_fotos = Imagen.objects.filter(nombre_img__icontains=query)
        result_tags = Tag.objects.filter(name__icontains=query)
        lista = []
        tags_lista = []
        for n in result_fotos:
            lista.append(n)
        for rtag in result_tags:
            TaggedItems = TaggedItem.objects.get_by_model(Imagen, rtag.name)
            if not rtag.items.all().count() == 0:
                li = []
                for it in rtag.items.all():
                    if it.object:
                        li.append(it)
                tags_lista.append({'name':rtag.name, 'count': len(li)})
            for item in TaggedItems:
                lista.append(item)
        #tags.sort(key=operator.itemgetter('count'), reverse=True)
        imagenes = list(set(lista))

    return render(request, template, locals())

@login_required
def multimedia_fotos_tag(request, tags):
    tag_sel = get_object_or_404(Tag, name=tags)
    tags = []
    for docu in Imagen.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_img):
            tags.append(tag)
    imagenes = TaggedItem.objects.get_by_model(Imagen, tag_sel.name)
    return render(request, 'admin/fotos.html', locals())


@login_required
def multimedia_videos(request, template='admin/videos.html'):
    videos = Videos.objects.all()
    tags = []
    for docu in Videos.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_vid):
            tags.append(tag)

    query = request.GET.get('q', '')
    if query:
        result_fotos = Videos.objects.filter(nombre_video__icontains=query)
        result_tags = Tag.objects.filter(name__icontains=query)
        lista = []
        tags_lista = []
        for n in result_fotos:
            lista.append(n)
        for rtag in result_tags:
            TaggedItems = TaggedItem.objects.get_by_model(Videos, rtag.name)
            if not rtag.items.all().count() == 0:
                li = []
                for it in rtag.items.all():
                    if it.object:
                        li.append(it)
                tags_lista.append({'name':rtag.name, 'count': len(li)})
            for item in TaggedItems:
                lista.append(item)
        #tags.sort(key=operator.itemgetter('count'), reverse=True)
        videos = list(set(lista))

    return render(request, template, locals())

@login_required
def multimedia_videos_tag(request, tags):
    tag_sel = get_object_or_404(Tag, name=tags)
    tags = []
    for docu in Videos.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_vid):
            tags.append(tag)
    videos = TaggedItem.objects.get_by_model(Videos, tag_sel.name)
    return render('admin/videos.html',  locals())


@login_required
def multimedia_audios(request, template='admin/audios.html'):
    audios = Audios.objects.all()
    tags = []
    for docu in Audios.objects.all():
        for tag in Tag.objects.filter(name=docu.tags_aud):
            tags.append(tag)

    query = request.GET.get('q', '')
    if query:
        result_fotos = Videos.objects.filter(nombre_aud__icontains=query)
        result_tags = Tag.objects.filter(name__icontains=query)
        lista = []
        tags_lista = []
        for n in result_fotos:
            lista.append(n)
        for rtag in result_tags:
            TaggedItems = TaggedItem.objects.get_by_model(Videos, rtag.name)
            if not rtag.items.all().count() == 0:
                li = []
                for it in rtag.items.all():
                    if it.object:
                        li.append(it)
                tags_lista.append({'name':rtag.name, 'count': len(li)})
            for item in TaggedItems:
                lista.append(item)
        #tags.sort(key=operator.itemgetter('count'), reverse=True)
        audios = list(set(lista))

    return render(request, template, locals())

### Foros  ###
@login_required
def crear_foro(request):
    if request.method == 'POST':
        form = ForosForm(request.POST)
        form2 = ImagenForm(request.POST, request.FILES)
        form3 = DocumentoForm(request.POST, request.FILES)
        form4 = VideoForm(request.POST)
        form5 = AudioForm(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.contraparte = request.user
            form_uncommited.save()
            if form2.cleaned_data['nombre_img'] != '':
                form2_uncommitd = form2.save(commit=False)
                form2_uncommitd.content_object = form_uncommited
                form2_uncommitd.save()
            if form3.cleaned_data['nombre_doc'] != '':
                form3_uncommitd = form3.save(commit=False)
                form3_uncommitd.content_object = form_uncommited
                form3_uncommitd.save()
            if form4.cleaned_data['nombre_video'] != '':
                form4_uncommitd = form4.save(commit=False)
                form4_uncommitd.content_object = form_uncommited
                form4_uncommitd.save()
            if form5.cleaned_data['nombre_audio'] != '':
                form5_uncommitd = form5.save(commit=False)
                form5_uncommitd.content_object = form_uncommited
                form5_uncommitd.save()

            thread.start_new_thread(notify_all_foro, (form_uncommited,))

            return HttpResponseRedirect('/foros')

    else:
        form = ForosForm()
        form2 = ImagenForm()
        form3 = DocumentoForm()
        form4 = VideoForm()
        form5 = AudioForm()
    return render(request, 'foros/crear_foro.html', locals())

def notify_all_foro(foros):
    site = Site.objects.get_current()
    users = User.objects.all() #.exclude(username=foros.contraparte.username)
    contenido = render_to_string('foros/notify_new_foro.txt', {'foro': foros,
                                 'url': '%s/foros/ver/%s' % (site, foros.id),
                                 'url_aporte': '%s/foros/ver/%s/#formaporte' % (site, foros.id),
                                 })
    send_mail('Nuevo Foro en CAFOD', contenido, 'cafod@cafodca.org', [user.email for user in users if user.email])


@login_required
def ver_foro(request, foro_id):
    discusion = get_object_or_404(Foros, id=foro_id)

    if request.method == 'POST':
        form = AporteForm(request.POST)
        form2 = ImagenForm(request.POST, request.FILES)
        form3 = DocumentoForm(request.POST, request.FILES)
        form4 = VideoForm(request.POST)
        form5 = AudioForm(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.foro = discusion
            form_uncommited.save()
            if form2.cleaned_data['nombre_img'] != '':
                form2_uncommitd = form2.save(commit=False)
                form2_uncommitd.content_object = form_uncommited
                form2_uncommitd.save()
            if form3.cleaned_data['nombre_doc'] != '':
                form3_uncommitd = form3.save(commit=False)
                form3_uncommitd.content_object = form_uncommited
                form3_uncommitd.save()
            if form4.cleaned_data['nombre_video'] != '':
                form4_uncommitd = form4.save(commit=False)
                form4_uncommitd.content_object = form_uncommited
                form4_uncommitd.save()
            if form5.cleaned_data['nombre_audio'] != '':
                form5_uncommitd = form5.save(commit=False)
                form5_uncommitd.content_object = form_uncommited
                form5_uncommitd.save()

            thread.start_new_thread(notify_all_aporte, (form_uncommited,))

            return HttpResponseRedirect('/foros/ver/%d' % discusion.id)
    else:
        form = AporteForm()
        form2 = ImagenForm()
        form3 = DocumentoForm()
        form4 = VideoForm()
        form5 = AudioForm()
    return render(request, 'foros/ver_foro.html',  locals())

def notify_all_aporte(aportes):
    site = Site.objects.get_current()
    users = User.objects.all() #.exclude(username=foros.contraparte.username)
    contenido = render_to_string('foros/notify_new_aporte.txt', {'aporte': aportes,
                                 #'url': '%s/foros/ver/%s' % (site, foros.id),
                                 'url_aporte': '%s/foros/ver/%s/#%s' % (site, aportes.foro.id, aportes.id),
                                 })
    send_mail('Nuevo Aporte en CAFOD', contenido, 'cafod@cafodca.org', [user.email for user in users if user.email])


@login_required
def comentario_foro(request, aporte_id):
    aporte = get_object_or_404(Aportes, id=aporte_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form1_uncommited = form.save(commit=False)
            form1_uncommited.usuario = request.user
            form1_uncommited.aporte = aporte
            form1_uncommited.save()

            thread.start_new_thread(notify_user_comentario, (form1_uncommited,))

            return HttpResponse('/foros/ver/%d/#cmt%s' % (aporte.foro_id, form.instance.id))
    else:
        form = ComentarioForm()
    return render(request, 'foros/comentario.html', locals())

def notify_user_comentario(comentario):
    site = Site.objects.get_current()
    contenido = render_to_string('foros/notify_new_comment.txt', {
                                   'comentario': comentario,
                                   'url': '%s/foros/ver/%s' % (site, comentario.aporte.foro.id)
                                    })
    send_mail('Nuevo comentario CAFOD', contenido, 'cafod@cafodca.org', [comentario.aporte.user.email])


@login_required
def editar_foro(request, id):
    foro = get_object_or_404(Foros, id=id)
    ForoImgFormSet = generic_inlineformset_factory(Imagen, extra=5, max_num=5)
    ForoDocuFormSet = generic_inlineformset_factory(Documentos, extra=5, max_num=5)
    ForoVideoFormSet = generic_inlineformset_factory(Videos, extra=5, max_num=5)
    ForoAudioFormSet = generic_inlineformset_factory(Audios, extra=5, max_num=5)
    form2 = ForoImgFormSet(instance=foro)
    form3 = ForoDocuFormSet(instance=foro)
    form4 = ForoVideoFormSet(instance=foro)
    form5 = ForoAudioFormSet(instance=foro)

    if not foro.contraparte == request.user and not request.user.is_superuser:
        return HttpResponse("Usted no puede editar este Foro")

    if request.method == 'POST':
        form = ForosForm(request.POST, instance=foro)
        form2 = ForoImgFormSet(data=request.POST, files=request.FILES, instance=foro)
        form3 = ForoDocuFormSet(data=request.POST, files=request.FILES, instance=foro)
        form4 = ForoVideoFormSet(data=request.POST, files=request.FILES, instance=foro)
        form5 = ForoAudioFormSet(data=request.POST, files=request.FILES, instance=foro)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.contraparte = request.user
            form_uncommited.save()

            form2.save()
            form3.save()
            form4.save()
            form5.save()
            return HttpResponseRedirect('/foros/ver/'+id+'/?b=editado')

    else:
        form = ForosForm(instance=foro)
        form2 = ForoImgFormSet(instance=foro)
        form3 = ForoDocuFormSet(instance=foro)
        form4 = ForoVideoFormSet(instance=foro)
        form5 = ForoAudioFormSet(instance=foro)

    return render(request, 'foros/crear_foro.html',  locals())


@login_required
def borrar_foro(request, id):
    foro = get_object_or_404(Foros, id=id)
    if foro.contraparte == request.user or request.user.is_superuser:
        foro.delete()
        return redirect('/foros/?b=borrado')
    else:
        return redirect('/')

@login_required
def editar_aporte(request, aporte_id):
    aporte = get_object_or_404(Aportes, id=aporte_id)

    AporteImgFormSet = generic_inlineformset_factory(Imagen, extra=5, max_num=5)
    AporteDocuFormSet = generic_inlineformset_factory(Documentos, extra=5, max_num=5)
    AporteVideoFormSet = generic_inlineformset_factory(Videos, extra=5, max_num=5)
    AporteAudioFormSet = generic_inlineformset_factory(Audios, extra=5, max_num=5)
    form2 = AporteImgFormSet(instance=aporte)
    form3 = AporteDocuFormSet(instance=aporte)
    form4 = AporteVideoFormSet(instance=aporte)
    form5 = AporteAudioFormSet(instance=aporte)

    if not aporte.user == request.user and not request.user.is_superuser:
        return HttpResponse("Usted no puede editar este Foro")

    if request.method == 'POST':
        form = AporteForm(request.POST, instance=aporte)
        form2 = AporteImgFormSet(data=request.POST, files=request.FILES, instance=aporte)
        form3 = AporteDocuFormSet(data=request.POST, files=request.FILES, instance=aporte)
        form4 = AporteVideoFormSet(data=request.POST, files=request.FILES, instance=aporte)
        form5 = AporteAudioFormSet(data=request.POST, files=request.FILES, instance=aporte)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.contraparte = request.user
            form_uncommited.save()

            form2.save()
            form3.save()
            form4.save()
            form5.save()
            return HttpResponseRedirect('/foros')

    else:
        form = AporteForm(instance=aporte)
        form2 = AporteImgFormSet(instance=aporte)
        form3 = AporteDocuFormSet(instance=aporte)
        form4 = AporteVideoFormSet(instance=aporte)
        form5 = AporteAudioFormSet(instance=aporte)

    return render(request, 'foros/editar_aporte.html', locals())

@login_required
def editar_comentario(request, comen_id):
    comentario = get_object_or_404(Comentarios, id=comen_id)

    if not comentario.usuario == request.user and not request.user.is_superuser:
        return HttpResponse("Usted no puede editar este Comentario")

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.usuario = request.user
            form_uncommited.save()
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'foros/comentario.html',  locals())

@login_required
def borrar_aporte(request, id):
    aporte = get_object_or_404(Aportes, id=id)
    if aporte.user == request.user or request.user.is_superuser:
        aporte.delete()
        print 'si me borra'
        return redirect('/foros/lista')
    else:
        print 'mierda no me barra'
        return redirect('/foros/lista')

@login_required
def borrar_comentario(request, id):
    comentario = get_object_or_404(Comentarios, id=id)
    if comentario.usuario == request.user or request.user.is_superuser:
        comentario.delete()
        print 'siiii borre comentario'
        return redirect('/foros/lista')
    else:
        print 'Mierda no se pudo borrar el puto comentario'
        return redirect('/')
