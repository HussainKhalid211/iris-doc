# iris_doc
A tool that add the API tag above the APIs base on the formatted code.

## Get Started
```
python3 -m pip install -r requirements.txt

python3 iris_doc.py \
        --config=fmt_config/fmt_dart.yaml \
        --language=dart --template=/Users/json/path/template_en.json \
        --export-file-path=/Users/exportfile/path/export_file.dart
```