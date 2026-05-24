FROM bde2020/spark-master:3.3.0-hadoop3.3

# Install Python, pip, and NumPy from Alpine, then install pandas with pip.
# Build dependencies are removed afterwards so the final image remains smaller.
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-numpy \
    openblas-dev \
    build-base \
    python3-dev \
    linux-headers \
 && python3 -m pip install --upgrade pip \
 && python3 -m pip install pandas \
 && apk del --purge build-base python3-dev linux-headers \
 && rm -rf /var/cache/apk/* /root/.cache/pip

# Set Python 3 as the default
ENV PYSPARK_PYTHON=python3
ENV PYTHONPATH=/opt/project/scripts