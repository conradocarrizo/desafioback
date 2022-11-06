* configurar entorno virtual
    ``` bash
    # se hace uso de pyenv
    cd ~/desafioback/
    pyenv install 3.8.0 
    pyenv virtualenv 3.8.0 desafioback
    pyenv activate desafioback

    # con el entornovirtaul activo deberia ver algo asi en la shell: (pickup_points_api)     
    pip install -r requirements.txt 
    ```
* iniciar el django
    ``` bash
    cd ~/desafioback/
    ./manage.py runservert 
    ```