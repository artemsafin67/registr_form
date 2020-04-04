from flask import Flask, render_template, request, redirect

from data.login_form import LoginForm

from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User

import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FDJKFJKFJKDFJ'


@app.route('/')
def works_journal():
    session = create_session()
    news = session.query(Jobs).all()
    return render_template('works_journal.html', title='Works journal', news=news)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    session = create_session()

    if form.validate_on_submit():
        user = User()
        user.name = form['name'].data
        user.surname = form['surname'].data
        user.age = form['age'].data
        user.position = form['position'].data
        user.speciality = form['speciality'].data
        user.address = form['address'].data
        user.email = form['login_email'].data
        user.set_password(form['password'].data)
        user.modified_date = datetime.datetime.now()
        session.add(user)
        session.commit()
        return redirect('/success')
    else:
        return render_template('register.html', form=form, title="Register Form")


def main():
    global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
