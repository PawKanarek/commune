


import streamlit as st
import os, sys
sys.path.append(os.getenv('PWD'))
import datasets
from typing import *
from copy import deepcopy
from commune import Module
class ClientModule(Module):
    registered_clients = {}

    def __init__(self, clients:Union[List, Dict, Bool, None]):

        if clients == False or clients == None:
            return None
        elif isinstance(client, dict):
            return ClientModule(client)
        elif isinstance(client, list):
            return ClientModule(client)
        else:
            raise NotImplementedError

        self.register_clients(clients=clients)
    def get_default_clients(self):
        client_path_dict = dict(
        ipfs = 'commune.client.ipfs.module.IPFSModule',
        local = 'commune.client.local.module.LocalModule',
        s3 = 'commune.client.s3.module.S3Module',
        estuary = 'commune.client.estuary.module.EstuaryModule',
        pinata = 'commune.client.pinata.module.PinataModule',
        rest = 'commune.client.rest.module.RestModule',
        # ray='client.ray.module.RayModule'
        )
        return client_path_dict


    @property
    def client_path_dict(self):
        return self.get_default_clients()


    @property
    def default_clients(self):
        return list(self.get_default_clients().keys())

    def register_clients(self, clients=None):

        if isinstance(clients, list):
            assert all([isinstance(c,str)for c in clients]), f'{clients} should be all strings'
            for client in clients:
                self.register_client(client=client)
        elif isinstance(clients, dict):
            for client, client_kwargs in clients.items():
                self.register_client(client=client, **client_kwargs)
        else:
            raise NotImplementedError(f'{clients} is not supported')

    def get_client_class(self, client:str):
        assert client in self.client_path_dict, f"{client} is not in {self.default_clients}"
        return self.get_object(self.client_path_dict[client])

    def register_client(self, client, **kwargs):
        assert isinstance(client, str)
        assert client in self.default_clients,f"{client} is not in {self.default_clients}"

        client_module = self.get_client_class(client)(**kwargs)
        setattr(self, client, client_module )
        self.registered_clients[client] = client_module

    def remove_client(client:str):
        self.__dict__.pop(client, None)
        self.registered_clients.pop(client, None)
        return client
    
    delete_client = rm_client= remove_client
    
    def remove_clients(clients:list):
        output_list = []
        for client in clients:
            output_list.append(self.remove_client(client))
        return output_list

    delete_clients = rm_clients= remove_clients

    def get_registered_clients(self):
        return list(self.registered_clients.keys())


if __name__ == '__main__':
    import streamlit as st
    module = ClientModule()
    st.write(ClientModule._config())
    # st.write(module.__dict__)