from abc import ABC, abstractmethod

class CommandeInterface:
    def execute(self, command):
        """Executes a command in the host"""
        pass