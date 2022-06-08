#!/bin/bash
sudo apt-get install python3.8-venv pandoc texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra texlive-xetex -y
python3 -m venv scraper-env
source scraper-env/bin/activate
pip install -r requirements.txt
pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
exit 0