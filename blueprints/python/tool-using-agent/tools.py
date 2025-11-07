"""
Tool Definitions - Separate Module Pattern

For larger agents, it's helpful to define tools in a separate module.
This keeps the code organized and makes tools reusable.
"""

import random
from typing import List, Dict, Any
from datetime import datetime
import json


# ===== MATH TOOLS =====

def roll_dice(sides: int = 6, count: int = 1) -> Dict[str, Any]:
    """
    Roll one or more dice.

    Args:
        sides: Number of sides on each die (default: 6)
        count: Number of dice to roll (default: 1)

    Returns:
        Dictionary with roll results
    """
    if sides < 2:
        raise ValueError("Dice must have at least 2 sides")
    if count < 1:
        raise ValueError("Must roll at least 1 die")
    if count > 100:
        raise ValueError("Cannot roll more than 100 dice at once")

    rolls = [random.randint(1, sides) for _ in range(count)]

    return {
        "rolls": rolls,
        "total": sum(rolls),
        "count": count,
        "sides": sides,
        "average": sum(rolls) / len(rolls),
    }


def is_prime(number: int) -> Dict[str, Any]:
    """
    Check if a number is prime.

    Args:
        number: The number to check

    Returns:
        Dictionary with prime check results
    """
    if number < 2:
        return {"number": number, "is_prime": False, "reason": "Numbers less than 2 are not prime"}

    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return {
                "number": number,
                "is_prime": False,
                "reason": f"{number} is divisible by {i}",
            }

    return {"number": number, "is_prime": True, "reason": f"{number} is prime!"}


def calculate(expression: str) -> Dict[str, Any]:
    """
    Safely evaluate a mathematical expression.

    Args:
        expression: Mathematical expression (e.g., "2 + 2", "10 * 5")

    Returns:
        Dictionary with calculation results
    """
    try:
        # Warning: eval is dangerous! Use a proper math parser in production
        # Consider using libraries like: py-expression-eval, numexpr, simpleeval
        result = eval(expression, {"__builtins__": {}}, {})
        return {
            "expression": expression,
            "result": result,
            "success": True,
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e),
            "success": False,
        }


# ===== TIME/DATE TOOLS =====

def get_current_time(timezone: str = "UTC") -> Dict[str, Any]:
    """
    Get the current time.

    Args:
        timezone: Timezone name (default: UTC)

    Returns:
        Dictionary with time information
    """
    now = datetime.now()
    return {
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": timezone,
    }


# ===== TEXT PROCESSING TOOLS =====

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text and return statistics.

    Args:
        text: The text to analyze

    Returns:
        Dictionary with text statistics
    """
    words = text.split()
    sentences = text.split(".")
    characters = len(text)

    return {
        "character_count": characters,
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "unique_words": len(set(word.lower() for word in words)),
    }


def reverse_text(text: str, by_word: bool = False) -> str:
    """
    Reverse text.

    Args:
        text: The text to reverse
        by_word: If True, reverse word order instead of characters

    Returns:
        Reversed text
    """
    if by_word:
        return " ".join(reversed(text.split()))
    else:
        return text[::-1]


# ===== DATA CONVERSION TOOLS =====

def convert_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """
    Convert between different units.

    Args:
        value: The value to convert
        from_unit: Source unit
        to_unit: Target unit

    Returns:
        Dictionary with conversion results
    """
    # Simple example for temperature conversion
    conversions = {
        ("celsius", "fahrenheit"): lambda x: (x * 9 / 5) + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5 / 9,
        ("meters", "feet"): lambda x: x * 3.28084,
        ("feet", "meters"): lambda x: x / 3.28084,
        ("kilograms", "pounds"): lambda x: x * 2.20462,
        ("pounds", "kilograms"): lambda x: x / 2.20462,
    }

    key = (from_unit.lower(), to_unit.lower())

    if key not in conversions:
        return {
            "error": f"Conversion from {from_unit} to {to_unit} not supported",
            "success": False,
        }

    result = conversions[key](value)

    return {
        "original_value": value,
        "original_unit": from_unit,
        "converted_value": result,
        "converted_unit": to_unit,
        "success": True,
    }


# ===== API CALL TOOLS =====

def fetch_weather(city: str) -> Dict[str, Any]:
    """
    Fetch weather information for a city.

    Args:
        city: City name

    Returns:
        Dictionary with weather data
    """
    # TODO: Implement actual weather API call
    # Example: use OpenWeatherMap API
    # import requests
    # api_key = os.getenv("OPENWEATHER_API_KEY")
    # response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    # return response.json()

    return {
        "city": city,
        "temperature": "20°C",
        "conditions": "Sunny",
        "note": "This is mock data. Implement actual API call.",
    }


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for information.

    Args:
        query: Search query
        max_results: Maximum number of results (default: 5)

    Returns:
        List of search results
    """
    # TODO: Implement actual web search
    # Options: Google Custom Search API, Bing Search API, DuckDuckGo API

    return [
        {
            "title": f"Result {i + 1} for '{query}'",
            "url": f"https://example.com/result{i + 1}",
            "snippet": "This is a mock search result. Implement actual search API.",
        }
        for i in range(max_results)
    ]


# ===== FILE TOOLS =====

def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Read a file's contents.

    Args:
        file_path: Path to the file
        encoding: File encoding (default: utf-8)

    Returns:
        Dictionary with file contents
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()

        return {
            "file_path": file_path,
            "content": content,
            "size": len(content),
            "success": True,
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "success": False,
        }


def write_file(file_path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Write content to a file.

    Args:
        file_path: Path to the file
        content: Content to write
        encoding: File encoding (default: utf-8)

    Returns:
        Dictionary with write results
    """
    try:
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)

        return {
            "file_path": file_path,
            "bytes_written": len(content),
            "success": True,
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "success": False,
        }


# ===== TOOL REGISTRY =====

# All available tools with their metadata
TOOLS = {
    # Math tools
    "roll_dice": {
        "function": roll_dice,
        "description": "Roll one or more dice with specified number of sides",
        "category": "math",
        "examples": ["Roll 2 six-sided dice", "Roll a 20-sided die"],
    },
    "is_prime": {
        "function": is_prime,
        "description": "Check if a number is prime",
        "category": "math",
        "examples": ["Is 17 prime?", "Check if 100 is prime"],
    },
    "calculate": {
        "function": calculate,
        "description": "Evaluate a mathematical expression",
        "category": "math",
        "examples": ["Calculate 25 * 4", "What is 100 / 5?"],
    },
    # Time tools
    "get_current_time": {
        "function": get_current_time,
        "description": "Get the current date and time",
        "category": "time",
        "examples": ["What time is it?", "Get current time"],
    },
    # Text tools
    "analyze_text": {
        "function": analyze_text,
        "description": "Analyze text and return statistics",
        "category": "text",
        "examples": ["Analyze this text", "Get word count"],
    },
    "reverse_text": {
        "function": reverse_text,
        "description": "Reverse text by characters or words",
        "category": "text",
        "examples": ["Reverse 'hello'", "Reverse word order"],
    },
    # Conversion tools
    "convert_units": {
        "function": convert_units,
        "description": "Convert between different units of measurement",
        "category": "conversion",
        "examples": ["Convert 100 celsius to fahrenheit", "Convert 5 feet to meters"],
    },
    # API tools
    "fetch_weather": {
        "function": fetch_weather,
        "description": "Get weather information for a city",
        "category": "api",
        "examples": ["What's the weather in London?", "Get weather for Tokyo"],
    },
    "search_web": {
        "function": search_web,
        "description": "Search the web for information",
        "category": "api",
        "examples": ["Search for Python tutorials", "Find information about AI"],
    },
    # File tools
    "read_file": {
        "function": read_file,
        "description": "Read contents of a file",
        "category": "file",
        "examples": ["Read file.txt", "Show contents of data.json"],
    },
    "write_file": {
        "function": write_file,
        "description": "Write content to a file",
        "category": "file",
        "examples": ["Write 'hello' to file.txt", "Save data to output.json"],
    },
}


def get_tools_by_category(category: str) -> Dict[str, Any]:
    """Get all tools in a specific category."""
    return {
        name: info
        for name, info in TOOLS.items()
        if info["category"] == category
    }


def get_all_categories() -> List[str]:
    """Get list of all tool categories."""
    return list(set(info["category"] for info in TOOLS.values()))
