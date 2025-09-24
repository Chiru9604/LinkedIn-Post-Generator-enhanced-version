from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from post_generator import generate_post
from few_shot import FewShotPosts
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize few shot posts to get available tags
few_shot = FewShotPosts()

@app.route('/')
def index():
    """Serve the HTML page"""
    try:
        with open('linkedin_post_generator.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return "HTML file not found. Please make sure linkedin_post_generator.html exists.", 404

@app.route('/api/generate-post', methods=['POST'])
def api_generate_post():
    """API endpoint to generate LinkedIn posts"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        topic = data.get('topic')
        length = data.get('length')
        language = data.get('language')
        
        if not all([topic, length, language]):
            return jsonify({'error': 'Missing required fields: topic, length, language'}), 400
        
        # Validate values
        valid_lengths = ['Short', 'Medium', 'Long']
        valid_languages = ['English', 'Hinglish']
        
        if length not in valid_lengths:
            return jsonify({'error': f'Invalid length. Must be one of: {valid_lengths}'}), 400
        
        if language not in valid_languages:
            return jsonify({'error': f'Invalid language. Must be one of: {valid_languages}'}), 400
        
        # Generate the post
        generated_post = generate_post(length, language, topic)
        
        return jsonify({
            'success': True,
            'post': generated_post,
            'parameters': {
                'topic': topic,
                'length': length,
                'language': language
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate post: {str(e)}'
        }), 500

@app.route('/api/topics', methods=['GET'])
def api_get_topics():
    """API endpoint to get available topics"""
    try:
        topics = few_shot.get_tags()
        return jsonify({
            'success': True,
            'topics': sorted(topics)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get topics: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'LinkedIn Post Generator API is running'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if required files exist
    required_files = ['post_generator.py', 'few_shot.py', 'llm_helper.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Warning: Missing required files: {missing_files}")
        print("Make sure all dependencies are in place before running the server.")
    
    # Check if data file exists
    if not os.path.exists('data/processed_posts.json'):
        print("Warning: Data file 'data/processed_posts.json' not found.")
        print("The application may not work properly without the training data.")
    
    print("Starting LinkedIn Post Generator API server...")
    print("Access the application at: http://localhost:5000")
    print("API endpoints:")
    print("  POST /api/generate-post - Generate a LinkedIn post")
    print("  GET  /api/topics - Get available topics")
    print("  GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)