from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Link, Comment
from app import db
from utils import get_top_links

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    links = get_top_links(Link.query.all())
    return render_template('index.html', links=links)

@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        if not title or not url:
            flash('Title and URL are required.')
            return redirect(url_for('main.submit'))
        link = Link(title=title, url=url, user_id=current_user.id)
        db.session.add(link)
        db.session.commit()
        flash('Your link has been submitted.')
        return redirect(url_for('main.index'))
    return render_template('submit.html')

@bp.route('/item/<int:id>', methods=['GET', 'POST'])
def item(id):
    link = Link.query.get_or_404(id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You need to be logged in to comment.')
            return redirect(url_for('main.item', id=id))
        content = request.form['content']
        parent_id = request.form.get('parent_id')
        comment = Comment(content=content, user_id=current_user.id, link_id=id, parent_id=parent_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.')
        return redirect(url_for('main.item', id=id))
    return render_template('item.html', link=link)
