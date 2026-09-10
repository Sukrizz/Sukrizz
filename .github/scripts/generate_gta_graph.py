import urllib.request
import re
import os
import random

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch contributions: {e}")
        return []

    matches = re.findall(r'data-level="(\d+)"', html)
    levels = [int(m) for m in matches]
    return levels

def generate_svg(levels):
    # If no levels found (e.g. rate limit), generate a realistic fake year of data (365 days)
    if not levels:
        print("Using simulated data for preview.")
        levels = [random.choices([0, 1, 2, 3, 4], weights=[0.7, 0.15, 0.08, 0.05, 0.02])[0] for _ in range(365)]
        
    weeks = len(levels) // 7
    if len(levels) % 7 != 0:
        weeks += 1

    cell_size = 12
    cell_gap = 4
    # Padding and dimensions
    padding_x = 20
    padding_y = 40
    svg_width = max(weeks * (cell_size + cell_gap) + padding_x * 2, 800)
    svg_height = 7 * (cell_size + cell_gap) + padding_y * 2 + 30

    # Colors for monochrome GTA night city
    colors = {
        0: "#141414", # empty / dark
        1: "#333333", # dim
        2: "#666666", # medium
        3: "#aaaaaa", # bright
        4: "#ffffff"  # intense
    }

    svg_elements = []
    svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%">')
    svg_elements.append('<style>')
    svg_elements.append('  .bg { fill: #050505; }')
    svg_elements.append('  .car { animation: drive 12s linear infinite; }')
    svg_elements.append(f'  @keyframes drive {{ 0% {{ transform: translateX(-60px); }} 100% {{ transform: translateX({svg_width + 60}px); }} }}')
    svg_elements.append('  .window { animation: flicker 4s infinite alternate; }')
    svg_elements.append('  @keyframes flicker { 0% { opacity: 0.7; } 100% { opacity: 1; } }')
    svg_elements.append('  .text { fill: #ffffff; font-family: "Courier New", Courier, monospace; font-size: 14px; font-weight: bold; letter-spacing: 2px; }')
    svg_elements.append('</style>')
    
    # Background
    svg_elements.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" rx="8" />')

    # Add Night Shift title
    svg_elements.append(f'<text x="{padding_x}" y="25" class="text">NIGHT SHIFT // DEV</text>')

    # Draw the road above the graph
    road_y = 35
    road_height = 14
    svg_elements.append(f'<rect x="0" y="{road_y}" width="{svg_width}" height="{road_height}" fill="#1a1a1a" />')
    svg_elements.append(f'<rect x="0" y="{road_y}" width="{svg_width}" height="1" fill="#333333" />')
    svg_elements.append(f'<rect x="0" y="{road_y + road_height - 1}" width="{svg_width}" height="1" fill="#333333" />')
    
    # Road markings
    for wx in range(0, svg_width, 30):
        svg_elements.append(f'<rect x="{wx}" y="{road_y + (road_height/2) - 1}" width="15" height="2" fill="#555555" />')

    # Draw the car (GTA pixel art style top-down)
    car_y = road_y + 3
    svg_elements.append(f'<g class="car" transform="translate(0, {car_y})">')
    # Car body (white/gray)
    svg_elements.append('<rect x="0" y="0" width="20" height="8" fill="#eeeeee" rx="2" />')
    # Windshield
    svg_elements.append('<rect x="13" y="1" width="3" height="6" fill="#000000" />')
    # Rear window
    svg_elements.append('<rect x="2" y="1" width="3" height="6" fill="#000000" />')
    # Headlights
    svg_elements.append('<rect x="18" y="0" width="2" height="2" fill="#ffffff" />')
    svg_elements.append('<rect x="18" y="6" width="2" height="2" fill="#ffffff" />')
    # Taillights
    svg_elements.append('<rect x="0" y="0" width="1" height="2" fill="#555555" />')
    svg_elements.append('<rect x="0" y="6" width="1" height="2" fill="#555555" />')
    # Headlight beams
    svg_elements.append('<polygon points="20,1 45,-6 45,4" fill="#ffffff" opacity="0.15" />')
    svg_elements.append('<polygon points="20,7 45,4 45,14" fill="#ffffff" opacity="0.15" />')
    svg_elements.append('</g>')

    # Calculate offset to center the grid
    grid_width = weeks * (cell_size + cell_gap)
    offset_x = (svg_width - grid_width) / 2
    if offset_x < padding_x:
        offset_x = padding_x

    start_y = road_y + road_height + 20

    # Draw the city grid (contributions)
    for i, level in enumerate(levels):
        week = i // 7
        day = i % 7
        x = offset_x + week * (cell_size + cell_gap)
        y = start_y + day * (cell_size + cell_gap)
        color = colors.get(level, "#141414")
        
        # Draw a little "building" for non-zero contributions
        if level > 0:
            # Building base
            svg_elements.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" />')
            # Little window inside to give a city vibe
            window_size = 4
            wx = x + (cell_size - window_size) / 2
            wy = y + (cell_size - window_size) / 2
            window_color = "#ffffff" if level > 2 else "#888888"
            svg_elements.append(f'<rect class="window" x="{wx}" y="{wy}" width="{window_size}" height="{window_size}" fill="{window_color}" rx="1"/>')
        else:
            # Just a dark grid square
            svg_elements.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" />')

    svg_elements.append('</svg>')
    return "\n".join(svg_elements)

if __name__ == "__main__":
    # Fetch data and generate
    levels = fetch_contributions("Sukrizz")
    svg_content = generate_svg(levels)
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    with open("assets/gta_contribution.svg", "w") as f:
        f.write(svg_content)
    print("Successfully generated assets/gta_contribution.svg")

