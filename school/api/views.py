from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse

from school.models import Course, EnrolledIn, AssistsIn, Lecture, Assignment
from users.models import User
from school.api.serializers import CourseSerializer, LectureSerializer, AssignmentSerializer, EnrolledInSerializer
from users.api.serializers import UserSerializer
from users.models import Student, Instructor

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_list(request):
    user = request.user

    if request.method == 'GET':
        instructor = Instructor.objects.filter(user=user).first()
        if not instructor and not user.is_superuser:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)
        
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not user.is_superuser:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lecture_list(request, **kwargs):
    try:
        course = Course.objects.get(pk=kwargs.get('course_id'))
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if request.method == 'GET':
        # Determine if request was made by a student or an instructor
        student = Student.objects.filter(user=user).first()
        instructor = Instructor.objects.filter(user=user).first()

        # Request by student
        # Student can't access lectures unless they are enrolled in or assist in it
        if student:
            if (not EnrolledIn.objects.filter(student=student, course=course).exists() and
                not AssistsIn.objects.filter(student=student, course=course).exists()):
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        # Instructors and superusers can access any single course
        elif instructor:
            if instructor!=course.instructor:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)
        else:
            if not user.is_superuser:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        lectures = Lecture.objects.filter(course=course)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not user.is_superuser:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def assignment_list(request, **kwargs):
    try:
        course = Course.objects.get(pk=kwargs.get('course_id'))
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if request.method == 'GET':
        # Determine if request was made by a student or an instructor
        student = Student.objects.filter(user=user).first()
        instructor = Instructor.objects.filter(user=user).first()

        # Request by student
        # Student can't access assignments unless they are enrolled in or assist in it
        if student:
            if (not EnrolledIn.objects.filter(student=student, course=course).exists() and
                not AssistsIn.objects.filter(student=student, course=course).exists()):
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        # Instructors and superusers can access any single course
        elif instructor:
            if instructor!=course.instructor:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)
        else:
            if not user.is_superuser:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        assignments = Assignment.objects.filter(course=course)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not user.is_superuser:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def enrollment_list(request, **kwargs):
    try:
        course = Course.objects.get(pk=kwargs.get('course_id'))
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if request.method == 'GET':
        # Determine if request was made by a student or an instructor
        student = Student.objects.filter(user=user).first()
        instructor = Instructor.objects.filter(user=user).first()

        # Request by student
        # Student can't access assignments unless they are enrolled in or assist in it
        if student:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        # Instructors and superusers can access any single course
        elif instructor:
            if instructor!=course.instructor:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)
        else:
            if not user.is_superuser:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        students = EnrolledIn.objects.filter(course=course).values('student')
        users = User.objects.filter(id__in=students)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not user.is_superuser:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        print(request.data)
        request.data['student'] = 2
        request.data['course'] = kwargs.get('course_id')
        print(request.data)
        serializer = EnrolledInSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if request.method == 'GET':
        # Determine if request was made by a student or an instructor
        student = Student.objects.filter(user=user).first()
        instructor = Instructor.objects.filter(user=user).first()

        # Request by student
        # Student can't access course unless they are enrolled in or assist in it
        if student:
            if (not EnrolledIn.objects.filter(student=student, course=course).exists() and
                not AssistsIn.objects.filter(student=student, course=course).exists()):
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        # Instructors and superusers can access any single course
        else:
            if not instructor and not user.is_superuser:
                return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    if request.method == 'DELETE':
        if not user.is_superuser:
            return Response({'message': "Error: you do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN)

        operation = course.delete()
        data = {}
        if operation:
            data['success'] = "Course successfully deleted"
        else:
            data['failure'] = "Unable to delete course"

        return Response(data=data)