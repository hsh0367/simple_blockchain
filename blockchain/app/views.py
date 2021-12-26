from uuid import uuid4
import json
from time import time
from textwrap import dedent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from app.blockchain import Blockchain

node_identifier = str(uuid4()).replace("-", "")
blockchain = Blockchain()


class MineView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        last_block = blockchain.last_block
        last_proof = last_block["proof"]
        proof = blockchain.pow(last_proof)
        blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
        response = {
            "message": "new block found",
            "time": block["timestamp"],
            "index": block["index"],
            "transactions": block["transactions"],
            "proof": block["proof"],
            "previous_hash": block["previous_hash"],
        }
        return Response(response)


class TransactionsNewView(APIView):
    def post(self, request):
        data = request.data
        index = blockchain.new_transaction(
            sender=data.get("sender", None),
            recipient=data.get("recipient", None),
            amount=data.get("amount", 0),
        )
        response = {"message": f"transaction will be added to Block {index}"}
        return Response(response)


# {
#     "sender": "0",
#     "recipient": "063104e7a1794a788ce272b25c4ee898",
#     "amount": 1
# }


class FullChainView(APIView):
    def get(self, request, format=None):
        response = {
            "cahin": blockchain.chain,
            "length": len(blockchain.chain),
        }
        return Response(response)


class NodeRegisterView(APIView):
    def post(self, request):
        data = request.data
        nodes = data.get("node", None)
        for node in nodes:
            blockchain.register_node(node)
        response = {
            "message": "New nodes have been addend",
            "total_nodes": list(blockchain.nodes),
        }
        return Response(response)


# class NodeResolveView(APIView):
#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)
