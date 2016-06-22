# -*- coding: utf-8 -*-
import calendar
import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import func

from pyjobsweb.model import JobOfferSQLAlchemy


class StatsQuestioner(object):
    """
        Provide database query method and query result formatting.
    """

    PERIOD_MONTH = 'mon'
    PERIOD_WEEK = 'week'

    FIELD_SOURCE = 0
    FIELD_COUNT = 1
    FIELD_DATE = 2

    FIELDS = {
        FIELD_SOURCE: 'source',
        FIELD_COUNT: 'jobs',
        FIELD_DATE: 'date'
    }

    FLAT_Y_FIELD = FIELD_SOURCE
    FLAT_X_FIELD = FIELD_DATE

    @staticmethod
    def get_month_period(period_range):
        """
        return a start date and a end date of x complete previous month
        :param period_range: number of months
        :return: date_from (datetime), date_to (datetime)
        """

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
        """
        Simple make a list containing asked field value from query_result
        :param query_result: result from StatsQuestioner query
        :param field: field to be extracted
        :return: list containing asked field value from query_result
        """
        return sorted(set([r[field] for r in query_result]))

    @classmethod
    def extract_stats(cls, query_result, sources):
        """
        Return a dict of stats: { source_name: { datetime: { job_count } } }
        :param query_result: result from StatsQuestioner query
        :param sources: pyjobs_crawler sources
        :return: dict of sources where keys value are dict of date:jobs_count
        """
        periods = cls.extract(query_result, cls.FIELD_DATE)

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

    @classmethod
    def flat_query_by_y(cls, query_result, sources, date_value_callback=lambda date: date.strftime('%Y-%m-%d')):
        """
        Return flatted stats: [{date: 'YYYY-mm-dd', source_1: job_count, source_2: job_count, source_...}, ...]
        :param query_result: result from StatsQuestioner query
        :param sources: pyjobs_crawler sources
        :param date_value_callback: callback used to format
        :return: list of flatted stats dicts
        """
        periods = cls.extract(query_result, cls.FIELD_DATE)

        flat = []
        for period in periods:
            flat_line = cls.extract_flat_dict_for_field(
                query_result=query_result,
                where_field=cls.FLAT_X_FIELD,
                where_field_value=period,
                flat_field_key=cls.FLAT_Y_FIELD,
                flat_field_value=cls.FIELD_COUNT,
                sources=sources
            )
            # Stringify date
            flat_line[cls.FIELDS[cls.FIELD_DATE]] = date_value_callback(flat_line[cls.FIELDS[cls.FIELD_DATE]])
            flat.append(flat_line)

        return flat

    @classmethod
    def extract_flat_dict_for_field(cls, query_result, where_field, where_field_value, flat_field_key, flat_field_value,
                                    sources):
        """
        return a flatted dict based on field correspondence:
            {based_field_name: based_field_value, source_1: source_1_value, source_2: source_2_value, ...}
        Sources not found in query_result for field correspondence are filled by 0.
        :param query_result: result from StatsQuestioner query
        :param where_field: based field
        :param where_field_value:  based field value
        :param flat_field_key: field where apply flatting (eg. source)
        :param flat_field_value: field to use for value of flat_field_key in dict (eg. count)
        :param sources: pyjobs_crawler sources
        :return: flatted dict
        """
        extracted_dict = {cls.FIELDS[where_field]: where_field_value}

        for result_line in query_result:
            if result_line[where_field] == where_field_value:
                extracted_dict[result_line[flat_field_key]] = result_line[flat_field_value]

        for source in sources:
            if source not in extracted_dict:
                extracted_dict[source] = 0

        return extracted_dict

    def __init__(self, session):
        self._session = session

    def by_complete_period(self, period, date_from, date_to):
        """

        :param period: period unit (eg StatsQuestioner.PERIOD_MONTH)
        :param date_from: start date of concerned jobs
        :param date_to: end date of concerned jobs
        :return: sqlalchemy Query
        :rtype: sqlalchemy.orm.Query
        """
        # TODO - B.S. - 20160204: date_trunc only compatible with postgresql
        date_trunc_func = func.date_trunc(period, JobOfferSQLAlchemy.publication_datetime)
        return self._session.query(JobOfferSQLAlchemy.source, func.count(JobOfferSQLAlchemy.id), date_trunc_func) \
            .filter(JobOfferSQLAlchemy.publication_datetime >= date_from) \
            .filter(JobOfferSQLAlchemy.publication_datetime <= date_to) \
            .group_by(JobOfferSQLAlchemy.source) \
            .group_by(date_trunc_func) \
            .order_by(date_trunc_func)
