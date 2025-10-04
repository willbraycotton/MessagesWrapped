from lxml import etree

def update_svg(template_file, output_file, replacements):
    tree = etree.parse(template_file)
    root = tree.getroot()

    for text_node in root.xpath("//svg:tspan", namespaces={"svg": "http://www.w3.org/2000/svg"}):
        if text_node.text in replacements:
            text_node.text = replacements[text_node.text]

    tree.write(output_file)
    print(f"Updated SVG saved as {output_file}")






if __name__ == "__main__":

    replacements = {
        "{{mr}}": "John Doe"
    }

    update_svg("Frame 4 1.svg", "output.svg", replacements)
    