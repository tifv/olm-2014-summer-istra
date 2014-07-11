#!/usr/bin/python3

from collections import OrderedDict

from jeolm.filesystem import FilesystemManager
from jeolm.metadata import MetadataManager
from jeolm.records import RecordPath
from jeolm.target import Target

TABLE_STYLE = (r"""
<style>
table, th, td
{
border-collapse:collapse;
border:1px solid black;
}
th, td
{
padding:5px;
}
</style>
""")

def init_driver():
    fs = FilesystemManager()
    md = MetadataManager(fs=fs)
    md.load_metadata()
    Driver = fs.find_driver_class()
    driver = md.feed_metadata(Driver())
    return driver

def main(targets, *, pdf_base_link, source_base_link):
    print('<!DOCTYPE html><html><body><table>')
    print(TABLE_STYLE)
    print(
    '<tr>'
        '<th rowspan="2">Группы</th>'
        '<th rowspan="2">Название</th>'
        '<th rowspan="2">Авторы</th>'
        '<th style="text-align:left;">PDF</th>'
    '</tr><tr>'
        '<th style="text-align:right;"><em>Исходник</em></th>'
    '</tr>' )

    driver = init_driver()
    groups = driver.groups
    targets = [
        delegated_target.flags_clean_copy(origin='target')
        for delegated_target
        in driver.list_delegated_targets(
            *targets, recursively=True )
    ]
    for target in targets:
        metarecord = driver[target.path]
        outrecord = driver.produce_outrecord(target)
        if target.flags.intersection(groups):
            group_indices = list(target.flags.intersection(groups))
        else:
            group_indices = sorted(list(metarecord['$timetable']), key=lambda x: list(groups).index(x))
        if '$caption' in metarecord:
            caption = metarecord['$caption']
        else:
            caption = '; '.join(metarecord['$source$sections'])
        caption = ( caption
            .replace(r'\ldots', '&hellip;')
            .replace('--', '&ndash;')
            .replace('~', '&nbsp;') );
        try:
            print(
            '<tr>'
                '<td rowspan="2">{group}</td>'
                '<td rowspan="2">{caption}</td>'
                '<td rowspan="2">{author}</td>'
                '<td style="text-align:left;">'
                    '<a href="{pdf_base_link}{pdf_name}">{pdf_name}</a>'
                '</td>'
            '</tr><tr>'
                '<td style="text-align:right;"><em>'
                    '<a href="{source_base_link}{source_path}">{source_path}</a>'
                '</em></td>'
            '</tr>'
                .format(
                    group=', '.join(
                        groups[group_index]['name']
                        for group_index in group_indices ),
                    caption=caption,
                    author=driver.constitute_authors(
                        metarecord['$authors'], thin_space='&nbsp;' ),
                    pdf_name=outrecord['outname'] + '.pdf',
                    source_path=target.path.as_inpath(suffix='.tex'),
                    pdf_base_link=pdf_base_link,
                    source_base_link=source_base_link,
                )
            )
        except:
            print('Problem in target {target}'.format(target=target))
            raise

#    for metapath, metarecord, group, date, period in driver.list_timetable():
#        timetable[group][date][period][metapath] = metarecord
#    for group in listed_groups:
#        print('<th colspan="5">{0[name]} ({0[code]})</th>'.format(group))
#        for date, date_value in timetable[group].items():
#            for period, period_value in date_value.items():
#                for metapath, metarecord
#                assert isinstance(value, list), type(value)
#                if not value:
#                    value = '<RED><BOLD>!!! ЖОПА !!!<RESET>'
#                else:
#                    value = ', '.join(value)
#                fprint('\t\t<CYAN>{}: <RESET>{}'.format(period, value))

    print('</table></body></html>')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf-base-link', required=True)
    parser.add_argument('--source-base-link', required=True)
    parser.add_argument('targets', nargs='+', type=Target.from_string)
    args = parser.parse_args()
    main( args.targets,
        pdf_base_link=args.pdf_base_link,
        source_base_link=args.source_base_link,
    )
