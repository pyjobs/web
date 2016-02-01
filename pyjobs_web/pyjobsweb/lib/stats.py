# -*- coding: utf-8 -*-
import calendar
import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import func

from pyjobsweb.model import Job


class StatsQuestioner(object):
    """
        TODO: COMMENTAIRES
    """

    PERIOD_MONTH = 'mon'
    PERIOD_WEEK = 'week'

    FIELD_SOURCE = 0
    FIELD_COUNT = 1
    FIELD_DATE = 2

    @staticmethod
    def get_month_period(period_range):

        today = datetime.datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999)
        current_month = today.replace(day=1)
        last_day_of_current_month = calendar.monthrange(today.year, today.month)[1]

        if today.day == last_day_of_current_month:
            date_from = current_month + relativedelta(months=-period_range - 1)
            date_to = today
        else:
            date_from = current_month + relativedelta(months=-period_range)
            date_to = current_month - datetime.timedelta(days=1)

        return date_from, date_to

    @classmethod
    def extract(cls, query_result, field):
        return sorted(set([r[field] for r in query_result]))

    @classmethod
    def extract_stats(cls, query_result):
        periods = cls.extract(query_result, cls.FIELD_DATE)
        sources = cls.extract(query_result, cls.FIELD_SOURCE)

        stats = {}
        for source in sources:
            stats[source] = {}
            for period in periods:
                for query_line in query_result:
                    query_line_source, query_line_jobs_count, query_line_date = query_line
                    if query_line_source == source \
                            and query_line_date == period:
                        stats[source][period] = query_line_jobs_count
                if period not in stats[source]:
                    stats[source][period] = 0

        return stats

    def __init__(self, session):
        self._session = session

    def by_complete_period(self, period, date_from, date_to):
        """
        TODO - B.S. - 20160201: Model depuis la requête ?
        :param period:
        :param date_from:
        :param date_to:
        :return:
        """
        date_trunc_func = func.date_trunc(period, Job.publication_datetime)
        return self._session.query(Job.source, func.count(Job.id), date_trunc_func) \
            .filter(Job.publication_datetime >= date_from) \
            .filter(Job.publication_datetime <= date_to) \
            .group_by(Job.source) \
            .group_by(date_trunc_func) \
            .order_by(date_trunc_func)
