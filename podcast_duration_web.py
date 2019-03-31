from flask import (
    Flask, request, url_for, send_from_directory,
    flash, redirect,  render_template
)
import dutil
import re
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sdfkjhi*&^guKJGADS&^R@'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
STATUS_PATH = os.path.join(os.path.dirname(__file__), 'status.txt')
TMP_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')
PYTHON_PATH = '/usr/bin/python3'


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
    status = None
    if os.path.exists(STATUS_PATH):
        with open(STATUS_PATH, 'rb') as f:
            status = f.read().decode('utf-8')
    result_path = os.path.join(os.path.dirname(__file__), 'static', 'result.json')
    result_date = None
    if os.path.exists(result_path):
        stat = os.stat(result_path)
        result_date = datetime.fromtimestamp(int(stat.st_mtime)).strftime('%Y-%m-%d %H:%M')
    return render_template('index.html', urls=urls, dur=duration_string,
                           status=status, result_date=result_date)


@app.route('/upload', methods=['POST'])
def upload():
    if os.path.exists(STATUS_PATH):
        flash('Файл уже обрабатывается, подождите или напишите Илье')
    elif 'file' not in request.files:
        flash('Файл куда-то пропал')
    else:
        flash('Подождите минуту, запускаем скрипт..')
        request.files['file'].save(TMP_DATA_PATH)
    return redirect(url_for('front'))
