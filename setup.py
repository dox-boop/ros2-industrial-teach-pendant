from setuptools import find_packages, setup

package_name = 'pendant_demo'

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
    maintainer='daksh',
    maintainer_email='daksh@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
	entry_points={
    		'console_scripts': [
        		'pendant_node = pendant_demo.pendant_node:main',
			'controller_node = pendant_demo.controller_node:main',
			'home_client =  pendant_demo.home_client:main',
			'status_monitor = pendant_demo.status_monitor:main',
			'teach_pendant = pendant_demo.teach_pendant:main',
			'move_action_server = pendant_demo.move_action_server:main',
			'gui_pendant = pendant_demo.gui_pendant:main',
			'joint_state_controller = pendant_demo.joint_state_controller:main',
   	 	],
	},
)
