import re

import ckan.plugins.toolkit as toolkit

ENDS_WITH_NUMBER = re.compile(".*[0-9]$")


class RemoveDuplicatesCommand(toolkit.CkanCommand):
    ''' Removes the older of any duplicates - tactical, please make better'''
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

            for name in names:
                matches = sorted([n for n in names if n.startswith(name) and len(n) - len(name) == 1])
                if not matches:
                    continue

                matches.insert(0, name)
                titles = set([packages[n] for n in matches])
                if len(titles) > 1:
                    print "Mismatched titles"
                    continue

                # All but the latest
                for pkg in matches[0:-1]:
                    print "  Deleting {}".format(pkg)
                    toolkit.get_action('package_delete')(
                        self.get_context(), {'id': pkg}
                    )