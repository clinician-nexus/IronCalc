#!/bin/bash
python -m venv venv
source venv/bin/activate
# not sure why this is needed
pip install patchelf==0.19.1.0
pip install maturin==1.15.0
pip install pytest==9.2.0
maturin develop
pytest tests/
