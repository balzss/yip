import requests
import pip
import textwrap
import signal
import sys
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib


# when user exits with Ctrl-C, don't show error msg
signal.signal(signal.SIGINT, lambda x,y: sys.exit())

size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

colors = {'red': '\033[0;31m',
        'green': '\033[0;32m',
        'yellow': '\033[0;33m',
        'blue': '\033[1;34m',
        'purple': '\033[1;35m',
        'cyan': '\033[1;36m',
        'grey': '\033[0;37m',
        'endc': '\033[0m'}


def color(color, string):
    return colors.get(color) + string + colors.get('endc')


def wrap(t):
    return textwrap.fill(t, initial_indent='  ', subsequent_indent='  ',
            width=80, replace_whitespace=False)

def human_size(b):
    i = 0
    while b >= 1024:
        b /= 1024.
        i += 1
    # will give index error with packages bigger than 1025 PetaByte
    return '%.2f %s' % (b, size_suffixes[i])


def get_info(name, query):
    url = 'https://pypi.python.org/pypi/%s/json' % name
    data = requests.get(url).json()
    ver = data['info']['version']
    ver_info = data['releases'][ver][0] if data['releases'][ver] else ''

    return_info = {}

    if 'date' in query:
        return_info['date'] = 'Uploaded on: '
        return_info['date'] += ver_info['upload_time'].split('T')[0] \
                if ver_info else 'UNKNOWN'

    if 'size' in query:
        return_info['size'] = 'Size: '
        return_info['size'] += human_size(ver_info['size']) \
                if ver_info else 'UNKNOWN'

    if 'license' in query:
        return_info['license'] = 'License: '
        return_info['license'] += data['info']['license'].split('\n')[0]

    if 'home_page' in query:
        return_info['home_page'] = 'Home Page: '
        return_info['home_page'] += data['info']['home_page']

    return return_info

def get_installed():
    return {i.key: i.version for i in pip.get_installed_distributions()}

def search_packages(q, i):
    unordered_results = client.search({'name': q, 'summary': q}, 'or')
    ranked_results = []
    for r in unordered_results:
        score = 0
        if r['name'].lower() == ' '.join(q).lower():
            score = 1000
        for s in q:
            score += r['name'].lower().count(s.lower()) * 3
            score += r['summary'].lower().count(s.lower()) * 1 \
                    if r['summary'] else 0

        ranked_results.append({'name': r['name'], 'version': r['version'],
                'summary': r['summary'], 'score': score})
        if len(ranked_results) >= i:
            break
    return sorted(ranked_results, key=lambda k: k['score'])

def set_opts(argv):
    if len(argv) > 1:
        q = []
        for a in argv[1:]:
            if a[0] == '-':
                break
            print(a)
            q.append(a)
    else:
        q = input(color('yellow', 'Enter search term: '))
    argv += ['-', '-']
    opts = {}
    opts['date'] = True if '-date' in argv[2:] else False
    opts['size'] = True if '-size' in argv[2:] else False
    opts['license'] = True if '-license' in argv[2:] else False
    opts['home_page'] = True if '-homepage' in argv[2:] else False
    limit = int(argv[argv.index('-limit') + 1]) if '-limit' in argv[2:] \
            and argv.index('-limit') != (len(argv)) and \
            argv[argv.index('-limit') + 1].isdigit() else 100

    return q, opts, limit

def create_list(ordered_res, opts):
    formatted_list = []
    for i, r in enumerate(ordered_res):

        name = r['name']
        version = r['version']
        description = r['summary']
        description = '---' if not description else description
        f_installed = ''

        if name in installed:
            f_installed = ' INSTALLED: '
            if installed[name] == version:
                f_installed += '(latest)'
            else:
                f_installed += '(%s)' % installed[name]
            f_installed = color('purple', f_installed)

        extra_info = {}
        f_extra = ''
        info_query = [key for key, value in opts.items() if value is True]
        if info_query:
            extra_info = get_info(name, info_query)
            f_extra = ' | '.join([value for key, value in extra_info.items()
                    if key != 'home_page'])
            f_extra = color('grey', f_extra)

        f_name = color('blue', '[%d]%s (%s)' % (i, name, version))

        info_dict = {'name': f_name, 'installed': f_installed,
                'extra': f_extra, 'summary': description}
        if 'home_page' in extra_info:
            info_dict['home_page'] = extra_info['home_page']
        formatted_list.append(info_dict)

    return formatted_list

def print_list(formatted_list):
    for r in formatted_list:
        name = r['name']
        installed = r['installed']
        extra = r['extra']
        print('%s%s %s' % (name, installed, extra))
        if 'home_page' in r:
            print(color('yellow', wrap(r['home_page'])))
        print('%s\n' % wrap(r['summary']))


def get_choise():
    print(color('yellow', '=====Enter package number for options====='))
    p_choise = input(color('yellow', '>>> '))

    if not p_choise.isdigit() or 0 > int(p_choise) >= len(ordered_packages):
        sys.exit()
    else:
        p_choise = ordered_packages[int(p_choise)]

    if p_choise['name'] in installed:
        install_option = '[r]emove'
        p_status = 'INSTALLED (latest)'

        if installed[p_choise['name']] != p_choise['version']:
            install_option += '\n  [u]pdate to (%s)' % p_choise['version']
            p_status = 'INSTALLED (%s)' % installed[p_choise['name']]

    else:
        install_option = '[i]nstall'
        p_status = 'Not installed'

    parsed_info = get_info(p_choise['name'],
            ['home_page', 'date', 'license', 'size'])

    p_info = '%s\n%s\n%s\n%s' % (parsed_info['date'], parsed_info['license'],
            parsed_info['size'], parsed_info['home_page'])

    print(color('blue', '\nName: %s' % p_choise['name']))
    print(color('purple', 'Version: %s\nStatus: %s'
            % (p_choise['version'], p_status)))
    print(color('grey', p_info))

    print(color('yellow', '\nOptions:'))
    print(wrap('[b]ack to search results'))
    print(wrap('[o]pen in browser'))
    print(wrap(install_option))

    o_choise = input(color('yellow', '\n>>> '))
    print(o_choise)


if __name__ == "__main__":
    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')

    installed = get_installed()
    q, opts, limit = set_opts(sys.argv)
    ordered_packages = search_packages(q, limit)
    formatted_packages = create_list(ordered_packages, opts)
    print_list(formatted_packages)
    get_choise()
