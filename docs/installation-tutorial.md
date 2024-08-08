# git-bob Installation Tutorial

In this tutorial, we will install `git-bob` in the `stackview` repository to demonstrate all steps necessary for this.
Afterwards, `git-bob` can use AI to help developing `stackview`.

## Step 1: github workflows.

The first step is to copy over the github workflows from the `git-bob` repository to the `stackview` repository.
It is recommended to do this change on a git-branch. We can then test this, before we submit the changes.
We only adapt one thing, we replace this line:

```
pip install -e .
```

by this one:

```
pip install git-bob==0.2.2
```

You can see the full [git commit here](https://github.com/haesleinhuepf/stackview/commit/a5542352b2f2dd7e2cfbff32280ae8cec0015458).

## Step 2: Creating an OpenAI API Key

We navigate to the [openai API website](https://openai.com/index/openai-api/) and log in.

You find the [API Key page](https://platform.openai.com/api-keys) by clicking on `Dashbord` and `API Keys`.

![img.png](images/install/img.png)

Click on `Create new secret key` and enter a meaningful name.

![img_1.png](images/install/img_1.png)

Copy the key from this text field:

![img_2.png](images/install/img_2.png)

And navigate to the repository on github 

```
https://github.com/<GITHUB ORGANIZATION>/<REPOSITORY>/settings/secrets/actions
```

In our case, we navigate to `stackview`:
```
https://github.com/haesleinhuepf/stackview/settings/secrets/actions
```

Click on `New repository secret` 

![img_3.png](images/install/img_3.png)

Enter the key name `OPENAI_API_KEY` and paste the key into the value field.

![img_4.png](images/install/img_4.png)

In the menu on the right, under Actions / General, give read and write permissions to the Workflows using the `GITHUB_TOKEN` and allow github actions to create and merge pull-requests.

![img.png](images/install/img4a.png)

## Step 3 (optional):

Go back to the OpenAI API website and set a limit for the API key. With this you can make sure that the usage does not spend to much money:

![img_5.png](images/install/img_5.png)

![img_6.png](images/install/img_6.png)

## Step 4: Testing the installation

Next, we navigate to the github repository and submit our changes as pull-request.

![img_7.png](images/install/img_7.png)

In this pull-request, enter `git-bob comment` and it will review the pull-request in the new repository:

![img_8.png](images/install/img_8.png)

Wait a second and this box should appear indicating that the git-bob github action is running:

![img_9.png](images/install/img_9.png)

If the installation works, another box will appear after a minute with a review from git-bob:

![img_10.png](images/install/img_10.png)

After merging this pull-request, you can continue asking `git-bob comment` in all pull-requests and issues in the repository.

In case of any issues while installing, please mention `@haesleinhuepf`.
