from setuptools import setup, find_packages

setup(
    name='xblock-llama',
    version='0.1.0',
    description='Llama XBlock',
    packages=find_packages(),
    install_requires=[
        'xblock',
        'requests',  # 添加 requests 依赖
    ],
    entry_points={
        'xblock.v1': [
            'llama = xblock_llama:LlamaXBlock',
        ]
    },
)