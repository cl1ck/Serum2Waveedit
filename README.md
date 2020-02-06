# Serum2Waveedit

## Develop

```
$ pip install pipenv
$ pipenv install --dev
$ pipenv shell
(pipenv) $ python Serum2Waveedit.py 
```

## Build

```
$ pip install pipenv
$ pipenv install --ignore-pipfile
$ pipenv run pyinstaller --onefile Serum2Waveedit.spec
```