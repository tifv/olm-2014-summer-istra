from string import Template

from jeolm.driver.regular import (
    Driver as RegularDriver, DriverError,
    RecordPath, RecordNotFoundError )

class Driver(RegularDriver):

    @property
    def groups(self):
        return self.getitem(RecordPath())['$groups']

    def list_timetable(self):
        for metapath, metarecord in self.items():
            if '$timetable' not in metarecord:
                continue
            for group, group_value in metarecord['$timetable'].items():
                assert isinstance(group_value, dict), metapath
                for date, date_value in group_value.items():
                    for period in date_value:
                        assert isinstance(period, int)
                        yield metapath, metarecord, group, date, period

    def extract_first_period(self, target, metarecord, group_flag):
        timetable = metarecord['$timetable'][group_flag]
        if timetable:
            first_date = min(timetable)
        else:
            return None, None
        if timetable[first_date]:
            first_period = min(timetable[first_date])
        else:
            return first_date, None
        return first_date, first_period

    def derive_attributes(self, parent_record, child_record, name):
        child_record.setdefault('$delegate$group',
            parent_record.get('$delegate$group', True) )
        super().derive_attributes(parent_record, child_record, name)

#    def select_outname(self, target, metarecord, date=None):
#        no_group = ( not target.flags.intersection(self.groups) or
#            '$timetable' not in metarecord or date is None)
#        if no_group:
#            return super().select_outname(target, metarecord, date=date)
#
#        group_flag, = target.flags.intersection(self.groups)
#        first_date, first_period = self.extract_first_period(
#            target, metarecord, group_flag )
#        date_prefix = (
#            '{0.year:04}-'
#            '{0.month:02}-'
#            '{0.day:02}-'
#            'p{1}'
#        ).format(first_date, first_period)
#        outname = date_prefix + '-' + '{target:outname}'.format(target=target)
#
#        return outname

    def select_outname(self, target, metarecord, date=None):
        return '{target:outname}'.format(target=target)

    @fetching_metarecord
    @processing_target_aspect(aspect='delegators', wrap_generator=True)
    def generate_delegators(self, target, metarecord):
        try:
            yield from super().generate_delegators(target, metarecord)
            return
        except self.NoDelegators:
            if not metarecord.get('$delegate$groups', True):
                raise
            if '$timetable' not in metarecord:
                for subname in metarecord:
                    if subname.startswith('$'):
                        continue
                    yield target.path_derive(subname)
            elif target.flags.intersection(self.groups):
                group_flags = target.flags.intersection(self.groups)
                if len(group_flags) != 1:
                    raise DriverError(target)
                group_flag, = group_flags
                if group_flag in metarecord['$timetable']:
                    # This is buildable path
                    raise self.NoDelegators
                else:
                    # Delegating to void
                    pass
            else:
                for group_flag in self.groups:
                    yield target.flags_union({group_flag})

    @processing_target_aspect(aspect='auto metabody', wrap_generator=True)
    @classifying_items(aspect='metabody', default='verbatim')
    def generate_auto_metabody(self, target, metarecord):
        if 'integral' not in target.flags:
            yield from super().generate_auto_metabody(target, metarecord)
            return
        if '$timetable' in metarecord:
            if len(metarecord['$timetable']) != 1:
                raise DriverError( "Unable to integrate {target}"
                    .format(target=target) )
            group_name, = metarecord['$timetable']
            yield target.flags_difference({'integral'})\
                .flags_union({group_name})
            yield self.substitute_clearpage()
        else:
            for subname in metarecord:
                if subname.startswith('$'):
                    continue
                yield target.path_derive(subname)

    @processing_target_aspect(aspect='header metabody', wrap_generator=True)
    @classifying_items(aspect='resolved_metabody', default='verbatim')
    def generate_header_metabody(self, target, metarecord, *, date):
#        if not target.flags.intersection(self.groups):
#            yield from super().generate_header_metabody(
#                target, metarecord, date=date )
#            return

        yield r'\begingroup'

        if '$authors' in metarecord:
            yield self.substitute_authorsdef(
                authors=self.constitute_authors(metarecord['$authors']) )

        group_flags = target.flags.intersection(self.groups)
        if group_flags:
            if len(group_flags) != 1:
                raise DriverError(target)
            group_flag, = group_flags
            if '$timetable' not in metarecord or \
                    group_flag not in metarecord['$timetable']:
                raise DriverError(target)
            yield self.substitute_groupnamedef(
                group_name=self.groups[group_flag]['name'] )
            first_date, first_period = self.extract_first_period(
                target, metarecord, group_flag )
            if first_date is not None:
                if first_period is not None:
                    date = self.substitute_period(
                        date=self.constitute_date(first_date),
                        period=first_period )
                else:
                    date = first_date

        yield from super().generate_header_metabody(
            target, metarecord, date=date )

        yield r'\endgroup'

    authorsdef_template = r'\def\jeolmauthors{$authors}'
    groupnamedef_template = r'\def\jeolmgroupname{$group_name}'
    period_template = r'$date, пара $period'

    @classmethod
    def constitute_authors(cls, authors, thin_space=r'\,'):
        if len(authors) > 2:
            def abbreviate(author):
                *names, last = author.split(' ')
                return thin_space.join([name[0] + '.' for name in names] + [last])
        else:
            def abbreviate(author):
                return author
        return ', '.join(abbreviate(author) for author in authors)

