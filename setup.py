from setuptools import find_packages, setup
import os   # OSの機能を使うためのモジュール
from glob import glob   # フォルダ内のファイルを探すためのモジュール

package_name = 'ic120_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ryoya SATO',
    maintainer_email='satoryoya1012711@gmail.com',
    description='ic120 teleop node',
    license='Apach-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ic120_teleop_node = ic120_teleop.ic120_teleop_node:main',
        ],
    },
)
