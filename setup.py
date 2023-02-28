from setuptools import find_packages, setup

import versioneer

setup(
    name="gt-workshop",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="GT-Workshop",
    author="Fotis Athineos",
    author_email="fotis.athineos@protonmail.com",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=[
        'Django==3.2.18',
        'django-baton==2.6.2',
        'gunicorn==20.1.0',
        'ipython==8.10.0',
    ],
    python_requires='>=3.8.0'
)
