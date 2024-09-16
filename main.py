import os
from gradio_client import Client
from PIL import Image, ImageDraw, ImageFont

# Set up your Hugging Face token
os.environ['HF_TOKEN'] = ''

# Define the client with the model name
client = Client("black-forest-labs/FLUX.1-schnell")

# Define the prompt
prompt = "make the image in poster style, "

# Define the folder path where the image will be saved
folder_path = os.path.join(os.getcwd(), 'image_gen')

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Delete existing images in the image_gen folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if filename.endswith('.png'):
        os.remove(file_path)

# Define the path to the Gradio temporary folder
gradio_temp_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'gradio')

# Delete existing images in the Gradio temporary folder
if os.path.exists(gradio_temp_folder):
    for root, dirs, files in os.walk(gradio_temp_folder):
        for file in files:
            if file.endswith('.webp') or file.endswith('.png'):
                os.remove(os.path.join(root, file))

# Generate the image
result = client.predict(
    prompt,
    seed=0,
    randomize_seed=True,
    width=1024,
    height=1024,
    num_inference_steps=4,
    api_name="/infer"
)

# Get the image path from the result
image_path = result[0]  # This is the path to the generated .webp image

# Load the main image using PIL
with Image.open(image_path) as img:
    # Convert the image to PNG format
    new_image_path = os.path.join(folder_path, 'generated_image.png')
    
    # Load the logos
    logo1 = Image.open('logo1.png')
    logo2 = Image.open('logo2.png')
    
    # Resize logos to smaller size
    logo_size = (int(img.width * 0.12), int(img.height * 0.12))  # 12% of main image size
    logo1 = logo1.resize(logo_size, Image.ANTIALIAS)
    logo2 = logo2.resize(logo_size, Image.ANTIALIAS)
    
    # Calculate positions for logos
    margin = 25  # Distance from edges
    logo1_position = (margin, margin)  # Top-left
    logo2_position = (img.width - logo_size[0] - margin, margin)  # Top-right
    
    # Paste the logos onto the main image
    img.paste(logo1, logo1_position, logo1)
    img.paste(logo2, logo2_position, logo2)
    
    # Draw text in the top center
    draw = ImageDraw.Draw(img)
    
    # Load a font
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)  # Large font for "MyComp Society"
        font_small = ImageFont.truetype("arial.ttf", 35)  # Small font for "wishes you"
    except IOError:
        font_large = ImageFont.load_default()  # Fallback to default font
        font_small = ImageFont.load_default()
    
    # Text content
    text_large = "MyComp Society"
    text_small = "wishes you"
    
    # Calculate text size and position for centering
    text_large_width, text_large_height = draw.textsize(text_large, font=font_large)
    text_small_width, text_small_height = draw.textsize(text_small, font=font_small)
    
    # Calculate the x position for centering the text
    text_large_x = (img.width - text_large_width) // 2
    text_small_x = (img.width - text_small_width) // 2
    
    # Calculate the y position for centering the text vertically between the logos
    center_y = (logo1_position[1] + logo_size[1] + margin - 30) // 2  # Middle point between top edge and bottom of logo
    
    # Set y positions for the text
    text_large_y = center_y - text_large_height // 2
    text_small_y = text_large_y + text_large_height + 5  # Small gap between texts
    
    # Add the text to the image
    draw.text((text_large_x, text_large_y), text_large, font=font_large, fill="white")
    draw.text((text_small_x, text_small_y), text_small, font=font_small, fill="white")
    
    # Save the final image
    img.save(new_image_path, 'PNG')

print(f"Image saved at {new_image_path}")

# Optionally, clean up the temporary Gradio folder after saving the image
import shutil
shutil.rmtree(gradio_temp_folder)
os.makedirs(gradio_temp_folder)  # Recreate an empty folder for future use
