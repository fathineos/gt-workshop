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
        'Django==6.0.3',
        'django-baton==5.1.2',
        'gunicorn==25.2.0',
        'ipython==9.11.0',
    ],
    python_requires='>=3.12.0'
)
