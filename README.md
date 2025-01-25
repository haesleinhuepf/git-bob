# git-bob ![](logo_32x32.png)
[![PyPI](https://img.shields.io/pypi/v/git-bob.svg?color=green)](https://pypi.org/project/git-bob)
[![DOI](https://zenodo.org/badge/831841421.svg)](https://doi.org/10.5281/zenodo.13970719)
[![License](https://img.shields.io/pypi/l/git-bob.svg?color=green)](https://github.com/haesleinhuepf/git-bob/raw/main/LICENSE)
<!--[![PyPI - Downloads](https://img.shields.io/pypi/dm/git-bob)](https://pypistats.org/packages/git-bob)-->

git-bob uses AI to solve GitHub issues and review pull requests. It runs inside the GitHub CI, no need to install anything on your computer.
Read more in the [preprint](https://doi.org/10.5281/zenodo.13928832). 

![banner](https://github.com/haesleinhuepf/git-bob/raw/main/docs/images/banner2.png)

Under the hood it uses [Anthropic's Claude](https://www.anthropic.com/api) or [OpenAI's chatGPT](https://openai.com/blog/openai-api) or [Google's Gemini](https://blog.google/technology/ai/google-gemini-ai/) to understand the text and 
[pygithub](https://github.com/PyGithub/PyGithub) to interact with the issues and pull requests. As its discussions are conserved, you can document how things were done using AI and 
others can learn how to prompt for the things you did. For example, the pair-plot discussion above is [available online](https://github.com/haesleinhuepf/git-bob-playground/issues/48).

## Disclaimer

[Rest of the README.md content remains exactly the same...]
