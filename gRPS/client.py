from __future__ import print_function

import logging
import io

import grpc
from gRPS import grpc_server_pb2
from gRPS import grpc_server_pb2_grpc

"""
def test_getList(stub, name):
    listFile = stub.GetList(name)
    print('List got')
    for c in listFile:
        print(c.title)
"""
stub = None

def run():
    global stub
    stub = grpc_server_pb2_grpc.ServerMethodsStub(grpc.insecure_channel('localhost:50051'))
    print(stub)
    #test_getList(stub, grpc_server_pb2.BucketName(name = 'articles'))

if __name__ == "__main__":
    logging.basicConfig()
    run()