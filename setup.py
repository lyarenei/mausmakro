import setuptools

setuptools.setup(
    name='mausmakro',
    version='0.2.1',
    description='Mouse macro player for automating various tasks.',
    url='https://github.com/lyarenei/mausmakro',
    author='Dominik Krivohlavek',
    author_email='domkrivohlavek@gmail.com',
    license='None',
    packages=setuptools.find_packages(exclude=['tests', 'examples', 'doc']),
    install_requires=[
        'lark',
        'pyautogui',
        'pynput',
        'click',
        'Pillow',
        'opencv-python',
    ],
    python_requires=">=3.7",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'mausmakro=mausmakro.__main__:main',
        ],
    },
)
