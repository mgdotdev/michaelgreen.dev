from setuptools import setup, find_packages

def read_requirements(requirements_file_path):
    """Retrun dependencies from a requirements file as a list.

    Read requirements '.in' or '.txt' file where dependencies are separated by a new line,
    removes all comments and options for pip, and return as a list of dependencies.
    """
    with open(requirements_file_path, 'r') as f:
        data = f.readlines()
    data = [i[: i.find("#")] if "#" in i else i for i in data]
    data = [i.strip() for i in data if i.strip()]
    data = [i for i in data if not i.startswith("-")]
    return data

setup(
    name='api',
    packages=find_packages(where="src"),
    package_data={"": ['*.json']},
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
    zip_safe=False,
)