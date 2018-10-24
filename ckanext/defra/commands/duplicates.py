import re

import ckan.plugins.toolkit as toolkit

ENDS_WITH_NUMBER = re.compile(".*[0-9]$")


class RemoveDuplicatesCommand(toolkit.CkanCommand):
    ''' Removes the older of any duplicates '''
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0

    def get_context(self):
        return {
            'ignore_auth': True,
        }

    def command(self):
        self._load_config()

        publishers = toolkit.get_action('organization_list')(
            self.get_context(), {'all_fields': True, 'include_datasets': True}
        )

        for publisher in publishers:
            print "---- {}".format(publisher['title'])

            packages = {}
            for p in publisher['packages']:
                packages[p['name']] = p['title']

            names = packages.keys()[:]

            poss_matches = sorted([
                n for n in names if ENDS_WITH_NUMBER.match(n) and n[0:-1] in names
            ])

            if not poss_matches:
                continue

            todel = []

            if len(poss_matches) > 1:
                todel.extend(poss_matches[:-1])

            todel.append(poss_matches[0][0:-1])

            # Make sure all datasets in todel have the same title ...
            todel.sort()
            titles = [packages[n] for n in todel]
            if len(set(titles)) > 1:
                print "Bailing, titles not the same"
                continue

            for name in todel:
                print " -------> Deleting {}".format(name)

                #toolkit.get_action('package_delete')(
                #    self.get_context(), {'id': name}
                #)

