import os
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
from gradio_client import Client
import time
import sv_ttk

os.environ['HF_TOKEN'] = ''

client = Client("black-forest-labs/FLUX.1-schnell")

def generate_image(prompt_user, logo1_path, logo2_path, font_large_path, font_small_path, large_text, small_text, large_text_color, small_text_color, status_label):
    prompt = f"{prompt_user} poster, add event greeting at center"
    
    folder_path = os.path.join(os.getcwd(), 'image_gen')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Delete existing images in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            os.remove(os.path.join(folder_path, filename))

    status_label.config(text="Generating poster...")

    result = client.predict(
        prompt,
        seed=0,
        randomize_seed=True,
        width=1024,
        height=1024,
        num_inference_steps=4,
        api_name="/infer"
    )
    
    # Load the generated image
    image_path = result[0]  
    with Image.open(image_path) as img:
        new_image_path = os.path.join(folder_path, 'generated_image.png')
        
        # Load the logos or use default ones
        logo1 = Image.open(logo1_path) if logo1_path else Image.open('logo1.png')
        logo2 = Image.open(logo2_path) if logo2_path else Image.open('logo2.png')
        
        # Resize logos
        logo_size = (int(img.width * 0.12), int(img.height * 0.12))  
        logo1 = logo1.resize(logo_size, Image.LANCZOS)
        logo2 = logo2.resize(logo_size, Image.LANCZOS)
        
        margin = 25 
        logo1_position = (margin, margin)
        logo2_position = (img.width - logo_size[0] - margin, margin)
        
        img.paste(logo1, logo1_position, logo1)
        img.paste(logo2, logo2_position, logo2)
        
        draw = ImageDraw.Draw(img)
        
        font_large = ImageFont.truetype(font_large_path, 60) if font_large_path else ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype(font_small_path, 35) if font_small_path else ImageFont.truetype("arial.ttf", 35)
        
        text_large = large_text if large_text else "MyComp Society"
        text_small = small_text if small_text else "wishes you"
        
        # Calculate text sizes
        text_large_bbox = draw.textbbox((0, 0), text_large, font=font_large)
        text_large_width = text_large_bbox[2] - text_large_bbox[0]
        text_large_height = text_large_bbox[3] - text_large_bbox[1]
        
        text_small_bbox = draw.textbbox((0, 0), text_small, font=font_small)
        text_small_width = text_small_bbox[2] - text_small_bbox[0]
        text_small_height = text_small_bbox[3] - text_small_bbox[1]
        
        # Calculate the positions for the texts
        text_center_x = (logo1_position[0] + logo_size[0] + logo2_position[0]) // 2
        
        # Position text_large and text_small
        text_large_x = text_center_x - text_large_width // 2
        text_large_y = logo1_position[1] + (logo_size[1] - text_large_height) // 2
        
        text_small_x = text_center_x - text_small_width // 2
        text_small_y = text_large_y + text_large_height + 10  # Add spacing between large and small text
        
        # Draw the text with the selected colors
        draw.text((text_large_x, text_large_y), text_large, font=font_large, fill=large_text_color)
        draw.text((text_small_x, text_small_y), text_small, font=font_small, fill=small_text_color)
        
        img.save(new_image_path, 'PNG')
    
    status_label.config(text="Poster generated successfully!")
    return new_image_path

def update_image_on_gui(image_path, img_label, status_label):
    if image_path:
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        img_label.configure(image=img)
        img_label.image = img
    else:
        status_label.config(text="Failed to generate poster. Please try again.")

def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def select_color(entry):
    color = colorchooser.askcolor()[1]
    if color:
        entry.delete(0, tk.END)
        entry.insert(0, color)

# GUI setup
root = tk.Tk()
root.title("Poster Generator")
root.geometry("600x800")

# Apply the Sun Valley theme using sv-ttk
sv_ttk.set_theme("dark")

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=20)

ttk.Label(input_frame, text="Prompt:").grid(row=0, column=0, sticky=tk.W, pady=5)
prompt_entry = ttk.Entry(input_frame, width=40)
prompt_entry.grid(row=0, column=1, pady=5)

ttk.Label(input_frame, text="Logo 1:").grid(row=1, column=0, sticky=tk.W, pady=5)
logo1_entry = ttk.Entry(input_frame, width=40)
logo1_entry.grid(row=1, column=1, pady=5)
logo1_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(logo1_entry))
logo1_button.grid(row=1, column=2, padx=5)

ttk.Label(input_frame, text="Logo 2:").grid(row=2, column=0, sticky=tk.W, pady=5)
logo2_entry = ttk.Entry(input_frame, width=40)
logo2_entry.grid(row=2, column=1, pady=5)
logo2_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(logo2_entry))
logo2_button.grid(row=2, column=2, padx=5)

ttk.Label(input_frame, text="Font (Large Text):").grid(row=3, column=0, sticky=tk.W, pady=5)
font_large_entry = ttk.Entry(input_frame, width=40)
font_large_entry.grid(row=3, column=1, pady=5)
font_large_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(font_large_entry))
font_large_button.grid(row=3, column=2, padx=5)

ttk.Label(input_frame, text="Font (Small Text):").grid(row=4, column=0, sticky=tk.W, pady=5)
font_small_entry = ttk.Entry(input_frame, width=40)
font_small_entry.grid(row=4, column=1, pady=5)
font_small_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(font_small_entry))
font_small_button.grid(row=4, column=2, padx=5)

ttk.Label(input_frame, text="Large Text:").grid(row=5, column=0, sticky=tk.W, pady=5)
large_text_entry = ttk.Entry(input_frame, width=40)
large_text_entry.grid(row=5, column=1, pady=5)

ttk.Label(input_frame, text="Small Text:").grid(row=6, column=0, sticky=tk.W, pady=5)
small_text_entry = ttk.Entry(input_frame, width=40)
small_text_entry.grid(row=6, column=1, pady=5)

# Color selection
ttk.Label(input_frame, text="Large Text Color:").grid(row=7, column=0, sticky=tk.W, pady=5)
large_text_color_entry = ttk.Entry(input_frame, width=40)
large_text_color_entry.grid(row=7, column=1, pady=5)
large_text_color_button = ttk.Button(input_frame, text="Choose Color", command=lambda: select_color(large_text_color_entry))
large_text_color_button.grid(row=7, column=2, padx=5)

ttk.Label(input_frame, text="Small Text Color:").grid(row=8, column=0, sticky=tk.W, pady=5)
small_text_color_entry = ttk.Entry(input_frame, width=40)
small_text_color_entry.grid(row=8, column=1, pady=5)
small_text_color_button = ttk.Button(input_frame, text="Choose Color", command=lambda: select_color(small_text_color_entry))
small_text_color_button.grid(row=8, column=2, padx=5)

status_label = ttk.Label(root, text="")
status_label.pack(pady=5)

# Image display
img_label = ttk.Label(root)
img_label.pack(pady=20)

# Button to generate the poster
generate_button = ttk.Button(root, text="Generate Poster", command=lambda: update_image_on_gui(
    generate_image(
        prompt_entry.get(),
        logo1_entry.get(),
        logo2_entry.get(),
        font_large_entry.get(),
        font_small_entry.get(),
        large_text_entry.get(),
        small_text_entry.get(),
        large_text_color_entry.get(),
        small_text_color_entry.get(),
        status_label
    ),
    img_label,
    status_label
))
generate_button.pack(pady=10)

root.mainloop()
