import os
import shutil
from gradio_client import Client
from PIL import Image

# Set up your Hugging Face token
os.environ['HF_TOKEN'] = ''

# Define the client with the model name
client = Client("black-forest-labs/FLUX.1-schnell")

# Define the prompt
prompt = "A golden cat holding a sign that says hello world"

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

# Load the image using PIL
with Image.open(image_path) as img:
    # Convert the image to PNG format
    new_image_path = os.path.join(folder_path, 'generated_image.png')
    img.save(new_image_path, 'PNG')

print(f"Image saved at {new_image_path}")

# Optionally, clean up the temporary Gradio folder after saving the image
shutil.rmtree(gradio_temp_folder)
os.makedirs(gradio_temp_folder)  # Recreate an empty folder for future use
