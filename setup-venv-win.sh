echo "Creating virtual environment..."
python -m venv env
echo "Virtual environment created..."
. env/Scripts/activate
echo "Virtual environment activated..."
echo "Upgrading pip..."
python -m pip install --upgrade pip
echo "Pip upgraded..."
FILE=requirements.txt
if [[ -f "$FILE" ]]; then
    echo "Installing requirements..."
    pip install -r $FILE
    echo "Requirements installed..."
else 
    echo "$FILE does not exist..."
fi
FILE=requirements-dev.txt
if [[ -f "$FILE" ]]; then
    echo "Installing dev requirements..."
    pip install -r $FILE
    echo "Dev requirements installed..."
else 
    echo "$FILE does not exist..."
fi
echo "Virtual environment is set up and ready to use."
read -p "Hit enter to finish script."