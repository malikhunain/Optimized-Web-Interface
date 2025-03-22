import numpy as np
import cv2
from skimage.util import random_noise
import os

def apply_gaussian_noise(image, mean=0, var=0.3):
    """Apply Gaussian noise to the image with increased variance."""
    # Convert to float [0-1] for skimage function
    img_float = image.astype(float) / 255.0
    noisy = random_noise(img_float, mode='gaussian', mean=mean, var=var)
    return np.array(255 * noisy, dtype=np.uint8)

def apply_shot_noise(image, amount=0.1):
    """Apply shot noise (Poisson noise) to the image."""
    # Convert to float [0-1] for skimage function
    img_float = image.astype(float) / 255.0
    # Scale the image to increase the noise effect
    scaled = img_float * 10.0  # Scale up to enhance Poisson noise effect
    noisy = random_noise(scaled, mode='poisson')
    # Scale back down and clip
    result = np.clip(noisy / 10.0, amount, 1)
    return np.array(255 * result, dtype=np.uint8)

def apply_impulse_noise(image, amount=0.3):
    """Apply impulse noise (salt & pepper) to the image with increased amount."""
    # Convert to float [0-1] for skimage function
    img_float = image.astype(float) / 255.0
    noisy = random_noise(img_float, mode='s&p', amount=amount)
    return np.array(255 * noisy, dtype=np.uint8)

def apply_speckle_noise(image, var=0.3):
    """Apply speckle noise to the image with increased variance."""
    # Convert to float [0-1] for skimage function
    img_float = image.astype(float) / 255.0
    noisy = random_noise(img_float, mode='speckle', var=var)
    return np.array(255 * noisy, dtype=np.uint8)

def apply_gradual_drift(image, drift_amount=0.6):
    """Apply gradual drift to the image (brightness shift) with increased effect."""
    # Convert to float and normalize
    img_float = image.astype(float) / 255.0
    
    # Create a gradient mask (left to right)
    h, w = img_float.shape[:2]
    gradient = np.linspace(0, drift_amount, w)
    gradient_mask = np.tile(gradient, (h, 1))
    
    # Apply the gradient mask
    if len(img_float.shape) > 2:  # Color image
        gradient_mask = np.stack([gradient_mask] * 3, axis=2)
    
    # Add the gradient to the image and clip values
    drifted = np.clip(img_float + gradient_mask, 0, 1)
    
    return np.array(255 * drifted, dtype=np.uint8)

def apply_sudden_drift(image, drift_amount=0.7):
    """Apply sudden drift to the image (half image shifted) with increased effect."""
    # Convert to float and normalize
    img_float = image.astype(float) / 255.0
    
    # Create a sudden shift mask (upper half normal, lower half shifted)
    h, w = img_float.shape[:2]
    mask = np.zeros((h, w))
    mask[h//2:, :] = drift_amount
    
    # Apply the mask
    if len(img_float.shape) > 2:  # Color image
        mask = np.stack([mask] * 3, axis=2)
    
    # Add the mask to the image and clip values
    drifted = np.clip(img_float + mask, 0, 1)
    
    return np.array(255 * drifted, dtype=np.uint8)

def apply_modifier(input_path, output_path, modifiers):
    """Apply selected modifiers to an image."""
    try:
        # Read the image
        img = cv2.imread(input_path)
        
        if img is None:
            print(f"Error reading image: {input_path}")
            return False
        
        # Convert BGR to RGB for processing
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Make a copy of the original image to ensure we're not modifying the original
        modified_img = img.copy()
        
        # Apply each selected modifier with more pronounced effects
        for modifier in modifiers:
            if modifier == 'gaussian':
                modified_img = apply_gaussian_noise(modified_img)
            elif modifier == 'shot':
                modified_img = apply_shot_noise(modified_img)
            elif modifier == 'impulse':
                modified_img = apply_impulse_noise(modified_img)
            elif modifier == 'speckle':
                modified_img = apply_speckle_noise(modified_img)
            elif modifier == 'gradual_drift':
                modified_img = apply_gradual_drift(modified_img)
            elif modifier == 'sudden_drift':
                modified_img = apply_sudden_drift(modified_img)
        
        # Convert RGB back to BGR for saving with OpenCV
        modified_img = cv2.cvtColor(modified_img, cv2.COLOR_RGB2BGR)
        
        # Save the modified image
        success = cv2.imwrite(output_path, modified_img)
        if not success:
            print(f"Failed to save image to {output_path}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error processing image {input_path}: {str(e)}")
        return False