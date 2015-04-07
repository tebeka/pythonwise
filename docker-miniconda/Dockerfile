# Example Dockerfile for setting up Docker container with MiniConda[1] and an
# example app
# [1] http://conda.pydata.org/miniconda.html

FROM ubuntu:14.04
MAINTAINER Miki Tebeka <miki@353solutions.com>

# System packages 
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

# Python packages from conda
RUN conda install -y \
    scikit-image \
    flask \
    pillow

COPY imgsrv.py /
ENTRYPOINT ["/miniconda/bin/python", "/imgsrv.py"]
EXPOSE 8080
