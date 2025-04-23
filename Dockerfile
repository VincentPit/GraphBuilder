FROM python:3.10-slim

# Set the working directory
WORKDIR .

# Install dependencies (Miniconda and other system dependencies)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libreoffice \
        cmake \
        poppler-utils \
        tesseract-ocr \
        wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda init bash

# Set environment variables for Conda
ENV PATH="/opt/conda/bin:$PATH"
ENV CONDA_AUTO_UPDATE_CONDA=false

# Copy the environment.yml from the current directory
COPY environment.yml /code/

# Create the Conda environment called 'graph' from the environment.yml
RUN conda env create -f /code/environment.yml

# Set the default environment to 'graph' and activate it
SHELL ["conda", "run", "-n", "graph", "/bin/bash", "-c"]

# Expose the necessary port
ENV PORT 8000
EXPOSE 8000

# Copy the application code
COPY . /code

CMD ["/bin/bash"]