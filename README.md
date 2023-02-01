# pizza-flow
A python multiprocessing exercise

### requirements
- Python 3
- MongoDB
- Docker

### Clone
```
git clone https://github.com/Nemo20k/pizza-flow.git
cd pizza-flow

```

### Usage
 ##### with MongoDB using Docker
 ```bash
 docker-compose up --build
 ```

 #### using Python & Mongo
 ```bash
 pip install -r ./requirements.txt
 mongod
 python3 main.py --mongo_uri "mongodb://localhost:27017"
 ```

 #### just run python
  ```bash
 pip install -r ./requirements.txt
 python3 main.py
 ```


you can edit the pizza input by editing the file `order.toml`, or the worker setting by editing `workers.toml`, or by giving other files as arguments using
```bash
 python3 main.py --worker_file "path-to-worker-file.toml" --order_file "path-to-order-file.toml"
```
