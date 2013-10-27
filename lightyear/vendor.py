import urllib.request
import urllib.error
import urllib.parse
import socket
import json
import os.path

from .ly_types import CSSRule
from .errors import LyError


QUERY_TIMEOUT = 2
VENDOR_JSON_FILE = 'vendor-data.json'
VENDOR_JSON_URL = 'https://raw.github.com/Fyrd/caniuse/master/data.json'
DEFAULT_TARGETS = 'ie=10;firefox=20;chrome=26;safari=5'

VENDOR_PREFIXES = {
    'ie': '-ms-',
    'firefox': '-moz-',
    'chrome': '-webkit-',
    'safari': '-webkit-',
    'opera': '-o-'
}

CORRECTIONS = {
    'backface-visibility': 'transforms2d',
    'perspective': 'transforms2d',
    'perspective-origin': 'transforms2d',
    'transform': 'transforms2d',
    'transform-origin': 'transforms2d',
    'transform-style': 'transforms2d',
    'animation': 'css-animation',
    'animation-delay': 'css-animation',
    'animation-direction': 'css-animation',
    'animation-duration': 'css-animation',
    'animation-fill-mode': 'css-animation',
    'animation-iteration-count': 'css-animation',
    'animation-name': 'css-animation',
    'animation-play-state': 'css-animation',
    'animation-timing-function': 'css-animation',
    'align-content': 'flexbox',
    'align-items': 'flexbox',
    'align-self': 'flexbox',
    'flex': 'flexbox',
    'flex-basis': 'flexbox',
    'flex-direction': 'flexbox',
    'flex-flow': 'flexbox',
    'flex-grow': 'flexbox',
    'flex-shrink': 'flexbox',
    'flex-wrap': 'flexbox',
    'justify-content': 'flexbox',
    'order': 'flexbox',
    'font-kerning': 'font-feature',
    'font-synthesis': 'font-feature',
    'font-variant-alternates': 'font-feature',
    'font-variant-caps': 'font-feature',
    'font-variant-east-asian': 'font-feature',
    'font-variant-ligatures': 'font-feature',
    'font-variant-numeric': 'font-feature',
    'font-variant-position': 'font-feature',
    'transition': 'css-transitions',
    'transition-delay': 'css-transitions',
    'transition-duration': 'css-transitions',
    'transition-property': 'css-transitions',
    'transition-timing-function': 'css-transitions'
}


### PREFIXR.COM METHOD ###

def vendorize_css(css):
    print('yoyoyoyo!!!!')
    return _prefixr(css)


def _prefixr(css):
    try:
        post_data = urllib.parse.urlencode({'css': css}).encode('utf-8')
        request = urllib.request.Request(
            'http://prefixr.com/api/index.php',
            post_data,
            headers={"User-Agent": "LightYear CSS"})
        httpf = urllib.request.urlopen(request, timeout=QUERY_TIMEOUT)

        if not "utf-8" in httpf.getheader('Content-Type').lower():
            raise LyError('Prefixr.com API returned invalid data.')
        text = httpf.read().decode(encoding='UTF-8')

        return text.replace('\n', '').replace('\t', '')

    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        raise LyError('Could not connect to Prefixr.com API.\nMessage: ' + str(e))
    except urllib.error.ContentTooShortError as e:
        raise LyError('The data retrieved via the Prefixr.com API was of an unexpected length.')
    except socket.timeout:
        raise LyError('The connection to Prefixr.com timed out.\nMessage: ' + str(e))


### CANIUSE.COM METHOD ###

def vendorize_tree(ltree, offline=True, targets=None):
    '''
    Iterates over the ltree and inserts vendor prefixed declarations as needed.
    Valid options for method are:

       'offline' - use local data in VENDOR_JSON_FILE
       'online' - download fresh data from VENDOR_JSON_URL

        offline, or online.
    '''
    targets = targets or DEFAULT_TARGETS
    prefixer = CanIUsePrefixes(targets=targets, offline=offline)
    vendorize_block(ltree, prefixer)


def vendorize_block(block, prefixer):
    # Examine nodes in reverse, to avoid seeing same node multiple times
    for i, node in reversed(list(enumerate(block))):
        # Recursively process child blocks.
        if hasattr(node, 'block'):
            vendorize_block(node.block, prefixer)

        # Insert vendorized properties
        if hasattr(node, 'prop'):
            for new_prop, browser, version in prefixer.vendorized_properties(node.prop):
                values = [prefixer.vendorize_value(value, browser, version)
                          for value in node.values]
                block.insert(
                    i,
                    CSSRule(
                        tag=node.tag,
                        prop=new_prop,
                        values=values,
                        index=node.index,
                        important=node.important)
                    )


class CanIUsePrefixes():
    def __init__(self, targets, offline):
        self.targets = [setting.split('=')
                        for setting in targets.split(';')]
        self.data = self.get_data(offline)

    def get_data(self, offline):
        return self._get_data_offline() if offline else self._get_data_online()

    def _get_data_offline(self):
        vendor_data_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            VENDOR_JSON_FILE)
        with open(vendor_data_path, 'r') as jsonf:
            j = json.loads(jsonf.read())

        return j

    def _get_data_online(self):
        try:
            request = urllib.request.Request(
                VENDOR_JSON_URL,
                headers={"User-Agent": "LightYear CSS"})
            httpf = urllib.request.urlopen(request, timeout=QUERY_TIMEOUT)
        except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError) as e:
            raise LyError('Error while downloading vendor data.\nMessage: ' + str(e))
        except socket.timeout:
            raise LyError('While downloading vendor data, the connection timed out.\nMessage: ' + str(e))

        if not "utf-8" in httpf.getheader('Content-Type').lower():
            raise LyError('Could not decode CanIUse data.')
        text = httpf.read().decode(encoding='UTF-8')

        j = json.loads(text)
        return j['data']

    def vendorized_properties(self, proprty):
        properties = set()
        for browser, version in self.targets:
            if self.requires_prefix(proprty, browser, version):
                new_property = VENDOR_PREFIXES[browser] + proprty
                if not new_property in properties:
                    properties.add(new_property)
                    yield (new_property, browser, version)

    def vendorize_value(self, value, browser, version):
        if isinstance(value, str):
            if self.requires_prefix(value, browser, version):
                return VENDOR_PREFIXES[browser] + value
        return value

    def requires_prefix(self, proprty, browser, version):
        if not proprty in CORRECTIONS:
            return False
        corrected = CORRECTIONS[proprty]
        try:
            status = self.data[corrected]['stats'][browser][version]
        except KeyError:
            return False
        if status == 'y x':
            return True
        return False
