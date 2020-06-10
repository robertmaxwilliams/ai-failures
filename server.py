from bottle import get, post, request, static_file, run

# local helper file
from data import *

def common_member(a, b): 
    return set(a) & set(b)

def html_body_wrap(body):
    head = '''<head><style type="text/css">body{margin:40px
        auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0
        10px}h1,h2,h3{line-height:1.2}form{line-height:1}</style></head>'''
    return "<!DOCTYPE html><html>" + head + "<body>\n" + body + "</body></html>"

def num_to_link_safe(n):
    html = ""
    if n in num_to_link:
        return f'<a href="{num_to_link[n]}">link</a>'
    else:
        return ''

def link_nums_to_html(link_nums):
    return "".join([" " + num_to_link_safe(n) for n in link_nums])


tags_and_names = [(agency_tags, "agency"), 
        (preventability_tags, "preventability"),
        (lifecycle_tags, "lifecycle"),
        (consequence_tags, "consequence")]
def generate_main_page():
    html = "<h1>Perform a query</h1>"
    html += '<p>Check boxes to include incidents with those tags in your results then scroll to the bottom and hit "Submit".<p>'
    html += '<form action="/query" method="post">'
    for some_tags, name in tags_and_names:
        html += f"<p>Select {name} levels:</p>\n"
        for tag, description in some_tags:
            html += f'<input type="checkbox" id="male" name="{name}" value="{tag}">\n'
            html += f'<label for="{tag}">{description} ({tag})</label><br>\n'
        html += '<br>\n'
    html += '<input value="Submit" type="submit" />'
    return html

@get('/')
def login():
    return html_body_wrap(generate_main_page())

@get('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='.')

@post('/query')
def query():
    user_tags = []
    for base_tags, name in tags_and_names:
        new_tags = request.forms.getall(name) 
        if new_tags == []:
            new_tags = [x for x, _ in base_tags]
        user_tags.append(new_tags)
    html = '<input type="button" value="Search Again" onclick="history.back()"/><br>'
    html += "<h1>results:</h1>"
    found_anything = False
    print(user_tags)
    for (text, link_nums, tags) in failures:
        if all([common_member(user_tag_group, tags) for user_tag_group in user_tags]):
            found_anything = True
            html += f'<p>{text} <b>{tags}</b>{link_nums_to_html(link_nums)}</p>'

    if not found_anything:
        html += f'<p>No results!</p>'
    return html_body_wrap(html)

run(host='localhost', port=8080, debug=True)
