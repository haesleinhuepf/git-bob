#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    entry_points={
        'git_bob.prompt_handlers': [
            'gpt = git_bob._endpoints:prompt_chatgpt',
            'claude = git_bob._endpoints:prompt_anthropic',
            'starcoder = git_bob._endpoints:prompt_huggingface',
        ],
    }
)
