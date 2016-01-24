from distutils.core import setup

setup(
    name='beertools',
    version='0.1.2',
    author='Atle Frenvik Sveen',
    author_email='atle@frenviksveen.net',
    packages=['beertools', 'beertools.tests', 'beertools.util'],
    package_data={
        'beertools': ['brewery_misspellings.json']
    },
    scripts=[
        'bin/read_pol_beers.py',
        'bin/read_ratebeer_beers.py',
        'bin/read_ratebeer_breweries.py'
    ],
    url='https://github.com/atlefren/beertools/',
    license='LICENSE',
    description='Utils for working with beer data',
    install_requires=[
        'Unidecode==0.04.18',
        'argparse==1.2.1',
        'python-Levenshtein==0.12.0',
        'requests==2.8.1',
        'wsgiref==0.1.2',
        'beautifulsoup4==4.4.1',
        'pytz==2015.7'
    ],
)
