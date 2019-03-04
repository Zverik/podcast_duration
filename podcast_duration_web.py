from flask import Flask, request, url_for, send_from_directory, flash, redirect, jsonify
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
    if request.method == 'POST':
        duration_string = find_duration(urls)
    return '''
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Получаем длительности подкастов</title>
  <link rel="stylesheet" href="pdur.css" type="text/css">
</head>
<body>
  <h2>Получаем длительности треков в подкасте</h2>
  <form action="{action}" method="POST">
    <div>Скопируйте сюда кусок json или введите минуты через запятую:</div>
    <textarea name="urls">{urls}</textarea><br>
    <input type="submit" value="Отправить">
    <a href="{action}">Очистить</a>
  </form>
  <pre>{dur}</pre>
  <form action="{upload}" method="POST" enctype="multipart/form-data">
    <div>Обновление целого файла:</div>
    <input type="file" name="file">
    <input type="submit" value="Отправить">
  </form>
</body>
</html>
'''.format(action=url_for('front'), upload=url_for('upload'),
           urls=urls, dur=duration_string)


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
