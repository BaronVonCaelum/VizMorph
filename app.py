#!/usr/bin/env python3
"""
VizMorph - Tableau Workbook Visualization Suggestion Engine
Main Flask application entry point
"""

import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

from src.tableau_parser import TableauParser
from src.viz_recommender import VizRecommender
from src.viz_generator import VizGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
tableau_parser = TableauParser()
viz_recommender = VizRecommender()
viz_generator = VizGenerator()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_workbook():
    """Upload and parse a Tableau workbook"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith(('.twb', '.twbx')):
            return jsonify({'error': 'Invalid file type. Please upload a .twb or .twbx file'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse the workbook
        workbook_data = tableau_parser.parse_workbook(filepath)
        
        return jsonify({
            'success': True,
            'workbook_id': workbook_data['id'],
            'summary': workbook_data['summary'],
            'worksheets': workbook_data['worksheets']
        })
        
    except Exception as e:
        logger.error(f"Error uploading workbook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggest/<workbook_id>')
def suggest_visualizations(workbook_id):
    """Get visualization suggestions for a workbook"""
    try:
        # Get workbook data
        workbook_data = tableau_parser.get_workbook_data(workbook_id)
        if not workbook_data:
            return jsonify({'error': 'Workbook not found'}), 404
        
        # Generate suggestions
        suggestions = viz_recommender.generate_suggestions(workbook_data)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        logger.error(f"Error generating suggestions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview/<suggestion_id>')
def preview_visualization(suggestion_id):
    """Generate a D3.js preview of a suggested visualization"""
    try:
        # Get suggestion data
        suggestion = viz_recommender.get_suggestion(suggestion_id)
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404
        
        # Generate D3.js visualization
        d3_config = viz_generator.generate_d3_config(suggestion)
        
        return jsonify({
            'success': True,
            'config': d3_config
        })
        
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/<suggestion_id>')
def export_visualization(suggestion_id):
    """Export a visualization in various formats"""
    try:
        format_type = request.args.get('format', 'json')
        
        suggestion = viz_recommender.get_suggestion(suggestion_id)
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404
        
        export_data = viz_generator.export_visualization(suggestion, format_type)
        
        return jsonify({
            'success': True,
            'data': export_data
        })
        
    except Exception as e:
        logger.error(f"Error exporting visualization: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
