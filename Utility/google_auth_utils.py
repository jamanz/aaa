from kivy.utils import platform

if platform == "android":

    def stop_login(*args):
        pass


class LoginProviders:
    google = "google"
    facebook = "facebook"
    github = "github"
    twitter = "twitter"


login_providers = LoginProviders()


def auto_login(provider):
    """
    Auto login using a given provider. You may call it `on_start`.
    :param: `provider` is one of `kivyauth.login_providers`
    """
    if platform == "android":
        if provider == login_providers.google:
            from Utility.google_auth import auto_google
            return auto_google()
    else:
        raise NotImplementedError("Not yet availabe for desktop")