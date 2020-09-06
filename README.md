# insightface-lite-service

基于 [fastapi](https://github.com/tiangolo/fastapi) 和 [insightface](https://github.com/deepinsight/insightface) 的轻量级人脸识别服务。

## 使用

首先 `clone` 本项目，并进入项目根目录。

### docker

#### 构建镜像

```shell
docker build -t <your-image-name> .
```

如果构建镜像存在困难，可以使用预构建的镜像。
提示，镜像大小为1.95GB。

```shell
docker pull wensun/insightface-lite-service:latest
```

#### 启动容器

```shell
docker run -p <your-port>:80 -d <your-image-name>
```

### 本机

由于人脸识别的依赖限制，需要使用 **Python 3.6** 环境。

然后，按照 `requirements.txt` 安装依赖（该依赖是在 Ubuntu 环境下抽取的），并使用以下命令在本机 8000 端口启动开发服务：

```shell
uvicorn main:app --reload
```

如果按照 `requirements.txt` 安装后无法运行，也可以手动安装依赖：

```shell
pip install fastapi \
    uvicorn \
    python-multipart \
    numpy \
    scikit-image \
    scikit-learn \
    opencv-python \
    mxnet
```

## 现有接口

1. 检查健康状态

   ```ts
   GET /health
   request: null
   response: {
     status: string
   }
   ```

2. 比较两张图片中人脸的相似度（人脸比对）

   ```ts
   POST /compare
   request: {
     face1: multipart-formdata
     face2: multipart-formdata
   },
   response: {
     sim: number;    // similarity
     dist: number;   // distance
   }
   ```

## 常见问题

1. 报错 `ImportError: libGL.so.1: cannot open shared object file: No such file or directory`

   原因是缺少 `libgl1-mesa-glx`。使用以下命令进行安装即可（Ubuntu）：

   ```shell
   sudo apt-get update
   sudo apt-get install libgl1-mesa-glx
   ```

2. 报错 `RuntimeError: Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment.`

   编码问题。按照指示设置环境变量即可：

   ```shell
   export LC_ALL=C.UTF-8
   export LANG=C.UTF-8
   ```

3. 图片识别失败 / 明明有人脸却无法识别 / 相似度过低

   因为依赖的库似乎对背景噪声敏感，所以需要确保图片中的人脸占一定比例，这样才能正确识别。目前计划是对这种错误进行更友好的封装，如果有需要可以自行训练模型。

## TODO

- [ ] 增加CI / CD
- [ ] 减小镜像大小
- [ ] 提高接口健壮性
  - [ ] 更友好的错误处理
  - [ ] 并发处理
- [ ] 增加识别功能