from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required
from models import Link, Vote
from app import db

bp = Blueprint('api', __name__)

@bp.route('/api/upvote/<int:link_id>', methods=['POST'])
@login_required
def upvote(link_id):
    try:
        current_app.logger.info(f"User {current_user.id} attempting to upvote link {link_id}")
        link = Link.query.get_or_404(link_id)
        vote = Vote.query.filter_by(user_id=current_user.id, link_id=link_id).first()
        
        if vote:
            current_app.logger.info(f"User {current_user.id} has already voted for link {link_id}")
            return jsonify({'error': 'You have already voted for this link'}), 400
        
        new_vote = Vote(user_id=current_user.id, link_id=link_id)
        db.session.add(new_vote)
        link.score += 1
        db.session.commit()
        
        current_app.logger.info(f"User {current_user.id} successfully upvoted link {link_id}")
        return jsonify({'success': True, 'new_score': link.score})
    except Exception as e:
        current_app.logger.error(f"Error in upvote: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'An error occurred while processing your vote'}), 500
