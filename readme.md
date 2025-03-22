# Image Modifier Interface

This Flask application allows users to upload image datasets, apply various noise and drift modifiers to the images, and display the original and modified images side by side for comparison.

## Features

Upload image datasets in ZIP format.
Extract and display images from the uploaded dataset.
Apply various noise and drift modifiers to the images.
View original and modified images side by side.
Start, pause, and navigate through a slideshow of the images.

## Requirements

The application requires the following Python packages:

```bash
blinker==1.9.0
click==8.1.8
Flask==2.3.3
imageio==2.37.0
itsdangerous==2.2.0
Jinja2==3.1.6
lazy_loader==0.4
MarkupSafe==3.0.2
networkx==3.4.2
numpy==1.24.3
opencv-python-headless==4.6.0.66
packaging==24.2
pillow==11.1.0
scikit-image==0.25.2
scipy==1.15.2
tifffile==2025.3.13
Werkzeug==2.3.7
```

## Installation

 1. Clone the repository:

 ```bash
    git clone https://github.com/yourusername/image-modifier-interface.git
    cd image-modifier-interface
```
 2. Create a virtual environment and activate it:

 ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
 3. Install the required packages:

 ```bash
    pip install -r requirements.txt
```

## Usage

 1. Run the Flask application:
 2. Open your web browser and navigate to http://127.0.0.1:5000.

 3. Upload a ZIP file containing your image dataset.

 4. Extract the dataset and select the modifiers you want to apply.

 5. View the original and modified images side by side.

## Modifiers
The following modifiers are available:

 - Gaussian Noise
 - Shot Noise
 - Impulse Noise
 - Speckle Noise
 - Gradual Drift
 - Sudden Drift

## File Structure

- flask_app.py: Main Flask application file.
- modifiers.py: Contains functions to apply various noise and drift modifiers to images.
- templates: Contains HTML templates for the web interface.
- static: Contains uploaded, extracted, and modified images.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
This application uses the following libraries:

- Flask
- OpenCV
- scikit-image
- NumPy
- Bootstrap

Feel free to contribute to this project by submitting issues or pull requests.