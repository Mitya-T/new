# app.py
# app.py at the same level myproject
from myproject import app, db  # imports app from __init__
from flask_bootstrap import Bootstrap
from pprint import pprint

from flask import render_template, redirect, request, url_for, flash, abort, session
from flask_login import login_user, login_required, logout_user, current_user
from myproject.models import User, Project
from myproject.forms import LoginForm, RegistrationForm, PhoneForm, ProjectForm
# from werkzeug.security import generate_password_hash, check_password_hash # already done in models.py!!!!


@app.route('/', methods = ['GET','POST'])
def home():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('You are not in the database, please register')
            # return render_template('cond.html')
            return redirect(url_for('register'))


        elif user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Logged in successfully!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)

        else:
            flash('Login is ok, password is WRONG - please check your password...')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/cond')
def cond():
    return render_template('cond.html')

@app.route('/cond2')
def cond2():
    return render_template('cond2.html')

@app.route('/cond3')
def cond3():
    return render_template('cond3.html')

@app.route('/cond4')
def cond4():
    return render_template('cond4.html')

@app.route('/cond5')
def cond5():
    return render_template('cond5.html')

@app.route('/privacy_notice')
def privacy_notice():
    return render_template('privacy_notice.html')

@app.route('/update_email')
def update_email():
    return render_template('update_email.html')

# Welcomes user after they have logged in
@app.route('/welcome')
@login_required    # to make sure that user must be logged in to see that view
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/create_project', methods = ['GET','POST'])
@login_required    # to make sure that user must be logged in to see that view
def create_project():

    form = ProjectForm()

    if form.validate_on_submit():

        print(current_user)
        project = Project(title = form.title.data,
                    text = form.text.data,
                    language = form.language.data,
                    protocol = form.protocol.data,
                    format = form.format.data,
                    user_id = current_user.id
                    )

        db.session.add(project)

        db.session.commit()
        flash('Project created')
        # project = Project(parameter=form.parameter.data,
        #             protocol=form.protocol.data,
        #             format=form.format.data
        #             )

        return redirect(url_for('welcome_user'))

    return render_template('create_project.html', form=form)

# READ / VIEW (PROJECT)
@app.route('/<int:project_id>') # IMPORTANT that is is an INT to be able to pass later inside the function
# we don't care if someone is logged in or not
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', title=project.title,
                            date=project.date, post=project)




# UPDATE

@app.route('/<int:project_id>/update', methods=['GET','POST'])
@login_required
def update(project_id):
    project = Project.query.get_or_404(project_id)

    # Shows that access is forbidden!
    if project.author != current_user:
        abort(403)

    form = ProjectForm()

    if form.validate_on_submit():
        project.title = form.title.data
        project.text = form.text.data
        project.language = form.language.data
        project.protocol = form.protocol.data
        project.format = form.format.data
        # No need to add anything - just COMMIT
        db.session.commit()

        flash('Project Updated')

        return redirect(url_for('project', project_id=project.id)) # because of ```def blog_post(blog_post_id):```

    elif request.method == 'GET':
        form.title.data = project.title
        form.text.data = project.text

    return render_template('create_project.html', title='Updating (from UPDATE render_template)', form=form)



# DELETE

@app.route('/<int:project_id>/delete', methods=['GET','POST'])
@login_required

def delete_project(project_id):

    project = Project.query.get_or_404(project_id)

    # Shows that access is forbidden!
    if project.author != current_user:
        abort(403)

    db.session.delete(project)
    db.session.commit()
    flash('Project Deleted')

    return redirect(url_for('welcome_user'))




# User's list of PROJECTS:
@app.route("/<first_name>")
@login_required    # to make sure that user must be logged in to see that view
def user_posts(first_name):

    #requesting a page
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(first_name=first_name).first_or_404()

    # filtering the blog posts by username
    projects = Project.query.filter_by(author=user).order_by(Project.date.desc()).paginate(page=page, per_page=5) # comes from backref='author' on models.py

    return render_template('user_projects.html', projects=projects, user = user)



@app.route('/test')
def test():
    test = Project.query.all()
    pprint(test)


    return render_template('test.html', test=test)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out")
    return redirect(url_for('home'))





@app.route('/login', methods = ['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('You are not in the database, please register')
            # return render_template('cond.html')
            return redirect(url_for('register'))


        elif user.check_password(form.password.data) and user is not None:

            login_user(user)
            session["user"] = user
            flash('Logged in successfully!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)

        else:
            flash('Login is ok, password is WRONG - please check your password...')
            return redirect(url_for('login'))



    return render_template('login.html', form=form)



@app.route('/register', methods = ['GET','POST'])
def register():

    form = RegistrationForm()
    phone_form = PhoneForm()


    if form.validate_on_submit():

        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    dob=form.dob.data.strftime('%Y-%m-%d'),
                    email=form.email.data,
                    password=form.password.data,
                    address=form.address.data,
                    city=form.city.data,
                    # phone=form.phone.data # old and working!
                    phone=phone_form.phone.data


                    )

        if user.mel(form.email.data) and user.chk_pass(form.password.data):

            db.session.add(user)
            db.session.commit()
            flash("Thanks for registration!")

            return redirect(url_for('login'))
    return render_template('register.html', form=form, phone_form=phone_form)



if __name__ == '__main__':
    app.run(debug=True)
