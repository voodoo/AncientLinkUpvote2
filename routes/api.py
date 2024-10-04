from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Link, Vote
from app import db

bp = Blueprint('api', __name__)

@bp.route('/api/upvote/<int:link_id>', methods=['POST'])
@login_required
def upvote(link_id):
    link = Link.query.get_or_404(link_id)
    vote = Vote.query.filter_by(user_id=current_user.id, link_id=link_id).first()
    
    if vote:
        return jsonify({'error': 'You have already voted for this link'}), 400
    
    new_vote = Vote(user_id=current_user.id, link_id=link_id)
    link.score += 1
    db.session.add(new_vote)
    db.session.commit()
    
    return jsonify({'success': True, 'new_score': link.score})
