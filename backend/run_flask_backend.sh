uv backend_venv
source .backend_venv/bin/activate
uv pip install -r requirements.txt
cd ppa
python3 models_setup.py
cd ..
flask --app run run