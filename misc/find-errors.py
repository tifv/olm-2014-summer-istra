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

def main():
    driver = init_driver()
    authors = set()
    for metapath, metarecord in driver.items():
        if '$timetable' in metarecord and '$authors' not in metarecord:
            fprint('<RED>Missing authors in <BOLD>{}<RESET>'.format(metapath))
        if '$author' in metarecord:
            fprint('<RED>$author key present in <BOLD>{}<RESET>'.format(metapath))
        if '$authors' in metarecord:
            authors.update(metarecord['$authors'])
    fprint(', '.join(sorted(authors, key=lambda s: s.split(' ')[-1])))

if __name__ == '__main__':
    main()

