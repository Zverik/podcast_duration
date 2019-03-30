from flask import (
    Flask, request, url_for, send_from_directory,
    flash, redirect, jsonify, render_template
)
import dutil
import re
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def find_duration(s):
    s = s.strip()
    podcast = {}
    if re.match(r'^[.,\d\s]+$', s):
        byhand = dutil.parse_text('byhand', s)
        if not byhand:
            flash('Ожидаю числа через запятую: min,min,min или yymmdd,yymmdd')
            return ''
        lengths = {'byhand': byhand}
    else:
        for m in re.findall(r'"([a-z]+)":\s*"(http[^"]+)"', s):
            podcast[m[0]] = m[1]
        lengths = dutil.get_durations(podcast)
    data = dutil.gen_additional_fields(lengths)
    if not data:
        flash('Формат понятен, но выводов нет')
        return ''
    return json.dumps(data, indent=2, ensure_ascii=False)


@app.route('/pdur.css')
def serve_css():
    return send_from_directory('css', 'pdur.css')


@app.route('/', methods=['GET', 'POST'])
def front():
    duration_string = ''
    urls = request.form.get('urls', '')
    if urls and request.method == 'POST':
        duration_string = find_duration(urls)
    return render_template('index.html', urls=urls, dur=duration_string)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Файл куда-то пропал')
        return redirect(url_for('front'))
    try:
        data = json.load(request.files['file'])
    except Exception as e:
        flash('Ошибка при чтении файла: {}'.format(e))
        return redirect(url_for('front'))
    for p in data:
        if 'title' in p:
            lengths = dutil.get_durations(p)
            p.update(dutil.gen_additional_fields(lengths))
    return jsonify(data)
