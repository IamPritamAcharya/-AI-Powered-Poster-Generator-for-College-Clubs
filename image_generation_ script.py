import os
import shutil
from gradio_client import Client
from PIL import Image

os.environ['HF_TOKEN'] = ''

client = Client("black-forest-labs/FLUX.1-schnell")

prompt = "A golden cat holding a sign that says hello world"

folder_path = os.path.join(os.getcwd(), 'image_gen')

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if filename.endswith('.png'):
        os.remove(file_path)

gradio_temp_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'gradio')

if os.path.exists(gradio_temp_folder):
    for root, dirs, files in os.walk(gradio_temp_folder):
        for file in files:
            if file.endswith('.webp') or file.endswith('.png'):
                os.remove(os.path.join(root, file))


result = client.predict(
    prompt,
    seed=0,
    randomize_seed=True,
    width=1024,
    height=1024,
    num_inference_steps=4,
    api_name="/infer"
)


image_path = result[0]

with Image.open(image_path) as img:
    
    new_image_path = os.path.join(folder_path, 'generated_image.png')
    img.save(new_image_path, 'PNG')

print(f"Image saved at {new_image_path}")

shutil.rmtree(gradio_temp_folder)
os.makedirs(gradio_temp_folder)  
