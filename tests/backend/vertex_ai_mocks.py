# tests/backend/vertex_ai_mocks.py

"""
Lightweight Vertex AI mock installation for arcade agent tests.

The goal is:
- Let arcade_app.agent import `vertexai.*` without ImportError.
- Provide a simple GenerativeModel that returns a fixed text payload.
- Be easy to extend if the agent starts using more methods later.
"""

# WARNING: If you add a new vertexai query in the agents, YOU MUST add a corresponding mock here.
# Missing mocks will cause Silent failures in the SSE stream generator (ImportError/AttributeError).

from __future__ import annotations

import sys
import types
from typing import Optional, Any

__all__ = [
    "install_vertex_ai_mocks",
    "reset_vertex_ai_mocks",
    "set_vertex_ai_default_text",
    "MockGenerativeModel",
]

# Default text used by mocks; tests can override via set_vertex_ai_default_text.
_DEFAULT_TEXT = "Hello from Smoke Test Agent"


def set_vertex_ai_default_text(text: str) -> None:
    """
    Override the default text produced by the mock LLM.

    You can call this at the start of a test to change the expected SSE payload,
    e.g. "Smoke Test Judge Agent" or "Smoke Test Explain Agent".
    """
    global _DEFAULT_TEXT
    _DEFAULT_TEXT = text


class _MockGenerateResponse:
    def __init__(self, text: str) -> None:
        self.text = text


class _MockChatSession:
    def send_message(self, *args, **kwargs) -> _MockGenerateResponse:
        # Matches "chat" APIs like start_chat().send_message(...)
        return _MockGenerateResponse(_DEFAULT_TEXT)


class MockGenerativeModel:
    """
    Minimal stand-in for vertexai.generative_models.GenerativeModel.

    Supports:
    - GenerativeModel("model-name")
    - generate_content(...)
    - start_chat().send_message(...)
    """

    def __init__(self, *args, **kwargs) -> None:
        self._model_name = args[0] if args else "mock-model"

    def generate_content(self, *args, **kwargs) -> _MockGenerateResponse:
        return _MockGenerateResponse(_DEFAULT_TEXT)

    async def generate_content_async(self, *args, **kwargs) -> _MockGenerateResponse | _MockAsyncIterator:
        stream = kwargs.get("stream", False)
        if stream:
            return _MockAsyncIterator(_DEFAULT_TEXT)
        return _MockGenerateResponse(_DEFAULT_TEXT)

    def start_chat(self, *args, **kwargs) -> _MockChatSession:
        return _MockChatSession()


class _MockAsyncIterator:
    """Helper for streaming responses."""
    def __init__(self, text: str):
        self.text = text
        self.chunks = [text] # Just yield full text as one chunk for simplicity

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.chunks:
            raise StopAsyncIteration
        return _MockGenerateResponse(self.chunks.pop(0))


def install_vertex_ai_mocks(default_text: Optional[str] = None) -> None:
    """
    Install mocked `vertexai` modules into sys.modules.

    This creates:
    - vertexai
    - vertexai.generative_models (with GenerativeModel)
    - vertexai.language_models
    - vertexai.preview
    - vertexai.vision_models

    If `default_text` is provided, it becomes the default LLM output.
    """
    global _DEFAULT_TEXT
    if default_text is not None:
        _DEFAULT_TEXT = default_text

    # Root module
    vertexai_root = types.ModuleType("vertexai")
    vertexai_root.__path__ = [] # Mark as package

    # Provide a no-op init to satisfy vertexai.init(...)
    def _init(*_args, **_kwargs) -> None:
        return None

    vertexai_root.init = _init  # type: ignore[attr-defined]

    # Submodules
    generative_models = types.ModuleType("vertexai.generative_models")
    generative_models.__path__ = [] # Mark as package
    generative_models.GenerativeModel = MockGenerativeModel  # type: ignore[attr-defined]

    # Create the internal _generative_models module that seems to be requested
    _generative_models = types.ModuleType("vertexai.generative_models._generative_models")
    
    # Add potentially missing enums for safety settings
    class MockHarmBlockThreshold:
        BLOCK_NONE = "BLOCK_NONE"
        BLOCK_LOW_AND_ABOVE = "BLOCK_LOW_AND_ABOVE"
        BLOCK_MEDIUM_AND_ABOVE = "BLOCK_MEDIUM_AND_ABOVE"
        BLOCK_ONLY_HIGH = "BLOCK_ONLY_HIGH"

    class MockHarmCategory:
        HARM_CATEGORY_HARASSMENT = "HARM_CATEGORY_HARASSMENT"
        HARM_CATEGORY_HATE_SPEECH = "HARM_CATEGORY_HATE_SPEECH"
        HARM_CATEGORY_SEXUALLY_EXPLICIT = "HARM_CATEGORY_SEXUALLY_EXPLICIT"
        HARM_CATEGORY_DANGEROUS_CONTENT = "HARM_CATEGORY_DANGEROUS_CONTENT"

    class MockSafetySetting:
        pass

    class MockFunctionDeclaration:
        def __init__(self, **kwargs):
            pass

    class MockTool:
        def __init__(self, function_declarations=None):
            self.function_declarations = function_declarations or []

    class MockToolConfig:
        pass

    class MockInputOutputTextPair:
        pass

    class MockTextGenerationResponse:
        pass

    class MockCaching:
        pass

    class MockGeneratedImage:
        pass

    class MockImageGenerationModel:
        pass

    class MockImageTextModel:
        pass

    class MockSafetySettingsType:
        pass

    class MockGenerationConfigType:
        pass

    class MockGenerationResponse:
        pass

    def _convert_schema_dict_to_gapic(schema_dict):
        return schema_dict

    class MockPart:
        def __init__(self, text=None):
            self.text = text

    class MockContent:
        def __init__(self, parts=None):
            self.parts = parts or []

    class MockCandidate:
        def __init__(self, content=None, finish_reason=None):
            self.content = content
            self.finish_reason = finish_reason

    class MockFinishReason:
        STOP = "STOP"
        MAX_TOKENS = "MAX_TOKENS"
        SAFETY = "SAFETY"
        RECITATION = "RECITATION"
        OTHER = "OTHER"

    class MockImage:
         pass

    # Populate _generative_models
    _generative_models.HarmBlockThreshold = MockHarmBlockThreshold
    _generative_models.HarmCategory = MockHarmCategory
    _generative_models.SafetySetting = MockSafetySetting
    _generative_models.SafetySettingsType = MockSafetySettingsType
    _generative_models.GenerationConfigType = MockGenerationConfigType
    _generative_models.GenerationResponse = MockGenerationResponse
    _generative_models._convert_schema_dict_to_gapic = _convert_schema_dict_to_gapic
    _generative_models.FunctionDeclaration = MockFunctionDeclaration
    _generative_models.Tool = MockTool
    _generative_models.ToolConfig = MockToolConfig
    _generative_models.Part = MockPart
    _generative_models.Content = MockContent
    _generative_models.Candidate = MockCandidate
    _generative_models.FinishReason = MockFinishReason
    _generative_models.Image = MockImage
    _generative_models.GenerativeModel = MockGenerativeModel

    # Populate generative_models
    generative_models.HarmBlockThreshold = MockHarmBlockThreshold
    generative_models.HarmCategory = MockHarmCategory
    generative_models.SafetySetting = MockSafetySetting
    generative_models.SafetySettingsType = MockSafetySettingsType
    generative_models.GenerationConfigType = MockGenerationConfigType
    generative_models.GenerationResponse = MockGenerationResponse
    generative_models.FunctionDeclaration = MockFunctionDeclaration
    generative_models.Tool = MockTool
    generative_models.ToolConfig = MockToolConfig
    generative_models.Part = MockPart
    generative_models.Content = MockContent
    generative_models.Candidate = MockCandidate
    generative_models.FinishReason = MockFinishReason
    generative_models.Image = MockImage
    generative_models.GenerativeModel = MockGenerativeModel

    language_models = types.ModuleType("vertexai.language_models")
    language_models.InputOutputTextPair = MockInputOutputTextPair
    language_models.TextGenerationResponse = MockTextGenerationResponse
    preview = types.ModuleType("vertexai.preview")
    preview.caching = MockCaching
    vision_models = types.ModuleType("vertexai.vision_models")
    vision_models.GeneratedImage = MockGeneratedImage
    vision_models.Image = MockImage
    vision_models.ImageGenerationModel = MockImageGenerationModel
    vision_models.ImageTextModel = MockImageTextModel

    # Register into sys.modules
    sys.modules["vertexai"] = vertexai_root
    sys.modules["vertexai.generative_models"] = generative_models
    sys.modules["vertexai.generative_models._generative_models"] = _generative_models
    sys.modules["vertexai.language_models"] = language_models
    sys.modules["vertexai.preview"] = preview
    sys.modules["vertexai.vision_models"] = vision_models


def reset_vertex_ai_mocks() -> None:
    """
    Remove vertexai entries from sys.modules.

    Optional cleanup; most test runs won't strictly need this, but it's here
    if you want to be explicit.
    """
    for name in list(sys.modules.keys()):
        if name == "vertexai" or name.startswith("vertexai."):
            sys.modules.pop(name, None)
