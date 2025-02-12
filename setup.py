from setuptools import setup, find_packages

standalone = ['ch=gemelli.scripts.__init__:cli']
q2cmds = ['q2-gemelli=gemelli.q2.plugin_setup:plugin']

setup(
    name='convexhull2',
    version='0.1.0',
    packages=find_packages(),
    # entry_points={
    #     'console_scripts': [
    #         'my-command = my_package.my_script:main',  # "my-command" is the command you'll use in the CLI
    #     ],
    # },

    entry_points={
        'qiime2.plugins': ['q2-convexhull2=ch.q2.plugin_setup:plugin'],
        # 'console_scripts': ['q2-convexhull2=q2-convexhull2']
    },
    author='Daniela Perry',
    author_email='dsperry@ucsd.edu',
    description='New plotting functionality with convex hull calculations',
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'skbio',
        'matplotlib',
        'seaborn',
        'biom-format',
    ],

)