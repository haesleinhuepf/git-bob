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

## Example for-loop in Python

Here is a simple example of a for-loop that outputs numbers between 0 and 10:

```python
for i in range(11):
    print(i)
```

## Disclaimer

`git-bob` is a research project aiming at streamlining GitHub interaction in software development projects. Under the hood it uses
artificial intelligence / large language models to generate text and code fulfilling the user's requests. 
Users are responsible to verify the generated code according to good scientific practice.

When using `git-bob` you configure it to use an API key to access the AI models. 
You have to pay for the usage and must be careful in using the software.
Do not use this technology if you are not aware of the costs and consequences.

> [!CAUTION]
> When using the Anthropic, OpenAI, Google Gemini, Mistral or any other endpoint via git-bob, you are bound to the terms of service 
> of the respective companies or organizations.
> The GitHub issues, pull requests and messages you enter are transferred to their servers and may be processed and stored there. 
> Make sure to not submit any sensitive, confidential or personal data. Also using these services may cost money.

## Installation as GitHub action

There is a detailed [tutorial](https://github.com/haesleinhuepf/git-bob/blob/main/docs/installation-tutorial.md) on how to install git-bob as GitHub action to your repository. In very short, to use git-bob in your GitHub repository, you need to 
* Copy the [git-bob](https://github.com/haesleinhuepf/git-bob/blob/main/.github/workflows/git-bob.yml) GitHub workflow in folder `.github/workflows/` to your repository.
  * Make sure to replace `pip install -e .` with a specific git-bob version such as `pip install git-bob==0.16.0`.
  * Configure the LLM you want to use in the workflow files by specifying the `GIT_BOB_LLM_NAME` environment variable. These were tested:
    * `claude-3-5-sonnet-20241022`
    * `gpt-4o-2024-08-06`
    * `github_models:gpt-4o`
    * `github_models:meta-llama-3.1-405b-instruct`
    * `gemini-1.5-pro-002`
    * `mistral-large-2411` (uses `pixtral-12b-2409` for vision tasks)
    * `deepseek-chat`
  * configure a GitHub secret with the corresponding key from the LLM provider depending on the above configured LLM:
    * `OPENAI_API_KEY`: [OpenAI (gpt)](https://openai.com/blog/openai-api)
    * `ANTHROPIC_API_KEY`: [Anthropic (claude)](https://www.anthropic.com/api)
    * `GH_MODELS_API_KEY`: [GitHub Models Marketplace](https://github.com/marketplace/models)
    * `GOOGLE_API_KEY`: [Google AI](https://ai.google.dev/gemini-api/docs/api-key)
    * `MISTRAL_API_KEY`: [Mistral](https://console.mistral.ai/api-keys/)
    * `DEEPSEEK_API_KEY`: [DeepSeek](https://platform.deepseek.com/api_keys)
    * `KISSKI_API_KEY`: [KISSKI](https://services.kisski.de/services/en/service/?service=2-02-llm-service.json)
    * `BLABLADOR_API_KEY`: [BLABLADOR](https://login.helmholtz.de/oauth2-as/oauth2-authz-web-entry)
  * configure GitHub actions to run the workflow on issues and pull requests. Also give write-access to the Workflow using the `GITHUB_TOKEN`.

When using it in your repository, you can also set a custom system message, for example for:
* [General Data Science / Python Programming](https://github.com/haesleinhuepf/git-bob-playground/blob/bf08b3526980e011f632c13f29ae65372aafa5c7/.github/workflows/git-bob.yml#L75)
* [Bio-Image Analysis](https://github.com/haesleinhuepf/git-bob-bioimage-analysis-example/blob/main/.github/workflows/git-bob.yml#L75)
* [Giving advice on a specific repository / library](https://github.com/haesleinhuepf/stackview/blob/afc662a71a39f298af9f183c06c3d37c95cc2015/.github/workflows/git-bob.yml#L58)
* [Manuscript writing](https://github.com/haesleinhuepf/git-bob-manuscript/blob/49659f8a41854d4da696259e7c1316af2fc7c171/.github/workflows/comment-on-issue.yml#L49)

Furthermore, to guide discussions, you may want to setup issue templates, e.g.
* [General Python Programming Questions](https://github.com/haesleinhuepf/git-bob-playground/blob/main/.github/ISSUE_TEMPLATE/programming.md)
* [Bio-Image Analysis](https://github.com/haesleinhuepf/git-bob-playground/blob/main/.github/ISSUE_TEMPLATE/bioimage_analysis.md)
* [Statistics and Plotting](https://github.com/haesleinhuepf/git-bob-playground/blob/main/.github/ISSUE_TEMPLATE/statistics_plotting.md)

## Installation as gitlab pipeline

Since version 0.10.1 git-bob has experimental support for [gitlab](https://gitlab.com). You find detailed instructions how to install it [here](https://github.com/haesleinhuepf/git-bob/blob/main/docs/installation-tutorial-gitlab.md).

## Usage: Trigger words

To trigger git-bob, you need to comment on an issue or pull request with the `comment` trigger word (or aliases `think about`, `review`, `respond`):

```
git-bob comment
```

If you want to ask git-bob for a review of a pull-request, you can use the `review` trigger word. Also make sure mention explictly what you want to be reviewed.

```
git-bob review this PR. Check code quality and comments.
```

After some back-and-forth discussion, you can also use the `solve` trigger word (or aliases `implement`, `apply`) make git-bob solve an issue and send a pull-request. 
This trigger can also be used to modify code in pull requests.

```
git-bob solve
```

You can ask git-bob to implement a solution for testing, without sending a pull-request, using the `try` trigger:
```
git-bob try
```

If you have multiple API-Key for different LLMs configured, you can specify the LLM in the command using the `ask <LLM-Name> to` trigger command:

```
git-bob ask claude-3-5-sonnet-20241022 to solve this issue.
```

If the issue is complex and should be split into sub-issues, you can use the following command:

```
git-bob split
```

If you have two GitHub secrets `TWINE_USERNAME` and `TWINE_PASSWORD` configured, you can also use the following command to publish a new version of your library to PyPI:

```
git-bob deploy
```

All trigger words can be combined with `please` and/or `,`, which will make no difference to calling git-bob without these words:

```
git-bob, please ask gemini-1.5-pro-002 to solve this issue.
```

## Recommended Workflow

Here's the recommended workflow for using git-bob:

1. Create an issue describing the problem or task.
2. Comment on the issue with `git-bob comment`, or `git-bob think about this` (an alias for `comment`) to trigger git-bob making a plan.
3. Respond to git-bob with any clarifications or additional information it requests.
4. Comment on the issue with `git-bob solve` or `git-bob implement this` (an alias for `solve`) to trigger git-bob.
5. Wait for git-bob to create a pull request (PR) addressing the issue.
6. Review the PR and comment on the PR or on the original issue if changes are needed.
7. Wait for git-bob to create new PR or modifying the existing PR with the requested changes.
8. Repeat steps 3-5 as necessary until the issue is resolved satisfactorily.

## Use-case examples

A huge variety of use-cases for git-bob are thinkable. Here are some examples. Many serve purely demonstrative purposes. 
Some were parts of real scientific data analysis projects.

* Question answering 
  * [About specific Python libraries](https://github.com/haesleinhuepf/stackview/issues/79)
  * [The capital of France](https://github.com/haesleinhuepf/git-bob-playground/issues/24)
* Translation
  * [Translating text in Jupyter notebooks in other Languages](https://github.com/haesleinhuepf/git-bob-playground/issues/118) 
* Bio-image Analysis
  * [Nuclei segmentation](https://github.com/haesleinhuepf/git-bob-playground/issues/13)
  * [Cell segmentation](https://github.com/haesleinhuepf/git-bob-playground/issues/42)
  * [Resizing images](https://github.com/NFDI4BIOIMAGE/training/issues/356)
* Programming
  * [Caching](https://github.com/NFDI4BIOIMAGE/SlideInsight/issues/28)
  * [Fixing bugs in notebooks](https://github.com/haesleinhuepf/git-bob-playground/issues/174)
  * [Summarize code of a file](https://github.com/haesleinhuepf/git-bob-playground/issues/178)
  * [Summarize code in a repository](https://github.com/haesleinhuepf/git-bob/issues/445)
  * [Programming Google Search](https://github.com/haesleinhuepf/git-bob-playground/issues/193)
  * [Implementing a generic Factory patters](https://github.com/haesleinhuepf/git-bob-playground/issues/198)
* Prompting
  * [Prompting for SVG files](https://github.com/haesleinhuepf/git-bob-playground/issues/184)
* Continuous Integration and Deployment
  * [Configuring Github workflows](https://github.com/haesleinhuepf/git-bob-playground/issues/146)
  * [Configuring a Jupyter Book](https://github.com/NFDI4BIOIMAGE/training/issues/381)
* Data & Code Management
  * [Write a Data Management Plan (DMP)](https://github.com/haesleinhuepf/git-bob-playground/issues/180)
  * [Research Data Management & Folder Structures](https://github.com/haesleinhuepf/git-bob-playground/issues/45)
  * [Documenting source code](https://github.com/haesleinhuepf/git-bob/pull/29)
  * [Determining licenses of dependencies](https://github.com/haesleinhuepf/git-bob-playground/issues/101)
  * [Assisting scientific manuscript writing](https://github.com/haesleinhuepf/git-bob-manuscript/pull/9)
  * [Deleting files](https://github.com/haesleinhuepf/git-bob/issues/412)
  * [Converting tables to key-value pairs](https://github.com/haesleinhuepf/git-bob-playground/issues/103)
  * [Exporting Google Scholar profile as bibtex](https://github.com/haesleinhuepf/git-bob-playground/issues/114)
  * [Deciding for file formats: JSON versus YAML](https://github.com/haesleinhuepf/git-bob-playground/issues/117)
  * [Generating Galaxy workflows](https://github.com/haesleinhuepf/git-bob-playground/issues/123)
  * [Count citations of given DOIs](https://github.com/haesleinhuepf/git-bob-playground/issues/141)
  * [Convert PDF documents to PNG images](https://github.com/haesleinhuepf/git-bob-playground/issues/179)
  * [Convert PDF documents to animated GIFs](https://github.com/haesleinhuepf/git-bob-playground/issues/204)
  * [Convert SVG files to PNG images](https://github.com/haesleinhuepf/git-bob-playground/issues/216)
  * [Querying the arxiv](https://github.com/haesleinhuepf/git-bob-playground/issues/197)
  * [Retrieving meta-data of arxiv articles](https://github.com/haesleinhuepf/git-bob-playground/issues/196)
* Graphical User Interfaces
  * [Interactive drawing on an ipcanvas](https://github.com/haesleinhuepf/git-bob-playground/issues/121) 
* Statistics
  * [Filtering data and counting records](https://github.com/NFDI4BIOIMAGE/training/issues/299)
  * [Selecting ranges of columns](https://github.com/haesleinhuepf/git-bob-playground/issues/47)
  * [Summarizing data and plotting](https://github.com/NFDI4BIOIMAGE/training/issues/250)
  * [Writing text about well-known statistical methods](https://github.com/haesleinhuepf/git-bob-playground/issues/161)
* Plotting
  * [Violing plots with simulated data](https://github.com/haesleinhuepf/git-bob-playground/issues/44)
  * [UMAPs with simulated data](https://github.com/haesleinhuepf/git-bob-playground/issues/41)
  * [Plotting a circle of triangles (in gitlab)](https://gitlab.com/haesleinhuepf/git-bob-gitlab-playground/-/issues/8)
  * [Pairplots with simulated data](https://github.com/haesleinhuepf/git-bob-playground/issues/48)
  * [Word clouds](https://github.com/haesleinhuepf/git-bob-playground/issues/76)
  * [Plot simulated income data](https://github.com/haesleinhuepf/git-bob-playground/issues/195)
  * [Ploting the Dunning Kruger effect](https://github.com/haesleinhuepf/git-bob-playground/issues/202)
* Science Communication
  * [Making slides for Deep Learning training](https://github.com/haesleinhuepf/git-bob-playground/issues/97)
  * [Making slides for Research Data Management training](https://github.com/haesleinhuepf/git-bob-playground/issues/96)
  * [Visualizing how Fourier-Transform works](https://github.com/haesleinhuepf/git-bob-playground/issues/22)
  * [Making Jupyter Notebooks for training](https://github.com/haesleinhuepf/git-bob-playground/issues/92)
  * [Making slides about text](https://github.com/haesleinhuepf/git-bob-playground/issues/98)
  * [Visualizing processes using CPUs and GPUs](https://github.com/haesleinhuepf/git-bob-playground/issues/192)
* Fun
  * [Playing Tic-Tac-Toe](https://github.com/haesleinhuepf/git-bob-playground/issues/91)
  * [Story Telling for kids](https://github.com/haesleinhuepf/git-bob-playground/issues/82)
  * [PowerPoint Karaoke](https://github.com/haesleinhuepf/git-bob-playground/issues/99)
  * [Solving Advent of Code 2024 puzzles](https://github.com/haesleinhuepf/git-bob-advent-of-code)
  * [Solving the Halting Problem](https://github.com/haesleinhuepf/git-bob-playground/issues/156) [[2nd attempt](https://github.com/haesleinhuepf/git-bob-playground/issues/157)]
  * [Drawing a Christmas tree as SVG](https://github.com/haesleinhuepf/git-bob-playground/issues/188)
* Things that didn't work well
  * [How to use aider from python](https://github.com/haesleinhuepf/git-bob/issues/437#issuecomment-2539865080)
  * [How to use the atproto API](https://github.com/haesleinhuepf/git-bob-playground/issues/136)
  * [Executing code in a sandbox](https://github.com/haesleinhuepf/git-bob-playground/issues/177)
