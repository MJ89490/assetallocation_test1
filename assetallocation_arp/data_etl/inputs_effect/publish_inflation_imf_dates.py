import pandas as pd

"""
Dates is a list of publishing dates for imf inflation
The list needs to be updated with the latest publishing dates
"""

dates_imf_publishing = {'19-04-2006': 'Apr2006',
                        '14-09-2006': 'Sep2006',
                        '11-04-2007': 'Apr2007',
                        '17-10-2007': 'Oct2007',
                        '09-04-2008': 'Apr2008',
                        '08-10-2008': 'Oct2008',
                        '22-04-2009': 'Apr2009',
                        '01-10-2009': 'Oct2009',
                        '21-04-2010': 'Apr2010',
                        '06-10-2010': 'Oct2010',
                        '11-04-2011': 'Apr2011',
                        '20-09-2011': 'Sep2011',
                        '17-04-2012': 'Apr2012',
                        '09-10-2012': 'Oct2012',
                        '16-04-2013': 'Apr2013',
                        '08-10-2013': 'Oct2013',
                        '08-04-2014': 'Apr2014',
                        '07-10-2014': 'Oct2014',
                        '14-04-2015': 'Apr2015',
                        '06-10-2015': 'Oct2015',
                        '12-04-2016': 'Apr2016',
                        '04-10-2016': 'Oct2016',
                        '12-04-2017': 'Apr2017',
                        '10-10-2017': 'Oct2017',
                        '17-04-2018': 'Apr2018',
                        '09-10-2018': 'Oct2018',
                        '09-04-2019': 'Apr2019',
                        '15-10-2019': 'Oct2019',
                        '11-04-2020': 'Apr2020'
                        }


def update_dates(date_publication):
    """
    Function which updates the dates_imf_publishing text file.
    These dates are used for the inflation release
    :param date_publication: string date corresponding to the imf publication date
    """

    dates_imf_publishing = {}

    full_months = {4: 'Apr', 10: 'Oct', 9: 'Sep'}
    date_tmp = pd.to_datetime(date_publication, format='%d-%m-%Y')

    date_publishing = full_months[date_tmp.month] + str(date_tmp.year)

    dates_imf_publishing[date_publication] = date_publishing

    with open("dates_imf_publishing.txt", 'a') as f:
        for key, value in dates_imf_publishing.items():
            f.write('%s %s' % (key, value) + '\n')


def read_dates_imf_publishing_text():
    """
    Functions which reads the dates_imf_publishing text file.
    :return: a dictionnary with the dates imf
    """
    dates_imf = {}
    with open("dates_imf_publishing.txt") as f:
        for line in f:
            if line != '\n':
                (key, val) = line.split()
                dates_imf[key] = val
            else:
                continue
    return dates_imf

# if __name__=="__main__":
#     update_dates('11-04-2021')
#     print(read_dates_imf_publishing_text())