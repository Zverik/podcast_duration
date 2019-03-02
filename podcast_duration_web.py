from flask import Flask, request, url_for
import dutil
import re
import json

app = Flask(__name__)


def find_duration(s):
    s = s.strip()
    podcast = {}
    if re.match(r'^[.,\d\s]+$', s):
        byhand = dutil.parse_text('byhand', s)
        if not byhand:
            return ''
        lengths = {'byhand': byhand}
    else:
        for m in re.findall(r'"([a-z]+)":\s*"(http[^"]+)"', s):
            podcast[m[0]] = m[1]
        lengths = dutil.get_durations(podcast)
    data = dutil.gen_additional_fields(lengths)
    if not data:
        return ''
    return json.dumps(data, indent=2, ensure_ascii=False)


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
</head>
<body>
  <h2>Получаем длительности треков в подкасте</h2>
  <form action="{action}" method="POST">
  <div>Скопируйте сюда кусок json или введите минуты через запятую:</div>
  <textarea name="urls" style="width: 90%; height: 15em;">{urls}</textarea><br>
  <input type="submit" value="Отправить">
  <a href="{action}">Очистить</a>
  </form>
  <pre style="margin-top: 3em; font-size: 20px;">{dur}</pre>
</body>
</html>
'''.format(action=url_for('front'), urls=urls, dur=duration_string)
