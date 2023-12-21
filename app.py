from flask import Flask, render_template

app = Flask(__name__)

projects_data = [
    
        {   'html': 'store.html',
            'title': 'Online Store',
            'description': 'When I first started learning SQL, I set up a simple DB for online outdoor clothes store. I\'ve now design and integrated a front end for it.',
            'image': 'static/project1.jpg'
        },
        {   
            'html': 'game.html',
            'title': 'Project 2',
            'description': 'Description of Project 2.',
            'image': 'static/project2.jpg'
        }

]

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

@app.route('/project/<string:html_file>')
def project_detail(html_file):
    return render_template(html_file)

if __name__ == '__main__':
    app.run(debug=True)
