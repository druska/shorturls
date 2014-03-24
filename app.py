from urlparse import urlparse

from lib.numbers import base36encode
from models import db, Url

from flask import Flask, Response, json, request, redirect
app = Flask(__name__)

# db.create_all()

@app.route("/create", methods=["GET", "POST"])
def create():
    """Create a short URL and return a JSON response."""
    full_url = request.args.get('url')

    if not full_url:
        return Response(json.dumps({'success': False,
                                    'message': 'No "url" parameter specified'}),
                        mimetype='application/json')

    # Validate full_url
    parsed_url = urlparse(full_url)
    if parsed_url.scheme == '':
        return Response(json.dumps({'success': False,
                                    'message': 'No URL scheme specified'}),
                        mimetype='application/json')

    # Insert URL into db and generate a short url
    short_url = Url(full_url)
    db.session.add(short_url)
    db.session.commit()  # Get autoincrement id
    short_url.short_url = base36encode(short_url.id)
    db.session.commit()

    # Get host to display short url (this won't work with https)
    host = 'http://' + request.headers.get('Host', 'localhost')

    return Response(json.dumps({'success': True,
                                'url': full_url,
                                'short_url': '%s/%s' % (host, short_url.short_url)}),
                        mimetype='application/json')


@app.route("/<short_url>", methods=["GET"])
def short_url(short_url):
    """Either redirects to a short URL's URL or to / if the short URL
    doesn't exist."""
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.url, 301)
    else:
        return redirect('/', 302)


@app.route("/", methods=["GET"])
def home():
    return "Example: /create?url=http://google.com"

if __name__ == "__main__":
    app.run(debug=True)
