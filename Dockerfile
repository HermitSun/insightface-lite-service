FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

COPY . /app
RUN apt-get update \
 && apt-get install -y libgl1-mesa-glx
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn \
    python-multipart \
    numpy \
    scikit-image \
    scikit-learn \
    opencv-python \
    mxnet
