from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Response as resp, Blueprint
import json
import os.path
import random
from werkzeug.utils import secure_filename

if os.path.exists('secretkey.json'):
    with open('secretkey.json') as key_file:
        keys = json.load(key_file)


bp = Blueprint('urlshort', __name__, static_folder="static", static_url_path="./static")

# Serves the Home Page


@bp.route('/')
def home():
    session.keys()
    return render_template('home.html', codes=session.keys())

# On submission of the URL Shortenor form,
# it proceses the request and take the user to a page that confirms the shortened url


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    # If a proper form submission is made and that POST request is made, we process the request
    if request.method == 'POST':
        # creation of a python dictionary that will be edited and injected into the json
        urls = {}

        # if the urls.json file exists, we load the json
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # if a user uses a shortened name that already exists,
        # then we redirect them to the home page and provide an error message
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))
        # if the submission is a url, then save the url to the shortened keyword
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        # if the submission is not a url, but a file, then we process it as a file
        else:
            # we get the file from the html
            f = request.files['file']
            # We need the file path to be unique
            # We know that every 'code' or shortened keyword, has to be unique
            # So to solve this problem, we add the code name to the
            # file name, which makes the file name unique
            # "secure_filname" adds security and prevents a user from injecting malicious data
            full_name = request.form['code'] + secure_filename(f.filename)
            # Saves the file that is uploaded
            f.save(
                '/Users/ahmadsandid/documents/00coding/python/flask/url-shortener/urlshort/static/user_files/' + full_name)
            # Much like a link, it saves the path for the new file that was downloaded
            # and assigns it to the shortened code name in the json
            urls[request.form['code']] = {'file': full_name}

        # On open of the json file, we will dump the python dictionary that was just edited into the json file.
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True

        # After the process is done, the user will be sent to a 'your_url' page
        return render_template('your_url.html', code=request.form['code'])
    # We don't want the user to access confirmation page directly
    # So, if a user tries to access the page directly or try to make a get request
    # they will be redirected to the home page.
    else:
        return redirect(url_for('urlshort.home'))


def getURL(code1):
    # If urls.json exists in file structure
    if os.path.exists('urls.json'):
        # If we can open urls.json, we import it as 'urls_file'
        with open('urls.json') as urls_file:
            # We import the json file as a python dictionary, 'urls'
            urls = json.load(urls_file)
            # if the string input, 'code', is found within the json
            if code1 in urls.keys():
                # if the codename is associated with a url
                if 'url' in urls[code1].keys():
                    # redirect them to the url
                    return str(urls[code1]['url'])
                # if it is a file, we serve a static file
                else:
                    return str(url_for('static', filename='user_files/' +
                                       urls[code1]['file']))

    return abort(404)


@bp.route('/<string:code>')
def redirect_to_url(code):
    # If urls.json exists in file structure
    if os.path.exists('urls.json'):
        # If we can open urls.json, we import it as 'urls_file'
        with open('urls.json') as urls_file:
            # We import the json file as a python dictionary, 'urls'
            urls = json.load(urls_file)
            # if the string input, 'code', is found within the json
            if code in urls.keys():
                # if the codename is associated with a url
                if 'url' in urls[code].keys():
                    # redirect them to the url
                    return redirect(urls[code]['url'])
                    # for testing
                    # return redirect('https://www.youtube.com')
                # if it is a file, we serve a static file
                else:
                    return redirect(url_for('static', filename='user_files/' +
                                            urls[code]['file']))

    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))