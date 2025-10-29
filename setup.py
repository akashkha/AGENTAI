from setuptools import setup, find_packages

setup(
    name="interview_bot",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.28.1",
        "python-dateutil>=2.8.2",
        "Pillow>=9.5.0",
        "json5==0.9.14",
    ],
    package_data={
        'interview_bot': ['questions_db.json'],
    },
)