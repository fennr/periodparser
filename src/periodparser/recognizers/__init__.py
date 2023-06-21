from typing import List

from periodparser.recognizers.dates_period_recognizer import DatesPeriodRecognizer
from periodparser.recognizers.day_of_week_recognizer import DayOfWeekRecognizer
from periodparser.recognizers.days_month_recognizer import DaysMonthRecognizer
from periodparser.recognizers.holidays_recognizer import HolidaysRecognizer
from periodparser.recognizers.month_recognizer import MonthRecognizer
from periodparser.recognizers.part_of_day_recognizer import PartOfDayRecognizer
from periodparser.recognizers.recognizer import Recognizer
from periodparser.recognizers.relative_date_recognizer import RelativeDateRecognizer
from periodparser.recognizers.relative_day_recognizer import RelativeDayRecognizer
from periodparser.recognizers.time_recognizer import TimeRecognizer
from periodparser.recognizers.time_span_recognizer import TimeSpanRecognizer
from periodparser.recognizers.year_recognizer import YearRecognizer

recognizers: List[Recognizer] = [
    HolidaysRecognizer(),
    DatesPeriodRecognizer(),
    DaysMonthRecognizer(),
    MonthRecognizer(),
    RelativeDayRecognizer(),
    TimeSpanRecognizer(),
    YearRecognizer(),
    RelativeDateRecognizer(),
    DayOfWeekRecognizer(),
    TimeRecognizer(),
    PartOfDayRecognizer(),
]
