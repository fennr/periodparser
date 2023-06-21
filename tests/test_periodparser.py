import unittest
from datetime import datetime

from src.periodparser import extract
from src.periodparser.models.parser_models import DateTimeTokenType


class BaseParserTests(unittest.TestCase):
    def test_no_dates(self):
        result = extract("в день, какой неведомо, в никаком году")
        assert len(result.dates) == 0

    def test_january(self):
        starting_point = datetime(2019, 10, 13)
        result = extract("10 января событие", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.date_from.day == 10
        assert date.date_from.month == 1
        assert date.date_from.year == 2020

    def test_time_period_before_day(self):
        starting_point = datetime(2019, 10, 13)
        result = extract("c 5 до 7 вечера в понедельник будет событие", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.date_from.hour == 17
        assert date.date_to.hour == 19
        assert date.date_from.day == 14
        assert date.date_to.day == 14

    def test_time_period_simple(self):
        starting_point = datetime(2019, 10, 13)
        result = extract("c 10 до 13 событие", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        assert date.date_from.hour == 10
        assert date.date_to.hour == 13

    def test_daytime(self):
        starting_point = datetime(2019, 10, 14)
        result = extract("Завтра в час обед и продлится он час c небольшим", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert date.date_from.hour == 13

    def test_nighttime(self):
        starting_point = datetime(2020, 1, 1)
        result = extract(
            "Завтра в 2 ночи полнолуние, a затем в 3 часа ночи новолуние и наконец в 12 часов ночи игра.",
            starting_point,
        )
        assert len(result.dates) == 3

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert date.date_from.hour == 2

        date = result.dates[1]
        assert date.type == DateTimeTokenType.FIXED
        assert date.date_from.hour == 3

        date = result.dates[2]
        assert date.type == DateTimeTokenType.FIXED
        assert date.date_from.hour == 0
        assert date.date_from.day == 1

    def test_long_period(self):
        starting_point = datetime(2019, 10, 14)
        result = extract(
            "C вечера следующей среды до четверти 10 утра понедельника в декабре можно будет наблюдать снег",
            starting_point,
        )
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        assert date.date_from.year == 2019
        assert date.date_from.day == 23
        assert date.date_from.month == 10
        assert date.date_to.day == 2
        assert date.date_to.month == 12
        assert date.date_to.hour == 9
        assert date.date_to.minute == 15

    def test_collapse_complex(self):
        starting_point = datetime(2019, 10, 13)
        result = extract("B понедельник в 9 и 10 вечера", starting_point)
        assert len(result.dates) == 2

        date = result.dates[0]
        assert date.date_from.year == 2019
        assert date.date_from.day == 14
        assert date.date_from.hour == 21

        date = result.dates[1]
        assert date.date_from.day == 14
        assert date.date_from.hour == 22

        result = extract("B понедельник в 10 и 9 вечера", starting_point)
        assert len(result.dates) == 2

        date = result.dates[0]
        assert date.date_from.year == 2019
        assert date.date_from.day == 14
        assert date.date_from.hour == 22

        date = result.dates[1]
        assert date.date_from.day == 14
        assert date.date_from.hour == 21

    def test_multiple_simple(self):
        starting_point = datetime(2019, 10, 13)
        result = extract(
            "Позавчера в 6:30 состоялось совещание, a завтра днём будет хорошая погода.",
            starting_point,
        )
        assert len(result.dates) == 2

        date = result.dates[0]
        assert date.date_from.year == 2019
        assert date.date_from.day == 11
        assert date.date_from.hour == 6
        assert date.date_from.minute == 30

        date = result.dates[1]
        assert date.date_from.year == 2019
        assert date.date_from.day == 14
        assert True is date.has_time

    def test_collapse_direction(self):
        starting_point = datetime(2019, 10, 15)
        strings = [
            "B следующем месяце c понедельника буду ходить в спортзал!",
            "C понедельника в следующем месяце буду ходить в спортзал!",
        ]
        for s in strings:
            result = extract(s, starting_point)
            assert len(result.dates) == 1

            date = result.dates[0]
            assert date.date_from.year == 2019
            assert date.date_from.day == 4
            assert date.date_from.month == 11

    def test_weekday(self):
        starting_point = datetime(2019, 10, 13)
        result = extract("B следующем месяце во вторник состоится событие", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.date_from.year == 2019
        assert date.date_from.day == 5
        assert date.date_from.month == 11

        result = extract("Через месяц во вторник состоится событие", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.date_from.year == 2019
        assert date.date_from.day == 12
        assert date.date_from.month == 11

    def test_time_after_day(self):
        starting_point = datetime(2019, 10, 8)
        result = extract("в четверг 16 0 0 будет событие", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert True is date.has_time
        assert date.date_from.hour == 16
        assert date.date_from.day == 10

    def test_time_period(self):
        starting_point = datetime(2019, 9, 7)
        result = extract(
            "B следующий четверг c 9 утра до 6 вечера важный экзамен!", starting_point
        )
        assert len(result.dates) == 1

        date = result.dates[0]
        assert True is date.has_time
        assert date.date_from.hour == 9
        assert date.date_from.day == 12
        assert date.date_from.month == 9
        assert date.date_to.hour == 18
        assert date.date_to.day == 12
        assert date.date_to.month == 9
        assert date.date_from.year == 2019
        assert date.date_to.year == 2019

    def test_complex_period(self):
        starting_point = datetime(2019, 7, 7)
        result = extract(
            "хакатон c 12 часов 18 сентября до 12 часов 20 сентября", starting_point
        )
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        assert True is date.has_time
        assert date.date_from.hour == 12
        assert date.date_from.day == 18
        assert date.date_from.month == 9
        assert date.date_to.hour == 12
        assert date.date_to.day == 20
        assert date.date_to.month == 9
        assert date.date_from.year == 2019
        assert date.date_to.year == 2019

    def test_time_before_day(self):
        starting_point = datetime(2019, 9, 7)
        result = extract("B 12 часов 12 сентября будет встреча", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert True is date.has_time
        assert date.date_from.hour == 12
        assert date.date_from.day == 12
        assert date.date_from.month == 9

    def test_time_hour_of_day(self):
        starting_point = datetime(2019, 9, 7)
        result = extract("24 сентября в час дня", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert True is date.has_time
        assert date.date_from.hour == 13
        assert date.date_from.day == 24
        assert date.date_from.month == 9
        assert date.date_from.year == 2019

    def test_fix_period(self):
        starting_point = datetime(2019, 9, 7)
        result = extract("на выходных будет хорошо", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        assert date.date_from.day == 14
        assert date.date_to.day == 15

    def test_dates_period(self):
        starting_point = datetime(2019, 8, 6)
        strings = [
            "c 11 по 15 сентября будет командировка",
            "от 11 по 15 сентября будет командировка",
            "c 11 до 15 сентября будет командировка",
        ]
        for s in strings:
            result = extract(s, starting_point)
            assert len(result.dates) == 1

            date = result.dates[0]
            assert date.type == DateTimeTokenType.PERIOD
            assert date.date_from.day == 11
            assert date.date_to.day == 15
            assert date.date_from.month == 9
            assert date.date_to.month == 9

        starting_point = datetime(2019, 9, 6)
        result = extract("c 11 до 15 числа будет командировка", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        assert date.date_from.day == 11
        assert date.date_to.day == 15
        assert date.date_from.month == 9
        assert date.date_to.month == 9

    def test_days_of_week(self):
        starting_point = datetime(2019, 9, 6)
        result = extract("во вторник встреча c заказчиком", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert date.date_from.day == 10

    def test_holidays(self):
        starting_point = datetime(2019, 9, 2)
        result = extract("в эти выходные еду на дачу", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        assert date.date_from.day == 7
        assert date.date_to.day == 8

    def test_holiday(self):
        starting_point = datetime(2019, 9, 2)
        result = extract("пойду гулять в следующий выходной", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.FIXED
        assert date.date_from.day == 14
        assert date.date_to.day == 14

    def test_from_to_reversed(self):
        starting_point = datetime(2019, 10, 13)
        result = extract("c 2 до 5", starting_point)
        assert len(result.dates) == 1

        date = result.dates[0]
        assert date.type == DateTimeTokenType.PERIOD
        date_from = date.date_from
        date_to = date.date_to
        assert date_from.hour == 14
        assert date_to.hour == 17
        assert date_from.day == 13
        assert date_to.day == 13


# class BaseHorsTests(unittest.TestCase):


if __name__ == "__main__":
    unittest.main()
