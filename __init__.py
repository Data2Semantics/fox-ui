import os
import subprocess
import zlib
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
FOX_TASK_DIR = os.environ.get('FOX_TASK_DIR', './tasks')


@app.route('/')
def landing():
    return render_template(
        'landing.html',
        post_endpoint=url_for('endpoint'))


@app.route('/psl', methods=['GET', 'POST'])
def endpoint():
    if request.method == 'GET':
        return render_template(
            'endpoint.html',
            post_endpoint=url_for('endpoint'))

    data = request.form.get('data', None)
    if not data:
        return "Pass PSL input in 'data' query parameter."

    input_file, task_id = create_task(data)
    output_file = os.path.join(os.path.dirname(input_file), 'output.txt')
    if not os.path.isfile(output_file):
        app.logger.info("Schedulling task {} for execution.".format(task_id))
        run_task(input_file)
    else:
        app.logger.info(
            "Found output for task {}, not running.".format(task_id))
    return redirect('/task/{}/output.txt'.format(task_id))


@app.route('/task/<path:filename>')
def download_file(filename):
    return send_from_directory(FOX_TASK_DIR,
                               filename, mimetype='text/plain')


def fingerprint(data):
    return str(zlib.adler32(data.encode('utf-8')) & 0xffffffff)


def create_task(data):
    task_id = fingerprint(data)
    app.logger.info("Creating task {}.".format(task_id))
    task_dir = os.path.join(FOX_TASK_DIR, task_id)
    task_file = os.path.join(task_dir, 'source.psl')
    if not os.path.isdir(task_dir):
        os.mkdir(task_dir)
    if not os.path.isfile(task_file):
        with open(task_file, 'w') as fout:
            fout.write(data)
    return task_file, task_id


def run_task(file_name):
    task_dir = os.path.dirname(file_name)
    output = open(os.path.join(task_dir, 'output.txt'), 'w')
    error = open(os.path.join(task_dir, 'error.txt'), 'w')
    subprocess.Popen(
        [
            './fox.sh', file_name
        ],
        stdout=output,
        stderr=error)


if __name__ == '__main__':
    app.secret_key = 'development'
    app.debug = True
    app.run()
