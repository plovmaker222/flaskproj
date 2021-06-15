from flask import abort, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from . import home
from .. import db
from forms import IssueForm, IssueAssignForm
from ..models import Employee, Issue

@home.route('/')
def homepage():
    return render_template('home/index.html', title = "welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    issues = Issue.query.all()
    return render_template('home/dashboard.html', issues=issues, title = "dashboard")

@home.route('/issues/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_issue(id):
    add_issue = False
    issue = Issue.query.get_or_404(id)
    form = IssueForm(obj=issue)
    if form.validate_on_submit():
        issue.name = form.name.data
        issue.desc = form.description.data
        db.session.commit()
        flash('You have successfully edited the issue.')

        return redirect(url_for('home.dashboard'))

    form.description.data = issue.desc
    form.name.data = issue.name
    return render_template('home/issue.html', action="Edit",
                           add_issue=add_issue, form=form,
                           issue=issue, title="Edit issue")

@home.route('/issues/add', methods=['GET', 'POST'])
@login_required
def add_issue():
    add_issue = True
    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(name=form.name.data,
                                desc=form.description.data,
                                status=form.status.data)
        try:
            db.session.add(issue)
            db.session.commit()
            flash('You have successfully added a new issue.')
        except:
            flash('Error: issue name already exists.')
        return redirect(url_for('home.dashboard'))
    return render_template('home/issue.html', action="Add",
                           add_issue=add_issue, form=form,
                           title="New issue")

@home.route('/issues/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_issue(id):
    issue = Issue.query.get_or_404(id)
    form = IssueAssignForm(obj=issue)
    if form.validate_on_submit():
        issue.assigned_to = form.employee.data
        db.session.add(issue)
        db.session.commit()
        flash('You have successfully assigned an issue.')
        return redirect(url_for('home.dashboard'))
    return render_template('home/issue.html',
                           issue=issue, form=form,
                           title='Assign Issue')

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
