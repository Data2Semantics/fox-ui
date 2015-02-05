from subprocess import check_output, CalledProcessError
from flask import Flask, render_template, request, Response

app = Flask(__name__)
fname = 'temp.psl'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app.logger.debug("Got POST")
        app.logger.debug(request.form)
        data = request.form.get('data', None)
        if data:
            app.logger.debug(data)
            fout = open(fname, 'w')
            fout.write(data)
            fout.close()
            return Response(execute(), content_type="text/plain;charset=UTF-8")
        else:
            return "no data\n"
    else:
        return render_template('index.html')


def execute():
    return check_output(
        ['java',
         '-Xmx5000m',
         '-cp',
         './fox-assembly-1.0-SNAPSHOT.jar',
         'com.signalcollect.psl.CommandLinePslInferencer',
         '--filename',
         fname], 
        shell=False)

if __name__ == '__main__':
    app.secret_key = 'development'
    app.debug = True
    app.run()


# def index():
#     if request.method == 'POST':
#         app.logger.debug("Got POST")
#         in_file = request.files['file']
#         in_file.save(fname)
#         return execute()
#     else:
#         return render_template('index.html')
