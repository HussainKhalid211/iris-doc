# iris_doc
A CLI tool that fill the dita json data as comments to code from https://github.com/AgoraIO/agora_doc_source.

## Get Started
### dart
```
python3 -m pip install -r requirements.txt

python3 iris_doc.py \
        --config=fmt_config/fmt_dart.yaml \
        --language=dart \
        --template-url=https://github.com/AgoraIO/agora_doc_source/releases/download/main/flutter_ng_json_template_cn.json \
        --export-file-path=/Users/exportfile/path/export_file.dart
```

### ts
First install the eslint
```
npm install eslint
```

```
python3 -m pip install -r requirements.txt

python3 iris_doc.py \
        --config=fmt_config/fmt_ts.yaml \
        --language=ts \
        --template-url=https://github.com/AgoraIO/agora_doc_source/releases/download/main/rn_ng_json_template_en.json \
        --export-file-path=/Users/exportfile/path/export_file.ts
```

## License
The project is under the MIT license.