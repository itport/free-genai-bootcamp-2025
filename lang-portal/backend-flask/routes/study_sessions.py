from flask import request, jsonify, g
from flask_cors import cross_origin
from datetime import datetime
import math

def load(app):
  @app.route('/api/study-sessions', methods=['GET'])
  @cross_origin()
  def get_study_sessions():
    try:
      cursor = app.db.cursor()

      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get total count
      cursor.execute('''
      SELECT COUNT(*) as count
      FROM study_sessions ss
      JOIN groups g ON g.id = ss.group_id
      JOIN study_activities sa ON sa.id = ss.study_activity_id
      ''')
      total_count = cursor.fetchone()['count']

      # Get paginated sessions
      cursor.execute('''
      SELECT
      ss.id,
      ss.group_id,
      g.name as group_name,
      sa.id as activity_id,
      sa.name as activity_name,
      ss.created_at,
      COUNT(wri.id) as review_items_count
      FROM study_sessions ss
      JOIN groups g ON g.id = ss.group_id
      JOIN study_activities sa ON sa.id = ss.study_activity_id
      LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
      GROUP BY ss.id
      ORDER BY ss.created_at DESC
      LIMIT ? OFFSET ?
      ''', (per_page, offset))
      sessions = cursor.fetchall()

      return jsonify({
        'items': [{
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time since we don't track end time
          'review_items_count': session['review_items_count']
        } for session in sessions],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/<id>', methods=['GET'])
  @cross_origin()
  def get_study_session(id):
    try:
      cursor = app.db.cursor()

      # Get session details
      cursor.execute('''
      SELECT
      ss.id,
      ss.group_id,
      g.name as group_name,
      sa.id as activity_id,
      sa.name as activity_name,
      ss.created_at,
      COUNT(wri.id) as review_items_count
      FROM study_sessions ss
      JOIN groups g ON g.id = ss.group_id
      JOIN study_activities sa ON sa.id = ss.study_activity_id
      LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
      WHERE ss.id = ?
      GROUP BY ss.id
      ''', (id,))

      session = cursor.fetchone()
      if not session:
        return jsonify({"error": "Study session not found"}), 404

      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get the words reviewed in this session with their review status
      cursor.execute('''
      SELECT
      w.*,
      COALESCE(SUM(CASE WHEN wri.correct = 1 THEN 1 ELSE 0 END), 0) as session_correct_count,
      COALESCE(SUM(CASE WHEN wri.correct = 0 THEN 1 ELSE 0 END), 0) as session_wrong_count
      FROM words w
      JOIN word_review_items wri ON wri.word_id = w.id
      WHERE wri.study_session_id = ?
      GROUP BY w.id
      ORDER BY w.kanji
      LIMIT ? OFFSET ?
      ''', (id, per_page, offset))

      words = cursor.fetchall()

      # Get total count of words
      cursor.execute('''
      SELECT COUNT(DISTINCT w.id) as count
      FROM words w
      JOIN word_review_items wri ON wri.word_id = w.id
      WHERE wri.study_session_id = ?
      ''', (id,))

      total_count = cursor.fetchone()['count']

      return jsonify({
        'session': {
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time
          'review_items_count': session['review_items_count']
        },
        'words': [{
          'id': word['id'],
          'kanji': word['kanji'],
          'romaji': word['romaji'],
          'english': word['english'],
          'correct_count': word['session_correct_count'],
          'wrong_count': word['session_wrong_count']
        } for word in words],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  # todo POST /study_sessions/:id/review
  # This endpoint records the results of a review within a study session. It receives a list of word review items, each containing the word ID, whether it was answered correctly, and (optionally) a timestamp.
  
  @app.route('/api/study-sessions/<int:id>/review', methods=['POST'])
  @cross_origin()
  def record_review_results(id):
    try:
        cursor = app.db.cursor()

        # Check if the study session exists
        cursor.execute('SELECT id FROM study_sessions WHERE id = ?', (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Study session not found"}), 404

        # Get review data from the request body
        data = request.get_json()
        review_items = data.get('review_items')  # Expecting a list

        if not review_items or not isinstance(review_items, list):
            return jsonify({"error": "review_items must be a non-empty list"}), 400

        # Insert each review item
        for item in review_items:
            word_id = item.get('word_id')
            correct = item.get('correct')
            created_at = item.get('created_at', datetime.utcnow()) # Use current time if not provided.

            # Basic validation
            if word_id is None or correct is None:
                return jsonify({"error": "Each review item must have word_id and correct"}), 400
            if not isinstance(correct, bool):
                return jsonify({"error": "correct must be a boolean"}), 400

            # Check if word exists.  Important for data integrity.
            cursor.execute('SELECT id FROM words WHERE id = ?', (word_id,))
            if not cursor.fetchone():
                return jsonify({"error": f"Word with id {word_id} not found"}), 400

            # Insert into word_review_items
            cursor.execute('''
                INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
                VALUES (?, ?, ?, ?)
            ''', (word_id, id, int(correct), created_at))  # Convert correct to int (0 or 1)

        app.db.commit()

        # Update correct_count and wrong_count in word_reviews table
        # This is done *after* inserting all review items to avoid partial updates.
        for item in review_items:
            word_id = item.get('word_id')
            correct = item.get('correct')

            cursor.execute('''
                INSERT INTO word_reviews (word_id, correct_count, wrong_count)
                VALUES (?, ?, ?)
                ON CONFLICT(word_id) DO UPDATE SET
                correct_count = correct_count + ?,
                wrong_count = wrong_count + ?
            ''', (word_id, int(correct), 1-int(correct), int(correct), 1-int(correct)))

        app.db.commit()

        return jsonify({"message": "Review results recorded successfully"}), 201

    except Exception as e:
        app.db.get().rollback()
        return jsonify({"error": str(e)}), 500

  # todo /study_sessions POST
  # This endpoint creates a new study session. It receives the group ID and study activity ID, and records the start time (using the current server time).
  
  @app.route('/api/study-sessions', methods=['POST'])
  @cross_origin()
  def create_study_session():
    try:
        cursor = app.db.cursor()

        # Get data from the request body (expecting JSON)
        data = request.get_json()
        group_id = data.get('group_id')
        study_activity_id = data.get('study_activity_id')

        # Validate the input: both IDs must be provided
        if not group_id or not study_activity_id:
            return jsonify({"error": "Both group_id and study_activity_id are required"}), 400

        # Check if group exists
        cursor.execute('SELECT id FROM groups WHERE id = ?', (group_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Group not found"}), 404

        # Check if study activity exists
        cursor.execute('SELECT id FROM study_activities WHERE id = ?', (study_activity_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Study activity not found"}), 404

        # Get the current time (UTC) for the 'created_at' field
        created_at = datetime.utcnow()

        # Insert the new study session
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (?, ?, ?)
        ''', (group_id, study_activity_id, created_at))

        # Get the ID of the newly created session
        session_id = cursor.lastrowid
        app.db.commit()  # Commit the transaction

        # Return the ID of the created session
        return jsonify({"id": session_id}), 201  # 201 Created status code

    except Exception as e:
        app.db.get().rollback()  # Rollback in case of error.
        return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/reset', methods=['POST'])
  @cross_origin()
  def reset_study_sessions():
    try:
      cursor = app.db.cursor()

      # First delete all word review items since they have foreign key constraints
      cursor.execute('DELETE FROM word_review_items')

      # Then delete all study sessions
      cursor.execute('DELETE FROM study_sessions')

      app.db.commit()

      return jsonify({"message": "Study history cleared successfully"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500