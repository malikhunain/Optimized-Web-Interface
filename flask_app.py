from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import zipfile
import shutil
from werkzeug.utils import secure_filename
from modifiers import apply_modifier
import glob
import json
from flask import Response
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
EXTRACT_FOLDER = 'static/extracted'
MODIFIED_FOLDER = 'static/modified'
ALLOWED_EXTENSIONS = {'zip'}

# Create directories if they don't exist
for folder in [UPLOAD_FOLDER, EXTRACT_FOLDER, MODIFIED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER
app.config['MODIFIED_FOLDER'] = MODIFIED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# New global variable to track current displayed image
current_display = {
    'index': -1,
    'timestamp': 0,
    'original_path': '',
    'modified_path': '',
    'filename': ''
}

def update_current_display(index, original_path, modified_path, filename):
    global current_display
    current_display = {
        'index': index,
        'timestamp': time.time(),
        'original_path': original_path,
        'modified_path': modified_path,
        'filename': filename
    }


@app.route('/')
def index():
    # List available datasets (zip files)
    datasets = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.zip')]
    
    # Check if images are extracted and list them
    extracted_images = []
    if os.path.exists(app.config['EXTRACT_FOLDER']):
        extracted_images = [f for f in os.listdir(app.config['EXTRACT_FOLDER']) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # Get available modifiers
    modifiers = [
        {'name': 'Gaussian Noise', 'value': 'gaussian'},
        {'name': 'Shot Noise', 'value': 'shot'},
        {'name': 'Impulse Noise', 'value': 'impulse'},
        {'name': 'Speckle Noise', 'value': 'speckle'},
        {'name': 'Gradual Drift', 'value': 'gradual_drift'},
        {'name': 'Sudden Drift', 'value': 'sudden_drift'}
    ]
    
    return render_template('index.html', 
                          datasets=datasets, 
                          extracted_images=extracted_images,
                          modifiers=modifiers)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash(f'File {filename} uploaded successfully')
        return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload a zip file.')
    return redirect(url_for('index'))

@app.route('/extract/<filename>')
def extract_file(filename):
    # Clean the extraction directory first
    if os.path.exists(app.config['EXTRACT_FOLDER']):
        shutil.rmtree(app.config['EXTRACT_FOLDER'])
    os.makedirs(app.config['EXTRACT_FOLDER'])
    
    # Clean the modified directory
    if os.path.exists(app.config['MODIFIED_FOLDER']):
        shutil.rmtree(app.config['MODIFIED_FOLDER'])
    os.makedirs(app.config['MODIFIED_FOLDER'])
    
    # Extract the zip file
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(app.config['EXTRACT_FOLDER'])
    
    flash(f'Dataset {filename} extracted successfully')
    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        # Clean the extraction directory
        if os.path.exists(app.config['EXTRACT_FOLDER']):
            shutil.rmtree(app.config['EXTRACT_FOLDER'])
        flash(f'Dataset {filename} deleted successfully')
    else:
        flash(f'File {filename} not found')
    
    return redirect(url_for('index'))

@app.route('/prepare_display', methods=['POST'])
def prepare_display():
    selected_modifiers = request.form.getlist('modifiers')
    
    if not selected_modifiers:
        flash('Please select at least one modifier')
        return redirect(url_for('index'))
    
    # Get list of images in the extracted folder
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']:
        image_files.extend(glob.glob(os.path.join(app.config['EXTRACT_FOLDER'], ext)))
    
    if not image_files:
        flash('No images found in the extracted folder')
        return redirect(url_for('index'))
    
    # Store selected modifiers and image list in session
    session['selected_modifiers'] = selected_modifiers
    session['image_files'] = sorted([os.path.basename(f) for f in image_files])
    
    # Clean the modified directory
    if os.path.exists(app.config['MODIFIED_FOLDER']):
        shutil.rmtree(app.config['MODIFIED_FOLDER'])
    os.makedirs(app.config['MODIFIED_FOLDER'])
    
    return redirect(url_for('display_comparison'))

@app.route('/display')
def display_comparison():
    image_files = session.get('image_files', [])
    selected_modifiers = session.get('selected_modifiers', [])
    
    if not image_files or not selected_modifiers:
        flash('No images or modifiers selected')
        return redirect(url_for('index'))
    
    context = {
        'total_images': len(image_files),
        'selected_modifiers': ', '.join(selected_modifiers)
    }
    
    return render_template('display_optimized.html', context=context)

# @app.route('/process_image/<int:index>')
# def process_image(index):
#     image_files = session.get('image_files', [])
#     selected_modifiers = session.get('selected_modifiers', [])
    
#     if not image_files or index >= len(image_files):
#         return jsonify({'error': 'Invalid image index or no images available'})
    
#     # Get the current image
#     image_filename = image_files[index]
#     input_path = os.path.join(app.config['EXTRACT_FOLDER'], image_filename)
#     output_path = os.path.join(app.config['MODIFIED_FOLDER'], image_filename)
    
#     # Process the image only if it hasn't been processed yet
#     if not os.path.exists(output_path):
#         success = apply_modifier(input_path, output_path, selected_modifiers)
#         if not success:
#             return jsonify({'error': f'Failed to process image {image_filename}'})
    
#     # Return paths for display
#     return jsonify({
#         'original': f'/static/extracted/{image_filename}',
#         'modified': f'/static/modified/{image_filename}',
#         'index': index,
#         'total': len(image_files),
#         'filename': image_filename
#     })

@app.route('/process_image/<int:index>')
def process_image(index):
    image_files = session.get('image_files', [])
    selected_modifiers = session.get('selected_modifiers', [])
    
    if not image_files or index >= len(image_files):
        return jsonify({'error': 'Invalid image index or no images available'})
    
    # Get the current image
    image_filename = image_files[index]
    input_path = os.path.join(app.config['EXTRACT_FOLDER'], image_filename)
    output_path = os.path.join(app.config['MODIFIED_FOLDER'], image_filename)
    
    # Process the image only if it hasn't been processed yet
    if not os.path.exists(output_path):
        success = apply_modifier(input_path, output_path, selected_modifiers)
        if not success:
            return jsonify({'error': f'Failed to process image {image_filename}'})
    
    # Prepare paths for response
    original_path = f'/static/extracted/{image_filename}'
    modified_path = f'/static/modified/{image_filename}'
    
    # Update the current display information
    update_current_display(index, original_path, modified_path, image_filename)
    
    # Return paths for display
    return jsonify({
        'original': original_path,
        'modified': modified_path,
        'index': index,
        'total': len(image_files),
        'filename': image_filename
    })

@app.route('/api/current_image', methods=['GET'])
def get_current_image():
    """Return the currently displayed image pair"""
    global current_display
    
    if current_display['index'] == -1:
        return jsonify({
            'status': 'no_image',
            'message': 'No image is currently being displayed'
        }), 404
    
    return jsonify({
        'index': current_display['index'],
        'timestamp': current_display['timestamp'],
        'original': request.host_url.rstrip('/') + current_display['original_path'],
        'modified': request.host_url.rstrip('/') + current_display['modified_path'],
        'filename': current_display['filename']
    })

@app.route('/api/next_image', methods=['GET'])
def get_next_image():
    """Process and return the next image in the sequence"""
    image_files = session.get('image_files', [])
    
    if not image_files:
        return jsonify({
            'status': 'no_images',
            'message': 'No images available'
        }), 404
    
    next_index = current_display['index'] + 1
    if next_index >= len(image_files) or next_index < 0:
        next_index = 0  # Loop back to first image
    
    # Process the next image
    response = process_image(next_index)
    return response

@app.route('/api/images', methods=['GET'])
def get_all_images():
    """Return information about all available images"""
    image_files = session.get('image_files', [])
    selected_modifiers = session.get('selected_modifiers', [])
    
    if not image_files:
        return jsonify({
            'status': 'no_images',
            'message': 'No images available'
        }), 404
    
    return jsonify({
        'count': len(image_files),
        'current_index': current_display['index'],
        'modifiers': selected_modifiers,
        'image_files': image_files
    })

@app.route('/api/stream', methods=['GET'])
def stream():
    host_url = request.host_url.rstrip('/')  # Capture before entering the generator

    def event_stream():
        last_index = -2  # Different from initial -1 to trigger first update
        while True:
            if current_display['index'] != last_index:
                last_index = current_display['index']
                data = {
                    'index': current_display['index'],
                    'timestamp': current_display['timestamp'],
                    'original': host_url + current_display['original_path'],
                    'modified': host_url + current_display['modified_path'],
                    'filename': current_display['filename']
                }
                yield f"data: {json.dumps(data)}\n\n"
            time.sleep(0.2)  # Check for updates every 200ms
    
    return Response(event_stream(), mimetype="text/event-stream")



@app.route('/external_viewer')
def external_viewer():
    return render_template('external_viewer.html')

if __name__ == '__main__':
    app.run(debug=True)