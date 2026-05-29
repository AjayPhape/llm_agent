import xml.etree.ElementTree as ET
from collections import defaultdict
from zipfile import ZipFile

import networkx as nx

VSDX_FILE = "C:\\Users\\AjayPhape\\Downloads\\BPMN In Color Sample.vsdx"

ns = {"v": "http://schemas.microsoft.com/office/visio/2012/main"}

G = nx.DiGraph()

with ZipFile(VSDX_FILE, "r") as z:
    # Read all page XMLs
    # page_files = [
    #     xml
    #     for xml in z.namelist()
    #     if xml.startswith("visio/pages/page") and xml.endswith(".xml")
    # ]

    for page in z.namelist():
        if not (page.startswith("visio/pages/page") and page.endswith(".xml")):
            continue

        xml_data = z.read(page)
        root = ET.fromstring(xml_data)

        # ----------------------
        # Extract Shapes (Nodes)
        # ----------------------
        shapes = {}

        for shape in root.findall(".//v:Shape", ns):
            shape_id = shape.attrib.get("ID")

            text_elem = shape.find(".//v:Text", ns)

            label = ""

            if text_elem is not None:
                label = "".join(text_elem.itertext()).strip()

            shapes[shape_id] = label

            G.add_node(shape_id, label=label)

        # ----------------------
        # Extract Connections
        # ----------------------
        connects = root.findall(".//v:Connect", ns)

        connector_map = defaultdict(list)

        for c in connects:
            from_sheet = c.attrib.get("FromSheet")
            to_sheet = c.attrib.get("ToSheet")

            connector_map[from_sheet].append(to_sheet)

        # Connector normally links 2 shapes
        for connector, targets in connector_map.items():
            if len(targets) == 2:
                src = targets[0]
                dst = targets[1]

                if src in shapes and dst in shapes:
                    G.add_edge(src, dst)

# ----------------------
# Print Graph
# ----------------------

print("Nodes:")
for n, data in G.nodes(data=True):
    print(n, data)

print("\nEdges:")
for e in G.edges():
    print(e)
