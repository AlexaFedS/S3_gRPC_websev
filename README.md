# S3_gRPC_websev
## Генерация протофайлов: 
python -m grpc_tools.protoc -I ./gRPS/protos --python_out=./gRPS --grpc_python_out=./gRPS ./gRPS/protos/grpc_server.proto
## Установить:
django <br/>
djangorestframework <br/>
grpcio <br/>
grpcio-tools <br/>
djoser <br/>
