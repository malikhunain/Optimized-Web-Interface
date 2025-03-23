# Image Modifier Interface

This Flask application allows users to upload image datasets, apply various noise and drift modifiers to the images, and display the original and modified images side by side for comparison.

## Features

- Upload image datasets in ZIP format.
- Extract and display images from the uploaded dataset.
- Apply various noise and drift modifiers to the images.
- View original and modified images side by side.
- Start, pause, and navigate through a slideshow of the images.
- Sync with an external viewer for real-time updates.

## Requirements

The application requires the following Python packages:

```bash
aniso8601==10.0.0
blinker==1.9.0
click==8.1.8
Flask==2.3.3
Flask-RESTful==0.3.10
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
pytz==2025.1
scikit-image==0.25.2
scipy==1.15.2
six==1.17.0
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

```bash
python flask_app.py
```

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

## API Endpoints

- `GET /api/current_image`: Returns the currently displayed image pair.
- `GET /api/next_image`: Processes and returns the next image in the sequence.
- `GET /api/images`: Returns information about all available images.
- `GET /api/stream`: Streams real-time updates of the currently displayed image.

## Test API

Visit `http://127.0.0.1:5000/external_viewer` to test the API stream data.

## File Structure

- `flask_app.py`: Main Flask application file.
- `modifiers.py`: Contains functions to apply various noise and drift modifiers to images.
- `templates`: Contains HTML templates for the web interface.
- `static`: Contains uploaded, extracted, and modified images.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This application uses the following libraries:

- Flask
- OpenCV
- scikit-image
- NumPy
- Bootstrap

Feel free to contribute to this project by submitting issues or pull requests.
