from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Event, Registration, Attendance, Feedback
from django.db.models import Count, Q

# ---------------------------
# Student registers for an event
# ---------------------------
@csrf_exempt
def register_student(request):
    student_id = request.GET.get('student_id')
    event_id = request.GET.get('event_id')

    if not (student_id and event_id):
        return JsonResponse({"error": "Missing student_id or event_id"}, status=400)

    registration, created = Registration.objects.get_or_create(
        student_id=student_id, event_id=event_id
    )

    if created:
        return JsonResponse({"msg": "Student registered successfully"})
    else:
        return JsonResponse({"msg": "Student already registered"})


# ---------------------------
# Mark attendance
# ---------------------------
@csrf_exempt
def mark_attendance(request):
    student_id = request.GET.get('student_id')
    event_id = request.GET.get('event_id')
    status = request.GET.get('status', 'Present')

    if not (student_id and event_id):
        return JsonResponse({"error": "Missing student_id or event_id"}, status=400)

    Attendance.objects.update_or_create(
        student_id=student_id, event_id=event_id, defaults={'status': status}
    )
    return JsonResponse({"msg": "Attendance marked"})


# ---------------------------
# Submit feedback
# ---------------------------
@csrf_exempt
def submit_feedback(request):
    student_id = request.GET.get('student_id')
    event_id = request.GET.get('event_id')
    rating = request.GET.get('rating')

    if not (student_id and event_id and rating):
        return JsonResponse({"error": "Missing student_id, event_id, or rating"}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return JsonResponse({"error": "Rating must be between 1 and 5"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid rating"}, status=400)

    Feedback.objects.update_or_create(
        student_id=student_id, event_id=event_id, defaults={'rating': rating}
    )
    return JsonResponse({"msg": "Feedback submitted"})


# ---------------------------
# Reports
# ---------------------------

# Event Popularity Report
def event_popularity(request):
    data = Event.objects.all().values("name").annotate(
        registrations=Count("registration")
    ).order_by("-registrations")
    return JsonResponse(list(data), safe=False)


# Student Participation Report
def student_participation(request):
    data = Student.objects.all().values("name").annotate(
        attended=Count("attendance", filter=Q(attendance__status="Present"))
    ).order_by("-attended")
    return JsonResponse(list(data), safe=False)
