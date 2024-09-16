import os
from gradio_client import Client
from PIL import Image, ImageDraw, ImageFont

os.environ['HF_TOKEN'] = ''


client = Client("black-forest-labs/FLUX.1-schnell")

prompt = "make the image in poster style, "

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

    logo1 = Image.open('logo1.png')
    logo2 = Image.open('logo2.png')

    logo_size = (int(img.width * 0.12), int(img.height * 0.12)) 
    logo1 = logo1.resize(logo_size, Image.ANTIALIAS)
    logo2 = logo2.resize(logo_size, Image.ANTIALIAS)

    margin = 25 
    logo1_position = (margin, margin)
    logo2_position = (img.width - logo_size[0] - margin, margin) 

    img.paste(logo1, logo1_position, logo1)
    img.paste(logo2, logo2_position, logo2)

    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 35) 
    except IOError:
        font_large = ImageFont.load_default() 
        font_small = ImageFont.load_default()

    text_large = "MyComp Society"
    text_small = "wishes you"
    
    text_large_width, text_large_height = draw.textsize(text_large, font=font_large)
    text_small_width, text_small_height = draw.textsize(text_small, font=font_small)

    text_large_x = (img.width - text_large_width) // 2
    text_small_x = (img.width - text_small_width) // 2

    center_y = (logo1_position[1] + logo_size[1] + margin - 30) // 2  
    
    text_large_y = center_y - text_large_height // 2
    text_small_y = text_large_y + text_large_height + 5 
    
    draw.text((text_large_x, text_large_y), text_large, font=font_large, fill="white")
    draw.text((text_small_x, text_small_y), text_small, font=font_small, fill="white")
    

    img.save(new_image_path, 'PNG')

print(f"Image saved at {new_image_path}")

import shutil
shutil.rmtree(gradio_temp_folder)
os.makedirs(gradio_temp_folder)
