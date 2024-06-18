import random

from datacenter.models import Schoolkid, Mark, Chastisement, Teacher, Lesson, Commendation

COMMENDATIONS = (
    'Молодец', 'Отлично', 'Хорошо', 'Гораздо лучше, чем я ожидал', 'Ты меня приятно удивил', 'Великолепно', 'Прекрасно',
    'Ты меня очень обрадовал', 'Именно этого я давно ждал от тебя', 'Сказано здорово – просто и ясно',
    'Ты, как всегда, точен', 'Очень хороший ответ', 'Талантливо', 'Ты сегодня прыгнул выше головы', 'Я поражен',
    'Уже существенно лучше', 'Потрясающе', 'Замечательно', 'Прекрасное начало', 'Так держать', 'Ты на верном пути',
    'Здорово', 'Это как раз то, что нужно', 'Я тобой горжусь', 'С каждым разом у тебя получается всё лучше',
    'Мы с тобой не зря поработали', 'Я вижу, как ты стараешься', 'Ты растешь над собой', 'Ты многое сделал, я это вижу',
    'Теперь у тебя точно все получится!')


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
    Mark.objects.filter(schoolkid_id=schoolkid.id, points__in=[2, 3]).update(points=5)
    return 'Теперь ученик - круглый отличник'


def delete_chastisements(school_kid):
    schoolkid = get_schoolkid(school_kid)
    if not schoolkid:
        return
    chastisements = Chastisement.objects.filter(schoolkid_id=schoolkid.id)
    chastisements.delete()
    return 'Все замечания удалены'


def create_commendation(school_kid, subject_title):
    random_commendation = random.choice(COMMENDATIONS)
    schoolkid = get_schoolkid(school_kid)
    if not schoolkid:
        return
    try:
        last_lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                            year_of_study=schoolkid.year_of_study,
                                            subject__title=subject_title).last()
        if last_lesson is None:
            return 'Урок для похвалы не найден'
        teacher_id = last_lesson.teacher_id
        Commendation.objects.create(text=random_commendation,
                                    schoolkid_id=schoolkid.id,
                                    created=last_lesson.date,
                                    subject_id=last_lesson.subject.id,
                                    teacher_id=teacher_id)
    except AttributeError:
        return 'Уточните название предмета'
    return random_commendation
