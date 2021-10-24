# reev-api-python

Python to get data pro Reev using Reev API and saved it in a JSON file.

[Reev API Documentation](https://api.reev.co/docs)


## Development Environment setup

To create the development environment it's recommended to use conda. 
You can download and install it from the links bellow:

https://docs.conda.io/en/latest/miniconda.html
https://www.anaconda.com/distribution/

Run the following commands to get the environment ready

```
conda create -n ENVIRONMENT_NAME python=3.8
conda activate ENVIRONMENT_NAME
pip install -r requirements.txt
``` 

### Authentication 

To access the APIs, you will need to pass the api_token parameter, 
which can be acquired by going to app.reev.co -> Settings -> Integrations

Then, export your `REEV_TOKEN` to be used in requests to Reev API.

```
export REEV_TOKEN="YOUR TOKEN"
```

### Running

```
python main.py
```

### Testing
To test all functions, first install test requirements and then run pytest.

```
pip install -r tests/tests_requirements.txt
pytest --doctest-modules
```
