
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from core.models import Note, Book, PYQ, Syllabus, Doubt, Reply, Bookmark, Branch, User
from core.models import Note as note


@login_required
@require_http_methods(['POST'])
def download_note(request, note_id):

    # Increment count on download

    note.download_count = note.download_count + 1

    note.save(update_fields=['download_count'])

    pdf_url = note.pdf_link or (note.pdf_file.url if note.pdf_file else '')
    return JsonResponse({'message': 'Download recorded', 'download_count': note.download_count, 'pdf_url': pdf_url})


def is_super_or_admin(user):

    return user.role in ['super_student', 'admin']


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def upload_syllabus(request):
    if request.user.role != 'super_student':
        return JsonResponse({'error': 'Only super students can upload syllabus'}, status=403)

    subject_name = request.POST.get('subject_name')
    subject_code = request.POST.get('subject_code')
    branch_code = request.POST.get('branch')
    semester = request.POST.get('semester')
    units_raw = request.POST.get('units', '[]')

    pdf_link = request.POST.get('pdf_link', '')
    pdf_file = request.FILES.get('pdf_file')

    if not all([subject_name, subject_code, branch_code, semester]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    if not pdf_file and not pdf_link:
        return JsonResponse({'error': 'Either pdf_link or pdf_file is required'}, status=400)

    # Parse units JSON
    try:
        import json
        units = json.loads(units_raw) if isinstance(units_raw, str) else units_raw
        if not isinstance(units, list):
            return JsonResponse({'error': 'units must be a list'}, status=400)
        # normalize keys to {n, topic}
        normalized = []
        for idx, u in enumerate(units, start=1):
            if isinstance(u, dict):
                n = u.get('n', u.get('unit', idx))
                topic = u.get('topic', u.get('name', ''))
                normalized.append({'n': int(n), 'topic': topic})
            else:
                normalized.append({'n': idx, 'topic': str(u)})
        units = normalized
    except Exception as e:
        return JsonResponse({'error': f'Invalid units JSON: {e}'}, status=400)

    try:
        branch = Branch.objects.get(code=branch_code)
        s = Syllabus(
            subject_name=subject_name,
            subject_code=subject_code,
            branch=branch,
            semester=int(semester),
            units=units,
            pdf_link=pdf_link,
            pdf_file=pdf_file,
        )
        s.full_clean()
        s.save()
        return JsonResponse({'id': s.id, 'message': 'Syllabus uploaded'})
    except Branch.DoesNotExist:
        return JsonResponse({'error': 'Invalid branch'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# --------------------- NOTES ---------------------
@require_http_methods(['GET'])
def notes_list(request):

    branch = request.GET.get('branch')
    semester = request.GET.get('semester')
    search = request.GET.get('search', '').strip()
    limit = request.GET.get('limit')
    try:
        limit = int(limit) if limit is not None else None
    except Exception:
        limit = None

    qs = Note.objects.select_related('branch', 'uploaded_by')
    if branch and branch != 'all':
        qs = qs.filter(branch__code=branch)
    if semester and semester != 'all':
        qs = qs.filter(semester=semester)

    if search:
        qs = qs.filter(
            models.Q(title__icontains=search)
            | models.Q(subject__icontains=search)
            | models.Q(description__icontains=search)
            | models.Q(tags__icontains=search)
        )

    if limit and limit > 0:
        qs = qs.order_by('-uploaded_at')[:limit]
        data = []
        for n in qs:
            data.append({
                'id': n.id,
                'title': n.title,
                'subject': n.subject,
                'branch': n.branch.code,
                'semester': n.semester,
                'unit': n.unit,
                'description': n.description,
                'tags': n.tags.split(',') if n.tags else [],
                'uploaded_by': n.uploaded_by.username,
                'uploaded_at': n.uploaded_at.strftime('%Y-%m-%d'),
                'download_count': n.download_count,
                'pdf_url': n.pdf_link or (n.pdf_file.url if n.pdf_file else ''),
                'cover_link': n.cover_link,
                'is_mine': request.user.is_authenticated and n.uploaded_by == request.user,
            })
        return JsonResponse({'notes': data, 'has_next': False})

    paginator = Paginator(qs, 12)
    page = request.GET.get('page', 1)
    notes_page = paginator.get_page(page)
    data = []
    for n in notes_page:
        data.append({
            'id': n.id,
            'title': n.title,
            'subject': n.subject,
            'branch': n.branch.code,
            'semester': n.semester,
            'unit': n.unit,
            'description': n.description,
            'tags': n.tags.split(',') if n.tags else [],
            'uploaded_by': n.uploaded_by.username,
            'uploaded_at': n.uploaded_at.strftime('%Y-%m-%d'),
            'download_count': n.download_count,
            'pdf_url': n.pdf_link or (n.pdf_file.url if n.pdf_file else ''),
            'cover_link': n.cover_link,
            'is_mine': request.user.is_authenticated and n.uploaded_by == request.user,
        })
    return JsonResponse({'notes': data, 'has_next': notes_page.has_next()})

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def upload_note(request):
    title = request.POST.get('title')
    subject = request.POST.get('subject')
    branch_code = request.POST.get('branch')
    semester = request.POST.get('semester')
    unit = request.POST.get('unit')
    description = request.POST.get('description', '')
    tags = request.POST.get('tags', '')
    cover_link = request.POST.get('cover_link', '')
    pdf_link = request.POST.get('pdf_link', '')
    pdf_file = request.FILES.get('pdf_file')
    if not all([title, subject, branch_code, semester, unit]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    if not pdf_file and not pdf_link:
        return JsonResponse({'error': 'Either PDF file or PDF link required'}, status=400)
    try:
        branch = Branch.objects.get(code=branch_code)
        note = Note(
            title=title, subject=subject, branch=branch, semester=semester, unit=unit,
            description=description, tags=tags, cover_link=cover_link,
            pdf_link=pdf_link, pdf_file=pdf_file, uploaded_by=request.user
        )
        note.full_clean()
        note.save()
        return JsonResponse({'id': note.id, 'message': 'Note uploaded'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(['DELETE'])
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
        if note.uploaded_by != request.user and request.user.role not in ['admin', 'super_student']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        # delete physical file if present
        if note.pdf_file:
            pdf_path = note.pdf_file.path
            note.delete()
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        else:
            note.delete()

        return JsonResponse({'message': 'Deleted'})
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


@login_required
@require_http_methods(['POST'])
def toggle_bookmark(request, note_id):

    try:
        note = Note.objects.get(id=note_id)

        bookmark, created = Bookmark.objects.get_or_create(user=request.user, note=note)

        if not created:
            bookmark.delete()
            return JsonResponse({'bookmarked': False})
        return JsonResponse({'bookmarked': True})
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)

@login_required
def my_uploads(request):
    notes = Note.objects.filter(uploaded_by=request.user).values('id', 'title', 'subject', 'download_count')
    return JsonResponse({'notes': list(notes)})

@login_required
def saved_notes(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('note')
    data = [{'id': b.note.id, 'title': b.note.title, 'subject': b.note.subject} for b in bookmarks]
    return JsonResponse({'notes': data})

# --------------------- BOOKS (Super student only upload) ---------------------
@require_http_methods(['GET'])
def books_list(request):
    branch = request.GET.get('branch')
    search = request.GET.get('search', '').strip()

    qs = Book.objects.select_related('branch')
    if branch and branch != 'all':
        qs = qs.filter(branch__code=branch)

    if search:
        qs = qs.filter(
            models.Q(title__icontains=search)
            | models.Q(author__icontains=search)
            | models.Q(subject__icontains=search)
        )

    data = []
    for b in qs:
        data.append({
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'subject': b.subject,
            'branch': b.branch.code,
            'semester': b.semester,
            'rating': b.rating,
            'cover_gradient': b.cover_gradient,
            'description': b.description,
            'pdf_url': b.pdf_link or (b.pdf_file.url if b.pdf_file else ''),
            'cover_link': b.cover_link,
        })
    return JsonResponse({'books': data})

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def upload_book(request):

    if not is_super_or_admin(request.user):
        return JsonResponse({'error': 'Only super students or admin can upload books'}, status=403)

    title = request.POST.get('title')
    author = request.POST.get('author')
    subject = request.POST.get('subject')
    branch_code = request.POST.get('branch')
    semester = request.POST.get('semester')
    rating = request.POST.get('rating')
    cover_gradient = request.POST.get('cover_gradient')
    description = request.POST.get('description', '')
    cover_link = request.POST.get('cover_link', '')
    pdf_link = request.POST.get('pdf_link', '')
    pdf_file = request.FILES.get('pdf_file')

    if not all([title, author, subject, branch_code, semester, rating]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    if not pdf_file and not pdf_link:
        return JsonResponse({'error': 'Either PDF file or PDF link required'}, status=400)

    try:
        branch = Branch.objects.get(code=branch_code)
        book = Book(
            title=title,
            author=author,
            subject=subject,
            branch=branch,
            semester=int(semester),
            rating=int(rating),
            cover_gradient=cover_gradient or Book._meta.get_field('cover_gradient').get_default(),
            description=description,
            cover_link=cover_link,
            pdf_link=pdf_link,
            pdf_file=pdf_file,
        )
        book.full_clean()
        book.save()
        return JsonResponse({'id': book.id, 'message': 'Book uploaded'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# --------------------- SYLLABUS & PYQ ---------------------
# These are read-only endpoints for the frontend.

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def upload_pyq(request):
    # Only super_student/admin upload PYQ
    if request.user.role not in ['super_student', 'admin']:
        return JsonResponse({'error': 'Only super students can upload PYQ'}, status=403)

    subject = request.POST.get('subject')
    branch_code = request.POST.get('branch')
    semester = request.POST.get('semester')
    year = request.POST.get('year')
    exam_type = request.POST.get('exam_type')
    pdf_link = request.POST.get('pdf_link', '')
    pdf_file = request.FILES.get('pdf_file')

    if not all([subject, branch_code, semester, year, exam_type]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    if not pdf_file and not pdf_link:
        return JsonResponse({'error': 'Either pdf_link or pdf_file is required'}, status=400)

    try:
        branch = Branch.objects.get(code=branch_code)
        pyq = PYQ(
            subject=subject,
            branch=branch,
            semester=int(semester),
            year=int(year),
            exam_type=exam_type,
            pdf_link=pdf_link,
            pdf_file=pdf_file,
        )
        pyq.full_clean()
        pyq.save()
        return JsonResponse({'id': pyq.id, 'message': 'PYQ uploaded'})
    except Branch.DoesNotExist:
        return JsonResponse({'error': 'Invalid branch'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(['GET'])
def syllabus_list(request):
    branch = request.GET.get('branch', None)
    semester = request.GET.get('semester', None)


    qs = Syllabus.objects.all().order_by('subject_code')
    if branch and branch != 'all':
        qs = qs.filter(branch__code=branch)
    if semester and semester != 'all':
        qs = qs.filter(semester=semester)

    data = []
    for s in qs:
        units = s.units if isinstance(s.units, list) else (s.units or [])
        data.append({
            'id': s.id,
            'subject_name': s.subject_name,
            'subject_code': s.subject_code,
            'branch': s.branch.code,
            'semester': s.semester,
            'units': units,
            'pdf_url': s.pdf_url if hasattr(s, 'pdf_url') and s.pdf_url else (s.pdf_link or (s.pdf_file.url if s.pdf_file else '')),
        })
    return JsonResponse({'syllabi': data})


@require_http_methods(['GET'])
def pyqs_list(request):

    branch = request.GET.get('branch', None)
    exam_type = request.GET.get('exam_type', None)
    year = request.GET.get('year', None)
    search = request.GET.get('search', '').strip()

    qs = PYQ.objects.all().order_by('-year')
    if branch and branch != 'all':
        qs = qs.filter(branch__code=branch)
    if exam_type and exam_type != 'all':
        qs = qs.filter(exam_type=exam_type)
    if year and year != 'all':
        qs = qs.filter(year=year)

    if search:
        qs = qs.filter(
            models.Q(subject__icontains=search)
            | models.Q(branch__code__icontains=search)
            | models.Q(semester__icontains=str(search))
            | models.Q(year__icontains=str(search))
        )

    data = []
    for p in qs:
        data.append({
            'id': p.id,
            'subject': p.subject,
            'branch': p.branch.code,
            'semester': p.semester,
            'year': p.year,
            'exam_type': p.exam_type,
            'pdf_url': p.pdf_url if hasattr(p, 'pdf_url') and p.pdf_url else (p.pdf_link or (p.pdf_file.url if p.pdf_file else '')),
        })

    return JsonResponse({'pyqs': data})


# Doubts and replies for all logged in users


# --------------------- DOUBTS ---------------------
@require_http_methods(['GET'])
def doubts_list(request):
    status_filter = request.GET.get('status', 'all')
    qs = Doubt.objects.select_related('branch', 'asked_by')
    if status_filter == 'open':
        qs = qs.filter(is_solved=False)
    elif status_filter == 'solved':
        qs = qs.filter(is_solved=True)
    data = []
    for d in qs:
        replies = [{'by': r.user.username, 'answer': r.answer, 'is_best': r.is_best} for r in d.replies.all()]
        data.append({
            'id': d.id, 'title': d.title, 'description': d.description, 'subject': d.subject,
            'branch': d.branch.code, 'semester': d.semester,
            'asked_by': d.asked_by.username, 'asked_at': d.asked_at.strftime('%Y-%m-%d'),
            'is_solved': d.is_solved, 'views': d.views, 'replies': replies,
        })
    return JsonResponse({'doubts': data})

@login_required
@require_http_methods(['POST'])
def ask_doubt(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    subject = request.POST.get('subject')
    branch_code = request.POST.get('branch')
    semester = request.POST.get('semester')
    if not all([title, description, subject, branch_code, semester]):
        return JsonResponse({'error': 'Missing fields'}, status=400)
    branch = Branch.objects.get(code=branch_code)
    doubt = Doubt.objects.create(
        title=title, description=description, subject=subject, branch=branch,
        semester=semester, asked_by=request.user
    )
    return JsonResponse({'id': doubt.id, 'message': 'Doubt posted'})

@login_required
@require_http_methods(['POST'])
def reply_to_doubt(request, doubt_id):
    answer = request.POST.get('answer')
    if not answer:
        return JsonResponse({'error': 'Answer required'}, status=400)

    doubt = Doubt.objects.select_related('asked_by').get(id=doubt_id)

    # Strict constraint: only one reply per doubt.
    # After the first reply, the doubt is considered solved and no more replies are allowed.
    if doubt.is_solved:
        return JsonResponse({'error': 'This doubt is already solved. No further replies are allowed.'}, status=403)

    if doubt.replies.exists():
        # Safety net in case is_solved is out-of-sync.
        doubt.is_solved = True
        doubt.save(update_fields=['is_solved'])
        return JsonResponse({'error': 'This doubt already has a reply and is now treated as solved.'}, status=403)

    # Only one reply allowed per doubt.
    # Do NOT auto-mark best/solved here.
    # Best answer will be selected by the doubt asker via mark_best_reply.
    reply = Reply.objects.create(
        doubt=doubt,
        user=request.user,
        answer=answer,
        is_best=False,
    )

    return JsonResponse({'message': 'Reply added', 'reply_id': reply.id, 'doubt_id': doubt.id})

@login_required
@require_http_methods(['POST'])
def mark_best_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    if reply.doubt.asked_by != request.user and request.user.role != 'admin':
        return JsonResponse({'error': 'Only doubt asker can mark best answer'}, status=403)
    # mark selected reply as best and finalize doubt
    reply.doubt.replies.update(is_best=False)
    reply.is_best = True
    reply.save(update_fields=['is_best'])

    if not reply.doubt.is_solved:
        reply.doubt.is_solved = True
        reply.doubt.save(update_fields=['is_solved'])

    return JsonResponse({'message': 'Best answer marked'})

# --------------------- PROFILE ---------------------
@login_required
def profile_data(request):
    user = request.user
    return JsonResponse({
        'name': user.get_full_name() or user.username,
        'username': user.username,
        'email': user.email,
        'branch': user.branch.code if user.branch else '',
        'semester': user.semester,
        'college': user.college,
        'bio': user.bio,
        'avatar': user.avatar,
        'role': user.role,
    })

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def update_profile(request):
    user = request.user
    user.first_name = request.POST.get('name', user.first_name)
    user.college = request.POST.get('college', user.college)
    user.bio = request.POST.get('bio', user.bio)
    if request.POST.get('branch'):
        user.branch = Branch.objects.get(code=request.POST.get('branch'))
    if request.POST.get('semester'):
        user.semester = request.POST.get('semester')
    if request.POST.get('avatar'):
        user.avatar = request.POST.get('avatar')
    user.save()
    return JsonResponse({'message': 'Profile updated'})