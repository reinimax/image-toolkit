import shutil

def copy_screenshot(*args, **kwargs):
    shutil.copy("screenshot.png", "mk-docs/screenshot.png")
