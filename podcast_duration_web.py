from flask import Flask, request, url_for
import dutil
import re

app = Flask(__name__)


def find_duration(s):
    s = s.strip()
    if re.match(r'^[.,\d\s]+$', s):
        byhand = dutil.parse_text('byhand', s)
        if not byhand:
            return ''
        if 'duration' in byhand:
            med = dutil.find_medians(byhand['duration'])
            return dutil.format_medians(*med)
        elif 'date' in byhand:
            return 'dates not supported yet'
    podcast = {}
    for m in re.findall(r'"([a-z]+)":\s*"(http[^"]+)"', s):
        podcast[m[0]] = m[1]
    lengths = dutil.get_durations(podcast)
    mins = dutil.find_longest_mins(lengths)
    if not mins:
        return ''
    med = dutil.find_medians(mins)
    return dutil.format_medians(*med)


@app.route('/', methods=['GET', 'POST'])
def front():
    duration_string = ''
    urls = request.form.get('urls', '')
    if request.method == 'POST':
        duration_string = find_duration(urls)
        if duration_string:
            duration_string = '"duration": "{}"'.format(duration_string)
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
  <div style="margin-top: 3em;">{dur}</div>
</body>
</html>
'''.format(action=url_for('front'), urls=urls, dur=duration_string)
