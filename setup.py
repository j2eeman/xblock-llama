from setuptools import setup, find_packages

setup(
    name='xblock-llama',
    version='0.1.0',
    description='Llama XBlock',
    packages=find_packages(),
    include_package_data=True,  # This is crucial!
    package_data={
        'xblock_llama': ['xblock_llama/templates/*.html', 'xblock_llama/static/css/*.css', 'xblock_llama/static/js/*.js'],
    },
    install_requires=[
        'xblock',
        'requests',  # 添加 requests 依赖
    ],
    entry_points={
        'xblock.v1': [
            'xblock_llama = xblock_llama.xblock_llama:LlamaXBlock',
        ]
    },
)