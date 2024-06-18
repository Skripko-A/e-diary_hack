import random

from datacenter.models import Schoolkid, Mark, Chastisement, Teacher, Lesson, Commendation


def get_schoolkid(school_kid):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=school_kid)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print('ФИО ученика не найдено, возможно у вас опечатка?')
    except Schoolkid.MultipleObjectsReturned:
        print('Уточните ФИО ученика, наёдено более одной записи')


def replace_bad_marks(school_kid):
    schoolkid = get_schoolkid(school_kid)
    if not schoolkid:
        return
    bad_marks = Mark.objects.filter(schoolkid_id=schoolkid.id, points__in=[2, 3])
    good_mark_points = random.randint(4, 5)
    for bad_mark in bad_marks:
        bad_mark.points = good_mark_points
        bad_mark.save()
    return bad_marks.count()


def delete_chastisements(school_kid):
    schoolkid = get_schoolkid(school_kid)
    if not schoolkid:
        return
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
    schoolkid = get_schoolkid(school_kid)
    if not schoolkid:
        return
    try:
        last_lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                            year_of_study=schoolkid.year_of_study,
                                            subject__title=subject_title).last()
        teacher_id = Teacher.objects.get(full_name=last_lesson.teacher).id

        Commendation.objects.create(text=random_commendation,
                                    schoolkid_id=schoolkid.id,
                                    created=last_lesson.date,
                                    subject_id=last_lesson.subject.id,
                                    teacher_id=teacher_id)
    except AttributeError:
        return 'Уточните название предмета'
    return random_commendation


