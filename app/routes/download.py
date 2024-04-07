@app.route('/download')
def download_file():
    file_path = ''
    return send_file(file_path, as_attachment=True)