# git-bob

git-bob is Python package that uses AI to answer github-issues and review pull-requests. 
Under the hood it uses [claude](https://claude.ai) to understand the text and 
[pygithub](https://github.com/PyGithub/PyGithub) to interact with the issues and pull-requests.

## Installation as github action

To use git-bob in your github repository, you need to 
* setup github workflows like shown in [this folder](.github/workflows). Make sure to replace `pip install -e .` with a specific git-bob version such as `pip install git-bob==0.1.0`.
* configure a github secret called "ANTHROPIC_API_KEY" with your API key for [claude](https://claude.ai).
* configure github actions to run the workflow on issues and pull-requests. Also give write-access to the action runner.

To trigger git-bob, you need to comment on an issue or pull-request with the following commands:

```
git-bob comment
```

## Installation as command-line tool

You can also install git-bob locally and run it from the terminal. 
In this case, create a github token and store it in an environment variable named `GITHUB_API_KEY`. 
Then you can run git-bob like this:

```bash
pip install git-bob
```

## Usage as command-line tool

You can use git-bob from the terminal on repositories you have read/write access to.

```bash
git_bob <action> <organization>/<repository> <issue-number>
```

Available actions:
* `review-pull-request`
* `comment-on-issue`

## Similar projects

There are similar projects out there
* [Claude Engineer](https://github.com/Doriandarko/claude-engineer)
* [BioChatter](https://github.com/biocypher/biochatter)
* [aider](https://github.com/paul-gauthier/aider)
* [OpenDevin](https://github.com/OpenDevin/OpenDevin)
* [Devika](https://github.com/stitionai/devika)
* [GPT-Codemaster](https://github.com/dex3r/GPT-Codemaster)

## Contributing

Feedback and contributions are welcome! Just open an issue and let's discuss before you send a pull-request. 
A [human](https://haesleinhuepf.github.io) will respond and comment on your ideas!
