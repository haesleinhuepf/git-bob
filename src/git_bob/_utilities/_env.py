SENSIBLE_ENV_KEYS = ["ANTHROPIC_API_KEY",
                    "GOOGLE_API_KEY",
                    "OPENAI_API_KEY",
                    "GH_MODELS_API_KEY",
                    "MISTRAL_API_KEY",
                    "KISSKI_API_KEY",
                    "BLABLADOR_API_KEY",
                    "GITHUB_API_KEY",
                    "GITLAB_API_KEY",
                    "TWINE_USERNAME",
                    "TWINE_PASSWORD",
                    "HF_TOKEN",
                    "DEEPSEEK_API_KEY",
                    "CODECOV_TOKEN"]

def save_and_clear_environment():
    """Clear all environment variables and store the entire env in a dictionary for restoration later"""
    import os
    # Save the current environment
    saved_env = dict(os.environ)

    # Clear all environment variables
    for key in list(os.environ.keys()):
        if key in SENSIBLE_ENV_KEYS or \
            "password" in key.lower() or \
            "username" in key.lower() or \
            "key" in key.lower():
            del os.environ[key]

    return saved_env


def restore_environment(saved_env):
    """Restore an environment that was saved with save_and_clear_environment"""
    import os
    # Clear current environment
    for key in list(os.environ.keys()):
        del os.environ[key]

    # Restore saved environment
    os.environ.update(saved_env)