from setuptools import setup, find_packages
setup(
    name="Python-CICD",          # Package name
    version="0.1.0",                  # Version
    author="Kundan Singh",               # Author
    author_email="kundansingh0619@example.com",
    description="A Python CI/CD demo project", # Description
    #packages=find_packages(where="src"),
    #package_dir={"": "src"},
    packages=find_packages(),         # Automatically find Python packages
    install_requires=[                # Add dependencies here if any
        "SQLAlchemy>=2.0.19",
    ],
    python_requires=">=3.10",          # Python version requirement

    # CLI commands (optional)
    # entry_points={
    #     'console_scripts': [
    #         'your-command = your_package.module:main',
    #     ],
    # },

)