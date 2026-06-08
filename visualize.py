
import random
import ipywidgets as widgets
from IPython.display import display
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

#Function to visualize XML structure with highlighted elements
def VisualizeXML(xml_string: str, highlight_dict: Dict[str, int]):

    #Helper function to map intensity to color gradients
    def colorize(value: float, max_value: float):
        normalized = value / max_value if max_value else 0
        color = plt.cm.YlOrRd(normalized)
        return color

    #Function to generate a legend
    def generate_legend(highlight_dict: Dict[str, int]):
        min_value = min(highlight_dict.values())
        max_value = max(highlight_dict.values())
        gradient = np.linspace(min_value, max_value, 256)
        fig, ax = plt.subplots(figsize=(6, 0.2))
        ax.imshow([gradient], aspect='auto', cmap='YlOrRd', extent=[0, 10, 0, 1])
        ax.set_axis_off()
        ax.set_xlim(0, 10)
        ax.text(0, 1.1, f'{min_value}', fontsize=10, ha='left', va='bottom', color='black')
        ax.text(10, 1.1, f'{max_value}', fontsize=10, ha='right', va='bottom', color='black')
        plt.show()

    #Recursive function to format XML while applying highlights to relevant elements
    def format_xml_with_highlight(element, depth:int = 0, highlight_dict: Dict[str, int] | None = None):
        indent = "    " * depth

        #Function to apply background color highlights to specified text content
        def highlight(content: str):
            if highlight_dict:
                for text, intensity in highlight_dict.items():
                    if text in content:
                        color = colorize(intensity, max(highlight_dict.values()))
                        rgba = f'rgba({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)}, {color[3]})'
                        content = content.replace(
                            text,
                            f'<span style="background-color: {rgba};">{text}</span>'
                        )
            return content

        #Extract and format tag name, stripping XML namespace for clarity
        tag_name = highlight(element.tag.split('}')[-1])

        #Format attributes with highlighting
        attribs = " ".join([
            f'{highlight(key.split("}")[-1])}="{highlight(value)}"' for key, value in element.attrib.items()
        ])

        # Preserve spacing if attributes exist
        attribs = f" {attribs}" if attribs else ""
        opening_tag = f"&lt;{tag_name}{attribs}&gt;"
        closing_tag = f"&lt;/{tag_name}&gt;"

        #Handle text content and recursion for child elements
        if len(element) == 0:
            content = highlight(element.text.strip()) if element.text and element.text.strip() else ""
            return f"{indent}{opening_tag}{content}{closing_tag}\n"
        else: # If children exist, format with proper nesting
            children = "".join([format_xml_with_highlight(child, depth + 1, highlight_dict) for child in element])
            return f"{indent}{opening_tag}\n{children}{indent}{closing_tag}\n"

    try:
        #Parse the XML string and register namespace for correct handling of attributes
        root = ET.fromstring(xml_string)
        namespaces = {"android": "http://schemas.android.com/apk/res/android"}
        ET.register_namespace("android", namespaces["android"])

        #Generate formatted XML string with highlights
        formatted_xml = format_xml_with_highlight(root, highlight_dict=highlight_dict)

        #Create an HTML widget to display formatted XML with highlights
        html_widget = widgets.HTML(
            value=f"<pre style='font-family: monospace; white-space: pre-wrap;'>{formatted_xml}</pre>",
            layout=widgets.Layout(width="100%", height="400px", overflow="auto")
        )

        #Display the color legend and formatted XML
        generate_legend(highlight_dict)
        display(html_widget)

    except Exception as e:
        display(widgets.HTML(f"<b>Error:</b> {e}"))