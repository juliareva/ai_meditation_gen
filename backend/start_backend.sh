if [ -z "$VIRTUAL_ENV" ]; then
    # If not in a virtual environment, activate it
    source projvenv/bin/activate
fi

flask --app meditation run