from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from database import db
from models import Voting, Option, Vote

voting_bp = Blueprint('voting', __name__)

@voting_bp.route('/')
def index():
    votings = Voting.query.order_by(Voting.created_at.desc()).all()
    return render_template('index.html', votings=votings)

@voting_bp.route('/votings')
def list_votings():
    votings = Voting.query.all()
    return jsonify([v.to_dict() for v in votings])

@voting_bp.route('/votings/<int:voting_id>')
def voting_detail(voting_id):
    voting = Voting.query.get_or_404(voting_id)
    return render_template('detail.html', voting=voting)

@voting_bp.route('/votings/new', methods=['GET'])
def new_voting_page():
    return render_template('create.html')

@voting_bp.route('/votings', methods=['POST'])
def create_voting():
    data = request.form
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    image_url = data.get('image_url')
    is_multiple_choice = 'is_multiple_choice' in data
    
    options_texts = request.form.getlist('options[]')
    
    if not title or not options_texts:
        flash('Title and at least one option are required.', 'error')
        return redirect(url_for('voting.new_voting_page'))

    new_voting = Voting(
        title=title,
        description=description,
        category=category,
        image_url=image_url,
        is_multiple_choice=is_multiple_choice
    )
    db.session.add(new_voting)
    db.session.flush()

    for text in options_texts:
        if text.strip():
            option = Option(voting_id=new_voting.id, text=text.strip())
            db.session.add(option)
    
    db.session.commit()
    return redirect(url_for('voting.index'))

@voting_bp.route('/vote', methods=['POST'])
def submit_vote():
    voting_id = request.form.get('voting_id')
    option_ids = request.form.getlist('options[]')
    ip_address = request.remote_addr

    if not voting_id or not option_ids:
        flash('Please select an option.', 'error')
        return redirect(url_for('voting.voting_detail', voting_id=voting_id))

    # Check for duplicate vote
    existing_vote = Vote.query.filter_by(voting_id=voting_id, ip_address=ip_address).first()
    if existing_vote:
        flash('You have already voted on this poll.', 'error')
        return redirect(url_for('voting.results', voting_id=voting_id))

    voting = Voting.query.get_or_404(voting_id)
    
    # Process votes
    for oid in option_ids:
        option = Option.query.get(oid)
        if option and option.voting_id == voting.id:
            option.vote_count += 1
    
    # Register the vote
    new_vote = Vote(voting_id=voting_id, ip_address=ip_address)
    db.session.add(new_vote)
    db.session.commit()

    return redirect(url_for('voting.results', voting_id=voting_id))

@voting_bp.route('/results/<int:voting_id>')
def results(voting_id):
    voting = Voting.query.get_or_404(voting_id)
    total_votes = sum(option.vote_count for option in voting.options)
    return render_template('results.html', voting=voting, total_votes=total_votes)

@voting_bp.route('/health')
def health_check():
    return {"status": "healthy"}, 200
