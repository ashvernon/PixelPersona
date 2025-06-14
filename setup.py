from setuptools import setup

setup(
    name='PixelPersona',
    version='0.1.0',
    description='Pixel Persona sprite generation toolkit',
    py_modules=['main'],
    install_requires=['Pillow', 'tk'],
    scripts=['main.py'],
)
