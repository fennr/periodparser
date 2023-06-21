![PyPI - Python Version](https://img.shields.io/pypi/pyversions/periodparser)
![PyPI - Python Version](https://img.shields.io/pypi/v/periodparser)
![Black badge](https://img.shields.io/badge/code%20style-black-000000.svg)


[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=git@github.com:fennr/periodparser)

# periodparser

python parser for human-readable period dates

## Установка

`pip install periodparser`

## Описание

Библиотека для парсинга дат и времени в естественной речи на русском языке.

## Пример

```python
import periodparser as pp

result = pp.extract('Техобслуживание пройдет с вечера следующей среды до пол 9 утра')
print(result.dates[
          0])  # [Type=DateTimeTokenType.PERIOD, From=2023-06-28T17:00:00, To=2023-06-29T08:30:00, Span=None, HasTime=True, StartIndex=24, EndIndex=62]
```