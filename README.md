# fastapi-example
fastapi、mongo、jwt example
# 目录如下
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── authenticaion.py
│   │   └── user.py
│   ├── common
│   │   └── security.py
│   ├── core
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── jwt.py
│   │   └── logging.py
│   ├── crud
│   │   └── user.py
│   ├── db
│   │   ├── mongodb.py
│   │   ├── mongodb_utils.py
│   │   └── redis.py
│   ├── main.py
│   ├── models
│   │   ├── common.py
│   │   ├── token.py
│   │   └── user.py
│   └── runtime.log
└── deploy.yaml
