# Register Model
```
from azureml.core import Model

run.register_model( model_name='mnist_model',
                    model_path='outputs/mnist.h5', # run outputs path
                    description='A classification model')
```
# List Model
```
for model in Model.list(ws):
    print(model.name)
```

# Use Model
```
import os

model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'mnist.h5')

model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "model/sklearn_regression_model.pkl"
    )
```