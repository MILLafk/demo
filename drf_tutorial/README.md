# drf_tutorial

## Setup

#. Install [Docker](https://docs.docker.com/engine/install/ubuntu/)

#. Configure Postgres 10 :
    .. code-block:: bash

        $ docker pull postgres:10
        $ docker run -p 5432:5432 --name pg-drf -e POSTGRES_PASSWORD=docker -e POSTGRES_DB=django_rf -d postgres:10
        $ docker ps

#. Make sure that [git lfs](https://git-lfs.github.com/) is installed on your environment.

        $ curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
        $ sudo apt-get update && sudo apt-get install -y git-lfs
        $ git lfs install
        $ git lfs pull

#. Setup Anaconda environment.

        $ conda create --name django_rf python=3.7
        $ conda activate django_rf
        $ pip install djangorestframework
        $ pip install opencv-python
        $ pip install Pillow
        $ pip install psycopg2-binary
        $ pip install requests
        $ pip install pre-commit

#. Install pre-commit.

        $ pre-commit install

#. Run code.

        $ cd video_process
        $ bash run.sh

### References
https://codeloop.org/django-rest-framework-course-for-beginners/
https://www.youtube.com/watch?v=B38aDwUpcFc
