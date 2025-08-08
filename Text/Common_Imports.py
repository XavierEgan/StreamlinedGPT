# https://platform.openai.com/docs/api-reference/chat/create?lang=python
from openai import OpenAI
from .Tool import Tool
from typing import Literal, Any, Callable
from abc import ABC, abstractmethod
import json