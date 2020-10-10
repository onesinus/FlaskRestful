from flask import (
    Blueprint, g, request
)

from werkzeug.exceptions import abort

from apis.auth import login_required
from apis.db import get_db

bp = Blueprint('blog', __name__, url_prefix="/blog")

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return {
        'success': True,
        'posts': posts
    }

@bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    body = request.form.get('body')

    error = None

    if not title:
        error = 'Title is required'

    if not body:
        error = 'Body is required'

    if error is not None:
        return {
            "success": False,
            "error": error
        }
    
    db = get_db()
    db.execute(
        'INSERT INTO post (title, body, author_id)'
        ' VALUES(?, ?, ?)',
        (title, body, g.user[0])
    )

    db.commit()
    return {
        "success": True,
        "data": {
            "user_id": g.user[0],
            "title": title,
            "body": body
        }
    }

@bp.route('/<int:id>/view')
def get_post(id):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id, )
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return {
        "success": True,
        "data": post
    }    

@bp.route('/<int:id>/edit', methods=['PUT'])
@login_required
def update(id):
    title = request.form.get('title')
    body = request.form.get('body')

    error = None

    if not title:
        error = 'Title is required'

    if not body:
        error = 'Body is required'

    if error is not None:
        return {
            "success": False,
            "error": error
        }        

    db = get_db()
    db.execute(
        'UPDATE post SET title = ?, body = ?'
        ' WHERE id = ?',
        (title, body, id)
    )

    db.commit()

    return {
        "success": True,
        "data": {
            "user_id": g.user[0],
            "title": title,
            "body": body
        }
    }

@bp.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ? ', (id, ))
    db.commit()

    return {
        "success": True,
        "data": {
            "id": id
        }
    }