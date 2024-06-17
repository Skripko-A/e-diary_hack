import random

from datacenter.models import Schoolkid, Mark, Chastisement, Teacher, Lesson, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def replace_bad_marks(school_kid):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=school_kid)
    except ObjectDoesNotExist:
        return 'Исправьте опечатку в имени ученика'
    except MultipleObjectsReturned:
        return 'Уточните ФИО ученика'
    bad_marks = Mark.objects.filter(schoolkid_id=schoolkid.id, points__in=[2, 3])
    good_mark_points = random.randint(4, 5)
    for bad_mark in bad_marks:
        bad_mark.points = good_mark_points
        bad_mark.save()
    return bad_marks.count()


def delete_chastisements(school_kid):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=school_kid)
    except ObjectDoesNotExist:
        return 'Исправьте опечатку в имени ученика'
    except MultipleObjectsReturned:
        return 'Уточните ФИО ученика'
    chastisements = Chastisement.objects.filter(schoolkid_id=schoolkid.id)
    chastisements.delete()
    return chastisements.count()


def create_commendation(school_kid, subject_title):
    commendations = open('commendation_texts.txt', 'r').read()
    while '  ' in commendations:
        commendations = commendations.replace('  ', ' ')
    commendations = commendations.replace('\n', '')
    commendations = tuple(commendations.split(sep='!, '))
    random_commendation = random.choice(commendations)
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=school_kid)
    except ObjectDoesNotExist:
        return 'Исправьте опечатку в имени ученика'
    except MultipleObjectsReturned:
        return 'Уточните ФИО ученика'
    last_lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                        year_of_study=schoolkid.year_of_study,
                                        subject__title=subject_title).last()
    if last_lesson is None:
        return 'Исправьте опечатку в названии предмета'
    random_teacher_id = random.choice(Teacher.objects.all()).id
    Commendation.objects.create(text=random_commendation,
                                schoolkid_id=schoolkid.id,
                                created=last_lesson.date,
                                subject_id=last_lesson.subject.id,
                                teacher_id=random_teacher_id)
    return random_commendation
