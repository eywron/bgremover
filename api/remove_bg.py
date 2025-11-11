import io
import os
import zipfile
from flask import Flask, request, send_file, jsonify
from rembg import remove

app = Flask(__name__)
# Enforce a file size limit (10 MB) to protect execution time & memory
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXT = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route('/', methods=["POST"])
def handler():
    """Accepts multipart/form-data with field name `file` (single) or multiple files
    named `file` (HTML input `multiple`) or `files`.

    Returns:
      - single PNG image (image/png) when one file uploaded
      - ZIP archive (application/zip) when multiple files uploaded
    """
    files = []
    if 'file' in request.files:
        files = request.files.getlist('file')
    elif 'files' in request.files:
        files = request.files.getlist('files')
    else:
        return jsonify({"error": "No file part in the request. Use form field name 'file' or 'files'."}), 400

    if not files:
        return jsonify({"error": "No files uploaded."}), 400

    processed = []

    try:
        for f in files:
            filename = f.filename or 'uploaded'
            if filename == '':
                continue
            if not allowed_file(filename):
                return jsonify({"error": f"File type not allowed: {filename}"}), 400

            data = f.read()
            if not data:
                return jsonify({"error": f"Empty file: {filename}"}), 400

            try:
                result_bytes = remove(data)
            except Exception as ex:
                return jsonify({"error": "Background removal failed.", "details": str(ex)}), 500

            out_name = os.path.splitext(filename)[0] + '.png'
            processed.append((out_name, result_bytes))

        if len(processed) == 1:
            name, img_bytes = processed[0]
            return send_file(io.BytesIO(img_bytes), mimetype='image/png', as_attachment=False, download_name=name)

        mem = io.BytesIO()
        with zipfile.ZipFile(mem, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, b in processed:
                z.writestr(name, b)
        mem.seek(0)
        return send_file(mem, mimetype='application/zip', as_attachment=True, download_name='removed_backgrounds.zip')

    except Exception as e:
        return jsonify({"error": "Internal server error during processing.", "details": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
