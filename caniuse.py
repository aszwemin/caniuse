"""
Request information about search query from caniuse.com
"""

import urllib2
import json
import sys

def get_caniuse_info(args):
    search = args[1]

    page = urllib2.urlopen('https://raw.githubusercontent.com/Fyrd/caniuse/master/fulldata-json/data-2.0.json')
    data = json.loads(page.read())

    order = [
        'ie', 'firefox', 'chrome', 'safari', 'opera', 'ios_saf', 'op_mini',
        'android', 'and_chr'
    ]
    browsers = {
        'ie': 'IE',
        'firefox': 'Firefox',
        'chrome': 'Chrome',
        'safari': 'Safari',
        'opera': 'Opera',
        'ios_saf': 'iOS Safari',
        'op_mini': 'Opera Mini',
        'android': 'Android Browser',
        'and_chr': 'Chrome for Android',
    }

    data = data['data']
    ret = ""
    for k, v in data.iteritems():
        if k.find(search) > -1 or search in v['description'].lower() or \
                search in v['title'].lower():
            ret += '-' * 30 + '\n'
            ret += 'Title:' + v['title'] + '\n'
            ret += 'Description:' + v['description'] + '\n'
            ret += '\nSupported browsers:\n'
            for el in order:
                ver_list = []
                for k1, v1 in v['stats'][el].iteritems():
                    if 'y' in v1:
                        ver_list.append(k1)
                ret += str(browsers[el]) + ' ' + ','.join(sorted(ver_list)) + '\n'
            ret += '\nLinks:\n'
            for l in v['links']:
                ret += l['title'] + ' ' + l['url'] + '\n'

    return ret

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'You need to supply a search term'
    else:
        res = get_caniuse_info(sys.argv)
        print res or 'No results for your query'
