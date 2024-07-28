from abc import ABC, abstractmethod


class Agent():
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def chat(self):
        return "Default agent"
