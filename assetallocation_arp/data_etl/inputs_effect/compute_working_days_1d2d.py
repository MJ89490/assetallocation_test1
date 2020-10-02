"""
@author: LK69943
@email: laura.kane@lgim.com
date: 11/07/2019
description: working days library for the 1D and 2D model
"""

import QuantLib as ql
import datetime as dt
import pandas as pd


class ComputeWorkingDays1D2D:

    @staticmethod
    def ql_to_dt(x):
        """

        :param x: QuantLib date
        :return: converts the Date column in a Dataframe from QuantLib format to datetime format
        """
        return dt.date(x.year(), x.month(), x.dayOfMonth())

    @staticmethod
    def dt_to_ql(x):
        """

        :param x: datetime or date
        :return: converts the EndDate column in a Dataframe from datetime format to QuantLib format
        """
        d = int(x.strftime("%d"))
        m = int(x.strftime("%m"))
        y = int(x.strftime("%Y"))

        return ql.Date(d, m, y)

    @staticmethod
    def working_days(start_date, end_date, wd_tenor):
        """

        :param start_date: datetime date, start date of strategy
        :param end_date: datetime date, end date of strategy
        :param wd_tenor: quantlib tenor, e.g. ql.Daily, ql.Weekly
        defines if you would like daily / weekly dates, etc.
        :return: creates dataframe of every working day between the start and end date
        refers to UK holiday calendar
        """
        # Convert dates to QuantLib
        start_date = ComputeWorkingDays1D2D.dt_to_ql(start_date)
        end_date = ComputeWorkingDays1D2D.dt_to_ql(end_date)

        # Find every working day between the start and end date
        df = []

        tenor = ql.Period(wd_tenor)  # tenor = ql.Period(ql.Daily)
        calendar = ql.UnitedKingdom()
        business_convention = ql.Following
        termination_business_convention = ql.Following
        date_generation = ql.DateGeneration.Forward
        end_of_week = True
        schedule = ql.Schedule(start_date,
                               end_date,
                               tenor,
                               calendar,
                               business_convention,
                               termination_business_convention,
                               date_generation,
                               end_of_week)

        for i, d in enumerate(schedule):
            df.append(d)

        df = pd.DataFrame(df, columns=['Date'])  # convert to dataframe
        df['Date'] = df['Date'].apply(ComputeWorkingDays1D2D.ql_to_dt)  # convert date to datetime

        return df

    @staticmethod
    def date_add_yr(start_date, n):
        start_date = ComputeWorkingDays1D2D.dt_to_ql(start_date)
        new_date = start_date + ql.Period(n, ql.Years)
        new_date = ComputeWorkingDays1D2D.ql_to_dt(new_date)
        return new_date

    @staticmethod
    def date_add_month(start_date, n):
        start_date = ComputeWorkingDays1D2D.dt_to_ql(start_date)
        new_date = start_date + ql.Period(n, ql.Months)
        new_date = ComputeWorkingDays1D2D.ql_to_dt(new_date)
        return new_date

    @staticmethod
    def convert_to_working_date_uk(dt_date):
        """
        :param dt_date: datetime date
        :return: datetime date, the working day version, according to the UK bank holiday calendar;
        if enter non-working day, will find previous working day
        """
        uk_calendar = ql.UnitedKingdom()
        ql_date = ComputeWorkingDays1D2D.dt_to_ql(dt_date)
        ql_date = uk_calendar.advance(ql_date, ql.Period(1, ql.Days))
        ql_date = uk_calendar.advance(ql_date, ql.Period(-1, ql.Days))
        dt_date = ComputeWorkingDays1D2D.ql_to_dt(ql_date)
        return dt_date

    @staticmethod
    def convert_to_working_ql_date_uk(ql_date):
        """

        :param dt_date: datetime date
        :return: datetime date, the working day version, according to the UK bank holiday calendar;
        if enter non-working day, will find previous working day
        """
        uk_calendar = ql.UnitedKingdom()
        ql_date = uk_calendar.advance(ql_date, ql.Period(1, ql.Days))
        ql_date = uk_calendar.advance(ql_date, ql.Period(-1, ql.Days))
        return ql_date

    @staticmethod
    def get_previous_month_end(today):
        first_of_month = dt.date(today.year, today.month, 1)
        month_end = first_of_month - dt.timedelta(days=1)

        return ComputeWorkingDays1D2D.convert_to_working_date_uk(month_end)
