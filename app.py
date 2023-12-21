from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/projects')
def projects():
    projects_data = [
        {
            'id': 1,
            'title': 'Online Store',
            'description': 'When I first started learning SQL, I set up a simple DB for online outdoor clothes store. I\'ve now design and integrated a front end for it.',
            'image': 'static/project1.jpg'
        },
        {
            'id': 2,
            'title': 'Project 2',
            'description': 'Description of Project 2.',
            'image': 'static/project2.jpg'
        },
        
    ]
    return render_template('projects.html', projects=projects_data)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    return "Hello_world"




if __name__ == '__main__':
    app.run(debug=True)
