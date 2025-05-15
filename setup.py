from setuptools import find_packages, setup

package_name = 'ros2_course'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zsombor',
    maintainer_email='korbzsombor@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = ros2_course.talker:main',
            'hello = ros2_course.hello:main',
            'fractal_drawer = ros2_course.fractal_drawer:main',
            'pyramid = ros2_course.pyramid:main'
            'drawtree = ros2_course.draw_tree:main',
        ],
    },
)
