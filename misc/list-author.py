#!/usr/bin/python3

from jeolm.filesystem import FilesystemManager
from jeolm.metadata import MetadataManager
from jeolm.fancify import fancifying_print as fprint

def init_driver():
    fs = FilesystemManager()
    md = MetadataManager(fs=fs)
    md.load_metadata()
    Driver = fs.find_driver_class()
    driver = md.feed_metadata(Driver())
    return driver

def main(listed_authors):
    driver = init_driver()
    if listed_authors is None:
        def condition(authors): return True
    else:
        def condition(authors): return frozenset(authors).intersection(listed_authors)
    for metapath, metarecord in driver.items():
        if '$authors' not in metarecord:
            continue
        if not condition(metarecord['$authors']):
            continue
        fprint('<GREEN><BOLD>{}<RESET>'.format(metapath))
        fprint('  <GREEN>{}<RESET>'.format(', '.join(metarecord['$authors'])))
        if '$timetable' not in metarecord:
            continue
        fprint('  <CYAN>{}<RESET>'.format(', '.join(sorted(
            metarecord['$timetable']
        ))))

if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        cmd, *listed_authors = argv
        main(listed_authors)
    else:
        main(None)

