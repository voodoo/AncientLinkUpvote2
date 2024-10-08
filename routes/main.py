from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Link, Comment, User
from app import db
from utils import get_top_links
from sqlalchemy import or_, func, and_
from datetime import datetime, timedelta
from urllib.parse import urlparse

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

@bp.route('/link/search')
def search():
    if not request.args:
        return render_template('search_results.html', links=None, comments=None, query='', search_type='all', date_range='all', urlparse=urlparse)

    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')
    date_range = request.args.get('date_range', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    if query:
        links_query = Link.query.filter(
            or_(
                func.lower(Link.title).contains(func.lower(query)),
                func.lower(Link.url).contains(func.lower(query))
            )
        )
        comments_query = Comment.query.filter(func.lower(Comment.content).contains(func.lower(query)))

        if date_range != 'all':
            date_filter = datetime.utcnow() - timedelta(days=int(date_range))
            links_query = links_query.filter(Link.created_at >= date_filter)
            comments_query = comments_query.filter(Comment.created_at >= date_filter)

        if search_type == 'links':
            comments_query = Comment.query.filter(False)
        elif search_type == 'comments':
            links_query = Link.query.filter(False)

        links = links_query.order_by(Link.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        comments = comments_query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    else:
        links = Link.query.order_by(Link.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        comments = Comment.query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('search_results.html', links=links, comments=comments, query=query, search_type=search_type, date_range=date_range, urlparse=urlparse)
