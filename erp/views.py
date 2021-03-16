from django.shortcuts import render
from erp.models import RegisteredPrograms, Menus, Files, RegisteredProgramsCheckIns, RegistereddevNotice, devNoticeCheckIns
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.db import transaction
from django.db.models import Q


@login_required
def index(request):
    return render(request, 'erp/index.html', {
        'programs': RegisteredPrograms.objects.all(),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'search_text': request.GET.get('search_text', None)
    })


def sign_in(request):
    return render(request, 'erp/sign_in.html', {
        'programs': RegisteredPrograms.objects.all(),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'search_text': request.GET.get('search_text', None)
    })


@login_required
@csrf_exempt
def devManage(request):
    if request.method == 'GET':
        return render(request, 'erp/dev/devManage/devManage.html', {
            'programs': RegisteredPrograms.objects.all(),
            'menu': request.GET.get('menu', None),
            'menus': Menus.objects.all(),
            'search_text': request.GET.get('search_text', None)
        })
    elif request.method == 'POST':
        menu = request.GET.get('menu', None)
        target = RegisteredPrograms.objects.create(
            title=request.POST['inputName'],
            category=request.POST['inputCat'],
            progress=request.POST['selectProgress'],
            rating=request.POST['selectRating'],
            url=request.POST['inputURL'],
            content=request.POST['editordata'],
            manual=request.POST['summernote_modal_input'],
            writer=request.POST['writer'],
            parent_id=request.POST['parent_id']
        )
        for f in request.FILES.getlist('inputfile', None):
            Files.objects.create(
                board='devManage',
                p_id=target.id,
                file=f
            )
        return HttpResponseRedirect(f"/devManage?menu={menu}")


@login_required
@csrf_exempt
def devMenu(request):
    if request.method == 'GET':
        return render(request, 'erp/dev/devMenu/devMenu.html', {
            'programs': RegisteredPrograms.objects.all(),
            'menu': request.GET.get('menu', None),
            'menus': Menus.objects.all().order_by('id'),
            'search_text': request.GET.get('search_text', None)
        })
    elif request.method == 'POST':
        menu_dict = json.loads(request.POST.get('menus'))
        Menus.objects.all().delete()

        for t in menu_dict:
            Menus.objects.create(
                m_id=t['m_id'],
                parent=t['parent'],
                menu_name=t['menu_name'],
                parent_url=t['parent_url'],
            )

        return HttpResponse(status=204)


# @login_required
@transaction.atomic
@csrf_exempt
def devManageDetail(request, id):
    if request.method == 'GET':
        check_ins = RegisteredProgramsCheckIns.objects.filter(p_id=id).order_by('-created_at')
        q_list = []
        for c in check_ins.values('id'):
            q_list.append(c['id'])

        check_in_files = Files.objects.filter(Q(p_id__in=q_list) & Q(board='devManage_check_in'))

        return render(request, 'erp/dev/devManage/devManage_Detail.html', {
            'programs': RegisteredPrograms.objects.all(),
            'program': RegisteredPrograms.objects.get(id=id),
            'menu': request.GET.get('menu', None),
            'menus': Menus.objects.all(),
            'files': Files.objects.filter(Q(board='devManage') & Q(p_id=id)),
            'check_ins': check_ins,
            'search_text': request.GET.get('search_text', None),
            'check_in_files': check_in_files
        })
    elif request.method == 'POST':
        program = RegisteredPrograms.objects.get(id=id)

        program.title = request.POST['inputName']
        program.category = request.POST['inputCat']
        program.progress = request.POST['selectProgress']
        program.rating = request.POST['selectRating']
        program.url = request.POST['inputURL']
        program.content = request.POST['editordata']
        program.manual = request.POST['summernote_modal_input']
        program.writer = request.POST['writer']
        program.parent_id = request.POST['parent_id']
        program.save()
        
        if request.POST['file_delete_list']:
            d_list = request.POST['file_delete_list'].split(',')
            
            for x in d_list:
                Files.objects.filter(id=x).delete()
                

        return HttpResponseRedirect(f"/devManage?menu=dev")


@login_required
def devManageMod(request, id):
    return render(request, 'erp/dev/devManage/devManage_Mod.html', {
        'programs': RegisteredPrograms.objects.all(),
        'program': RegisteredPrograms.objects.get(id=id),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'search_text': request.GET.get('search_text', None)
    })


@login_required
def devManage_Write(request):
    return render(request, 'erp/dev/devManage/devManage_Write.html', {
        'programs': RegisteredPrograms.objects.all(),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'search_text': request.GET.get('search_text', None)
    })


@login_required
def devManage_Update(request, id):
    return render(request, 'erp/dev/devManage/devManage_Write.html', {
        'programs': RegisteredPrograms.objects.all(),
        'program': RegisteredPrograms.objects.get(id=id),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'files': Files.objects.filter(Q(board='devManage') & Q(p_id=id)),
        'search_text': request.GET.get('search_text', None)
    })


@transaction.atomic
@login_required
@csrf_exempt
def devManage_Check_In_Save(request, id):
    menu = request.GET.get('menu', None)

    target = RegisteredProgramsCheckIns.objects.create(
        p_id=id,
        title=request.POST['inputTitle'],
        writer=request.POST['writer'],
        content=request.POST['summernote_check_in'],
        progress=request.POST['selectProgress'],
        tag=request.POST.getlist('tag')
    )
    for f in request.FILES.getlist('inputFiles', None):
        Files.objects.create(
            board='devManage_check_in',
            p_id=target.id,
            file=f
        )

    program = RegisteredPrograms.objects.get(id=id)
    program.progress = request.POST['selectProgress']
    program.save()

    return HttpResponseRedirect(f"/devManage/post/{id}/?menu={menu}")


@login_required
def devManage_Delete(request):
    id = request.GET.get('pid', None).split(',')
    id = id[0:len(id)-1]

    for x in id:
        RegisteredPrograms.objects.filter(id=x).delete()

    return HttpResponseRedirect("/devManage?menu=dev")


@login_required
def example(request):
    return render(request, 'erp/example.html', {
        'programs': RegisteredPrograms.objects.all(),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'search_text': request.GET.get('search_text', None),
        'program': RegisteredPrograms.objects.get(url='f-erp-ex-001')
    })


@login_required
def devNotice(request):
    if request.method == 'GET':
        return render(request, 'erp/dev/devNotice/devNotice.html', {
            'notices': RegistereddevNotice.objects.all(),
            'menu': request.GET.get('menu', None),
            'menus': Menus.objects.all(),
            'search_text': request.GET.get('search_text', None),
            'program': RegisteredPrograms.objects.get(url='f-erp-ex-001')
        })
    elif request.method == 'POST':
        menu = request.GET.get('menu', None)
        target = RegistereddevNotice.objects.create(
            title=request.POST['inputName'],
            content=request.POST['editordata'],
            writer=request.POST['writer']
        )
        for f in request.FILES.getlist('inputfile', None):
            Files.objects.create(
                board='devNotice',
                p_id=target.id,
                file=f
            )
        return HttpResponseRedirect(f"/devNotice?menu=dev")


@login_required
def devNoticeDetail(request, id):
    if request.method == 'GET':
        check_ins = devNoticeCheckIns.objects.filter(p_id=id).order_by('-created_at')

        q_list = []
        for c in check_ins.values('id'):
            q_list.append(c['id'])

        return render(request, 'erp/dev/devNotice/devNotice_Detail.html', {
            'programs': RegisteredPrograms.objects.all(),
            'notice': RegistereddevNotice.objects.get(id=id),
            'menu': request.GET.get('menu', None),
            'menus': Menus.objects.all(),
            'files': Files.objects.filter(Q(board='devNotice') & Q(p_id=id)),
            'check_ins': check_ins,
            'search_text': request.GET.get('search_text', None),
            'check_in_files': Files.objects.filter(Q(p_id__in=q_list) & Q(board='devManage_check_in'))
        })
    elif request.method == 'POST':
        notice = RegistereddevNotice.objects.get(id=id)

        notice.title = request.POST['inputName']
        notice.content = request.POST['editordata']
        notice.writer = request.POST['writer']
        notice.save()
        
        if request.POST['file_delete_list']:
            d_list = request.POST['file_delete_list'].split(',')
            
            for x in d_list:
                Files.objects.filter(id=x).delete()

        return HttpResponseRedirect(f"/devNotice?menu=dev")


@login_required
def devNoticeWrite(request):
    return render(request, 'erp/dev/devNotice/devNotice_Write.html', {
        'programs': RegisteredPrograms.objects.all(),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'search_text': request.GET.get('search_text', None)
    })

@login_required
def devNotice_Delete(request):
    id = request.GET.get('pid', None).split(',')
    id = id[0:len(id)-1]

    for x in id:
        RegistereddevNotice.objects.filter(id=x).delete()
    return HttpResponseRedirect("/devNotice?menu=dev")


@login_required
def devNotice_Update(request, id):
    return render(request, 'erp/dev/devNotice/devNotice_Write.html', {
        'programs': RegisteredPrograms.objects.all(),
        'notice': RegistereddevNotice.objects.get(id=id),
        'menu': request.GET.get('menu', None),
        'menus': Menus.objects.all(),
        'files': Files.objects.filter(Q(board='devNotice') & Q(p_id=id)),
        'search_text': request.GET.get('search_text', None)
    })
