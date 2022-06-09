# Teenfic webscraper with auto french translation (AI)

https://teenfic.net/

https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-fr


If your GPU support CUDA,please use it instead of your CPU (GPU is approximately 6 times faster in sequential mode with my hardware).

https://developer.nvidia.com/cuda-downloads


## 1) Set environment 

```bash
/bin/bash set_env.sh
```
## 2) Start teenfic-scraper

You just need to input the first URL to download and translate the complete fiction

### Translate with CPU

```bash
source scraper-env/bin/activate
python3 teenfic-scraper.py ${URL}
```

### Translate with GPU (CUDA Toolkit is required)

```bash
source scraper-env/bin/activate
python3 teenfic-scraper-with-cuda.py ${URL}
```
