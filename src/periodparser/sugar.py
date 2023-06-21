from datetime import datetime
from re import sub
from typing import Optional

from periodparser.models.parse_result import PeriodResult
from periodparser.text_parser import parse


def preprocess(phrase: str) -> str:
    # change forms
    phrase = phrase.replace("часок", "час")
    phrase = phrase.replace("часиков", "часов")
    phrase = phrase.replace("минуток", "минут")

    # translate times
    phrase = phrase.replace("полчаса", "30 минут")
    phrase = phrase.replace("полчасика", "30 минут")
    phrase = phrase.replace("полтора часа", "1 час 30 минут")
    phrase = phrase.replace("через пару часов", "через 2 часа")
    phrase = phrase.replace("в обед", "в 13 часов")
    phrase = phrase.replace("после обеда", "в 14 часов")

    # swap syntax
    phrase = sub(r"через (минут|часов|часа) (\d*)", r"через \2 \1", phrase)
    phrase = sub(r"(минут|часов|часа) через (\d*)", r"через \2 \1", phrase)
    phrase = sub(r"в течение (\w*a)", r"через \1", phrase)
    phrase = phrase.replace("получас", "30 минут")
    phrase = sub(r"(\d+) c половиной часа", r"\1 часа 30 минут", phrase)

    return phrase


def preprocess_today(phrase: str) -> str:
    phrase = phrase.replace("вечерком", "вечером").replace("ближе к вечеру", "вечером")
    phrase = sub(r"(вечером|днём|утром)", r"сегодня \1", phrase)
    return phrase


def extract(phrase: str, now: Optional[datetime] = None) -> PeriodResult:
    """
    Извлекает период времени из заданной фразы и возвращает объект PeriodResult
    
    :param phrase: A string representing a period of time.
    :type phrase: str
    :param now: An optional datetime object representing the current time. Defaults to None.
    :type now: Optional[datetime]
    :return: A PeriodResult object containing information about the extracted period of time.
    :rtype: PeriodResult
    """
    phrase = preprocess(phrase)
    now = now or datetime.now()

    period_result = parse(phrase, now)
    if not period_result.dates:
        phrase = preprocess_today(phrase)
        period_result = parse(phrase, now)

    return period_result
