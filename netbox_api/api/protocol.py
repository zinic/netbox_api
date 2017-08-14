import json

import requests
import requests.auth

JSON_DECODE_ERR_FMT = 'Unable to decode result for request. Content body:\n{}'


class NetboxTokenAuth(requests.auth.AuthBase):
    """
    Attaches Netbox-style HTTP Token Authentication to the given Request object.
    """

    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return all([
            self.token == getattr(other, 'token', None),
        ])

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = 'Token {}'.format(self.token)
        return r


class HTTPException(Exception):
    def __init__(self, msg, failures=None):
        self.msg = msg
        self.failures = failures


class NetboxResponse(object):
    def __init__(self, resp, content):
        self._response = resp
        self._content = content
        self._json = None

    def _parse_content(self):
        try:
            payload = json.loads(self._content)

            # Single entity requests don't have the result wrapper JSON so we
            # choose to emulate it - DRY
            if 'results' not in payload:
                return {
                    'count': 1,
                    'next': None,
                    'previous': None,
                    'results': [payload]
                }

            return payload

        except json.decoder.JSONDecodeError as jde:
            raise HTTPException(JSON_DECODE_ERR_FMT.format(self._content)) from jde

    def raise_on_status(self):
        if self.ok is False:
            raise HTTPException('Unexpected status code: {}\n{}'.format(
                self._response.status_code,
                self._content))

    def wrap_results(self, cls):
        return [cls(**v) for v in self.results]

    @property
    def json(self):
        if self._json is None:
            self._json = self._parse_content()

        return self._json

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def ok(self):
        return 200 <= self._response.status_code < 300

    @property
    def count(self):
        return self.json['count']

    @property
    def next_page(self):
        return self.json['next']

    @property
    def previous_page(self):
        return self.json['previous']

    @property
    def results(self):
        return self.json['results']


class RequestHandler(object):
    def __init__(self, host, port, token, scheme, verify=None):
        self._host = host
        self._port = port
        self._scheme = scheme
        self._auth = NetboxTokenAuth(token)
        self._verify_path = verify
        self._session_obj = None

    @property
    def _session(self):
        if self._session_obj is None:
            self._session_obj = requests.Session()

            # Common auth
            self._session_obj.auth = self._auth

            # Common headers
            self._session_obj.headers['Accept'] = 'application/json'

        return self._session_obj

    def format_url(self, path_fmt, *parts):
        # Strip leading slashes
        if path_fmt.startswith('/'):
            path_fmt = path_fmt[1:]

        # Strip trailing slashes
        if path_fmt.endswith('/'):
            path_fmt = path_fmt[:len(path_fmt) - 1]

        # Format the path
        path = path_fmt.format(*parts)

        return '{}://{}:{}/api/{}/'.format(
            self._scheme,
            self._host,
            self._port,
            path)

    def request(self, method, url, **kwargs):
        request_func = getattr(self._session, method)

        # Copy the kwargs dict to modify it
        request_kwargs = kwargs.copy()

        if self._verify_path is not None:
            request_kwargs['verify'] = self._verify_path

        # Make the request
        resp = request_func(
            url=url,
            **request_kwargs)

        try:
            # Wrap the request which should read the entire body
            return NetboxResponse(resp, resp.text)
        finally:
            # Eagerly close the response
            resp.close()

    def paginate(self, cls, method, url, **kwargs):
        resp = self.request(method, url=url, **kwargs)

        while True:
            # Raise on bad status
            resp.raise_on_status()

            # Yield the next page of results
            for r in resp.wrap_results(cls):
                yield r

            # Exit this loop if there isn't a next page
            if resp.next_page is None:
                break

            # Perform the next get
            resp = self.request('get', url=resp.next_page)
