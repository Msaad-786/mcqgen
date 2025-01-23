#installing local package in my current Virtualenv
from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Muhammad Saad',
    author_email='m.saad44490@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)

