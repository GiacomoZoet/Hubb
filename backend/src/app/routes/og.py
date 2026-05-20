from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from html.parser import HTMLParser
import requests as http

og_bp = Blueprint('og', __name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; bot/1.0)'
}


class OGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.og = {'title': '', 'description': '', 'image': '', 'url': ''}

    def handle_starttag(self, tag, attrs):
        if tag != 'meta':
            return
        attrs = dict(attrs)
        prop = attrs.get('property', '') or attrs.get('name', '')
        content = attrs.get('content', '')
        if prop == 'og:title':
            self.og['title'] = content
        elif prop == 'og:description':
            self.og['description'] = content
        elif prop == 'og:image':
            self.og['image'] = content
        elif prop == 'og:url':
            self.og['url'] = content


@og_bp.route('', methods=['GET'])
@jwt_required()
def get_og():
    url = request.args.get('url', '').strip()
    if not url.startswith(('http://', 'https://')):
        return jsonify({}), 200

    try:
        resp = http.get(url, headers=HEADERS, timeout=5, allow_redirects=True)
        if not resp.ok:
            return jsonify({}), 200
        parser = OGParser()
        parser.feed(resp.text[:50000])
        if not parser.og['url']:
            parser.og['url'] = url
        return jsonify(parser.og), 200
    except Exception:
        return jsonify({}), 200
