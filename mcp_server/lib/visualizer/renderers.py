"""
Diagram Rendering Utilities
Handles conversion of diagram code to various output formats (PNG, SVG, etc.)
"""

import base64
import zlib
import urllib.request
import urllib.error
from pathlib import Path

from lib.utils.constants import KROKI_API_BASE_URL, MERMAID_COMPRESSION_LEVEL


class DiagramGenerationError(Exception):
    """Raised when diagram generation fails"""
    pass


def save_mermaid_as_png(mermaid_code: str, base_output_path: str) -> str:
    """
    Converts Mermaid text directly into a real PNG image using the Kroki API.
    Requires NO local installations (no Graphviz, no Node.js).
    
    Args:
        mermaid_code: Mermaid diagram code (with or without markdown wrapper)
        base_output_path: Base path for output file (extension will be changed to .png)
        
    Returns:
        Path to the generated PNG file
        
    Raises:
        DiagramGenerationError: If PNG generation fails for any reason
        
    Example:
        >>> mermaid_code = "graph TD\\n    A-->B"
        >>> png_path = save_mermaid_as_png(mermaid_code, "output/diagram.md")
        >>> print(png_path)  # "output/diagram.png"
    """
    try:
        # 1. Clean the markdown wrapper off the Mermaid string
        clean_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
        
        if not clean_code:
            raise DiagramGenerationError("Empty mermaid code provided")
        
        # 2. Compress and Base64 encode the string (Kroki's requirement)
        compressed = zlib.compress(clean_code.encode('utf-8'), MERMAID_COMPRESSION_LEVEL)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
        
        # 3. Build the API URL
        url = f"{KROKI_API_BASE_URL}/mermaid/png/{encoded}"
        
        # 4. Determine the final .png file path
        # If base_output_path is a .md file, change the extension to .png
        out_file = Path(base_output_path).with_suffix('.png')
        
        # 5. Download the image and save it to disk
        urllib.request.urlretrieve(url, str(out_file))
        
        # 6. Verify the file was created
        if not out_file.exists():
            raise DiagramGenerationError(f"PNG file was not created at {out_file}")
        
        return str(out_file)
        
    except DiagramGenerationError:
        # Re-raise our custom errors
        raise
    except urllib.error.HTTPError as e:
        raise DiagramGenerationError(f"Kroki API HTTP error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        raise DiagramGenerationError(f"Network error connecting to Kroki API: {str(e.reason)}")
    except Exception as e:
        raise DiagramGenerationError(f"Unexpected error generating PNG: {str(e)}")


# Made with Bob