#!/bin/bash
sudo apt-get install python3.8-venv pandoc texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra texlive-xetex -y
python3 -m venv scraper-env
source scraper-env/bin/activate
pip install -r requirements.txt
exit 0