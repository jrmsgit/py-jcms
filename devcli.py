#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from urllib.request import build_opener, HTTPCookieProcessor, Request
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.error import HTTPError


def _parseArgs (argv):
    parser = ArgumentParser (description = 'jcms - devel command line client')

    parser.add_argument ('-p', '--http', metavar = 'PORT', type = int,
            default = 8000, help = 'http port to bind to (default: 8000)')

    parser.add_argument ('-v', '--verbose', action = 'store_true',
            default = False, help = 'verbose mode')

    parser.add_argument ('-P', '--post', metavar = 'POST', action = 'append',
            default = None, help = 'post data (key:val)')

    parser.add_argument ('-L', '--nologin', action = 'store_true',
            default = False, help = 'disable login')

    parser.add_argument ('url', metavar = 'URL', type = str, nargs = '?',
            default = '/', help = 'url to connect to (default: /)')

    return parser.parse_args (argv)


def _doLogin (cli, baseURL):
    d = urlencode ({
        'username': 'superuser',
        'passwd': 'superuser',
    }).encode ('ascii')
    req = Request ('{}/login/'.format (baseURL), d)
    cli.open (req)


def _doRequest (opts):

    url = 'http://localhost:{}{}'.format (opts.http, opts.url)

    def getData ():
        p = None
        if opts.post is None:
            print ('GET', url)
        else:
            print ('POST', url)
            d = {}
            for o in opts.post:
                i = o.split (':')
                k = '{}'.format (i[0])
                v = i[1]
                d[k] = v
            p = urlencode (d).encode ('ascii')
            #~ print ('PARAMS:', p)
        return p

    cookies = CookieJar ()
    cli = build_opener (HTTPCookieProcessor (cookies))
    if not opts.nologin:
        _doLogin (cli, 'http://localhost:{}'.format (opts.http))

    req = Request (url, getData ())
    try:
        resp = cli.open (req)
    except HTTPError as err:
        resp = err

    print (resp.status, resp.reason)

    for hk, hv in resp.getheaders ():
        print (hk, ': ', hv, sep = '')

    if opts.verbose:
        print ()
        for c in cookies:
            print ('Cookie:', '{}={}'.format (c.name, c.value))

    # debug
    if opts.verbose or resp.status == 500:
        print ()
        for l in resp.read ().decode ().split ('\n'):
            print (l)

    resp.close ()


def _cmd ():
    _doRequest (_parseArgs (sys.argv[1:]))
    return 0


if __name__ == '__main__':
    sys.exit (_cmd ())
