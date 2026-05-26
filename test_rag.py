import os
from dotenv import load_dotenv
from agent.rag import build_qa_chain
from agent.router import route_property

load_dotenv()

# Test 1: router
print("=== Router Test ===")
print(route_property("what time does golden spoon close?"))
print(route_property("does azure beach have a pool?"))
print(route_property("what is the wifi password?"))

# Test 2: RAG
print("\n=== RAG Test ===")
question = "what time does golden spoon close?"
property_key = route_property(question)
answer = build_qa_chain(property_key)
print(answer(question))
