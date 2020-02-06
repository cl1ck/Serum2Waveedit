#!/usr/bin/env sh

set -eu

pipenv lock --requirements > requirements.txt
rm -rf dist/
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pyinstaller --log-level=debug -y Serum2Waveedit.py"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
cp -a serum dist/windows/Serum2Waveedit
mkdir -p dist/windows/Serum2Waveedit/converted
echo "Here you will find the converted wavetables" >> dist/windows/Serum2Waveedit/converted/readme.txt
