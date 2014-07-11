#!/usr/bin/python3

from collections import OrderedDict
from datetime import date as date_type

from jeolm.filesystem import FilesystemManager
from jeolm.metadata import MetadataManager
from jeolm.records import RecordPath
from jeolm.fancify import fancifying_print as fprint


def init_driver():
    fs = FilesystemManager()
    md = MetadataManager(fs=fs)
    md.load_metadata()
    Driver = fs.find_driver_class()
    driver = md.feed_metadata(Driver())
    return driver

def main(listed_groups):
    driver = init_driver()
    timetable = OrderedDict(
        (group, OrderedDict(
            (date, OrderedDict(
                (period, []) for period in periodlist
            ))
            for date, periodlist in groupvalue['timetable'].items()
        ))
        for group, groupvalue in driver.groups.items()
    )
    timetable_extra = driver.getitem(RecordPath())['$timetable$extra']
    for group, group_value in timetable_extra.items():
        for date, date_value in group_value.items():
            for period, extra in date_value.items():
                assert isinstance(extra, str)
                if 'ЖОПА' in extra:
                    extra = '<RED><BOLD>{}<RESET>'.format(extra)
                else:
                    extra = '<YELLOW>{}<RESET>'.format(extra)
                timetable[group][date][period].append(extra)
    for metapath, metarecord, group, date, period in driver.list_timetable():
        timetable[group][date][period].append('<GREEN>{}<RESET>'.format(metapath))
    if listed_groups is None:
        listed_groups = list(driver.groups)
    for group in listed_groups:
        fprint('<MAGENTA>=== <BOLD>{}<RESET><MAGENTA> ===<RESET>'.format(group))
        for date, date_value in timetable[group].items():
            if not any(date_value.values()) and date > date_type.today():
                continue
            fprint('\t<CYAN><BOLD>{}<RESET>'.format(date))
            for period, value in date_value.items():
                assert isinstance(value, list), type(value)
                if not value:
                    value = '<RED><BOLD>!!! ЖОПА !!!<RESET>'
                else:
                    value = ', '.join(value)
                fprint('\t\t<CYAN>{}: <RESET>{}'.format(period, value))

if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        cmd, *listed_groups = argv
    else:
        listed_groups = None
    main(listed_groups)

