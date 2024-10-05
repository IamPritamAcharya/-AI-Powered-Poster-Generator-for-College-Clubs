# Poster Generation Automation Tool

**Project Overview:**

This project leverages advanced neural network models and GUI technologies to automate the generation of high-quality, customizable posters. The goal is to streamline the design process, allowing users—particularly those without design expertise—to create visually appealing posters efficiently.

## 🛠️ Tools and Technologies

- **Python**: The primary programming language used for the implementation.
- **Tkinter**: A standard GUI toolkit for Python, used for creating the user interface.
- **Pillow**: A Python Imaging Library that adds image processing capabilities.
- **Gradio Client**: For easy interface creation and integration with machine learning models.
- **SV TTK**: A themed widget toolkit that enhances the appearance of the GUI.
- **FLUX.1 Schnell**: An advanced model from black-forest-labs used for automating poster generation.
- **Hugging Face**: Utilized for accessing and deploying machine learning models.

## 🚀 Key Features

- **Automated Poster Generation**: Utilizes the FLUX.1 Schnell model to reduce design time by **85%**, automating the creation of visually appealing posters.
- **Customizable Posters**: Users can create high-resolution posters based on their specific prompts, incorporating event details and branding elements.
- **Dynamic Customizations**: The tool enables users to customize logos, fonts, and colors through an intuitive interface, enhancing the personalization of each poster.
- **User-Friendly GUI**: Designed for non-designers, the graphical interface streamlines the poster creation process, improving marketing efficiency and accessibility.

## 📥 Installation

To install the necessary libraries, you can use the following command:
```bash
pip install tkinter pillow gradio sv-ttk
```
For the `FLUX.1 Schnell` model, follow the documentation on [Hugging Face](https://huggingface.co/) for setup instructions.

## 🎨 Usage

1. **Run the Application**:
   ```bash
   python gui.py
   ```

2. **Input Your Event Details**:
   Fill in the necessary details such as event name, date, and any specific branding requirements.

3. **Customize Your Poster**:
   Use the intuitive GUI to select logos, fonts, and colors according to your preferences.

4. **Generate and Download**:
   Click the "Generate" button to create your poster. Once satisfied, download it for distribution.

## 📅 Development Timeline

- **Month 1**: Research and development of the FLUX.1 Schnell model integration.
- **Month 2**: GUI design and implementation using Tkinter.

## 🤝 Contributing

If you'd like to contribute to the project, please fork the repository and submit a pull request. Any suggestions for improvements or features are welcome!

## 🌟 Acknowledgments

- Special thanks to [black-forest-labs](https://huggingface.co/black-forest-labs/FLUX.1-schnell) for providing the FLUX.1 Schnell model.
