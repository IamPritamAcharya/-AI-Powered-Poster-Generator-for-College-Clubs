import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from gradio_client import Client
import sv_ttk


# Set up your Hugging Face token
os.environ['HF_TOKEN'] = ''

# Initialize Gradio client
client = Client("black-forest-labs/FLUX.1-schnell")

# Function to generate the poster
def generate_image(prompt_user, logo1_path, logo2_path, font_large_path, font_small_path, large_text, small_text, status_label):
    prompt = f"{prompt_user} poster, add event greeting at center"
    
    # Create folder to save the image
    folder_path = os.path.join(os.getcwd(), 'image_gen')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Delete existing images in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            os.remove(os.path.join(folder_path, filename))
    
    status_label.config(text="Generating poster...")
    
    try:
        # Generate the image using Gradio
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
            
            font_large = ImageFont.truetype(font_large_path, 60) if font_large_path else ImageFont.truetype("GoogleSans-Regular.ttf", 60)
            font_small = ImageFont.truetype(font_small_path, 35) if font_small_path else ImageFont.truetype("GoogleSans-Regular.ttf", 35)
            
            text_large = large_text if large_text else "MyComp Society"
            text_small = small_text if small_text else "wishes you"
            
            text_large_width, text_large_height = draw.textsize(text_large, font=font_large)
            text_small_width, text_small_height = draw.textsize(text_small, font=font_small)
            
            text_center_x = img.width // 2
            text_center_y = logo1_position[1] + logo_size[1] + ((img.height - (logo1_position[1] + logo_size[1])) // 2)

            text_large_x = text_center_x - (text_large_width // 2)
            text_small_x = text_center_x - (text_small_width // 2)
            text_large_y = text_center_y - (text_large_height + 10) // 2
            text_small_y = text_center_y + (10) // 2 
            
            draw.text((text_large_x, text_large_y), text_large, font=font_large, fill="yellow")
            draw.text((text_small_x, text_small_y), text_small, font=font_small, fill="yellow")
            
            img.save(new_image_path, 'PNG')
        
        status_label.config(text="Poster generated successfully!")
        return new_image_path
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        return None

def update_image_on_gui(image_path, img_label, status_label):
    if image_path:
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        img_label.configure(image=img)
        img_label.image = img
    else:
        status_label.config(text="Failed to generate poster. Please try again.")

def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def save_image(image_path):
    try:
        if image_path:
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            save_path = os.path.join(downloads_folder, 'generated_image.png')
            Image.open(image_path).save(save_path)
            messagebox.showinfo("Success", f"Image saved to {save_path}")
        else:
            messagebox.showwarning("Warning", "No image to save!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Poster Generator")
root.geometry("750x850")

# Apply the Sun Valley theme using sv-ttk
sv_ttk.set_theme("dark")

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=20, padx=20, fill=tk.X)

# Styling for entries and labels
style = ttk.Style()
style.configure("TLabel", background="#1C1C1C", foreground="#FFFFFF", font=("GoogleSans-Regular", 12))
style.configure("TButton", font=("GoogleSans-Regular", 10))
style.configure("RoundedFrame.TFrame", background="#1C1C1C", borderwidth=0)
style.configure("TEntry", font=("GoogleSans-Regular", 10))

# Prompt row
prompt_label = ttk.Label(input_frame, text="Prompt:")
prompt_label.grid(row=0, column=0, sticky=tk.W, pady=5)
prompt_entry = ttk.Entry(input_frame, width=30)
prompt_entry.grid(row=0, column=1, pady=5, columnspan=2)

# Logo 1 and Logo 2 row
logo1_label = ttk.Label(input_frame, text="Logo 1:")
logo1_label.grid(row=1, column=0, sticky=tk.W, pady=5)
logo1_entry = ttk.Entry(input_frame, width=18)
logo1_entry.grid(row=1, column=1, pady=5)
logo1_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(logo1_entry))
logo1_button.grid(row=1, column=2, padx=5)

logo2_label = ttk.Label(input_frame, text="Logo 2:")
logo2_label.grid(row=1, column=3, sticky=tk.W, pady=5)
logo2_entry = ttk.Entry(input_frame, width=18)
logo2_entry.grid(row=1, column=4, pady=5)
logo2_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(logo2_entry))
logo2_button.grid(row=1, column=5, padx=5)

# Font (Large Text) and Font (Small Text) row
font_large_label = ttk.Label(input_frame, text="Font (Large Text):")
font_large_label.grid(row=2, column=0, sticky=tk.W, pady=5)
font_large_entry = ttk.Entry(input_frame, width=18)
font_large_entry.grid(row=2, column=1, pady=5)
font_large_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(font_large_entry))
font_large_button.grid(row=2, column=2, padx=5)

font_small_label = ttk.Label(input_frame, text="Font (Small Text):")
font_small_label.grid(row=2, column=3, sticky=tk.W, pady=5)
font_small_entry = ttk.Entry(input_frame, width=18)
font_small_entry.grid(row=2, column=4, pady=5)
font_small_button = ttk.Button(input_frame, text="Browse", command=lambda: select_file(font_small_entry))
font_small_button.grid(row=2, column=5, padx=5)

# Large Text and Small Text row
large_text_label = ttk.Label(input_frame, text="Large Text:")
large_text_label.grid(row=3, column=0, sticky=tk.W, pady=5)
large_text_entry = ttk.Entry(input_frame, width=18)
large_text_entry.grid(row=3, column=1, pady=5)

small_text_label = ttk.Label(input_frame, text="Small Text:")
small_text_label.grid(row=3, column=3, sticky=tk.W, pady=5)
small_text_entry = ttk.Entry(input_frame, width=18)
small_text_entry.grid(row=3, column=4, pady=5)

status_label = ttk.Label(root, text="", background="#1C1C1C", foreground="#FFFFFF", font=("GoogleSans-Regular", 10))
status_label.pack(pady=10)

generate_button = ttk.Button(root, text="Generate Poster", command=lambda: update_image_on_gui(
    generate_image(prompt_entry.get(), logo1_entry.get(), logo2_entry.get(), font_large_entry.get(),
                   font_small_entry.get(), large_text_entry.get(), small_text_entry.get(), status_label),
    img_label, status_label
))
generate_button.pack(pady=10)

save_button = ttk.Button(root, text="Save Image", command=lambda: save_image(img_label.image))
save_button.pack(pady=10)

img_label = ttk.Label(root, background="#1C1C1C")
img_label.pack(pady=20)

root.mainloop()
