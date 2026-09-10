import os
import json
import urllib.request

USERNAME = os.environ.get("GITHUB_ACTOR", "Sukrizz")
TOKEN = os.environ.get("GITHUB_TOKEN")

def fetch_contributions_graphql(username, token):
    query = """
    query($userName:String!) {
      user(login: $userName){
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({"query": query, "variables": {"userName": username}}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
    if "errors" in result:
        raise Exception(f"GraphQL Error: {result['errors']}")
        
    return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]

def fetch_contributions_html(username):
    # Fallback when no token is present (e.g. local testing)
    url = f"https://github.com/users/{username}/contributions"
    import re
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch contributions HTML: {e}")
        return []

    matches = re.findall(r'data-level="(\d+)"', html)
    levels = [int(m) for m in matches]
    return levels

def get_levels_from_data(calendar_data):
    weeks = calendar_data["weeks"]
    levels = []
    
    all_counts = []
    for week in weeks:
        for day in week["contributionDays"]:
            if day["contributionCount"] > 0:
                all_counts.append(day["contributionCount"])
                
    all_counts.sort()
    
    if not all_counts:
        thresholds = [1, 2, 3, 4]
    else:
        q1 = all_counts[max(0, len(all_counts)//4 - 1)]
        q2 = all_counts[max(0, len(all_counts)//2 - 1)]
        q3 = all_counts[max(0, len(all_counts)*3//4 - 1)]
        
        t1 = max(1, q1)
        t2 = max(t1 + 1, q2)
        t3 = max(t2 + 1, q3)
        
        thresholds = [t1, t2, t3, max(t3 + 1, all_counts[-1])]
    
    print(f"Calculated thresholds: >0, >={thresholds[0]}, >={thresholds[1]}, >={thresholds[2]}")

    for week in weeks:
        padded_week = [None] * 7
        for day in week["contributionDays"]:
            weekday = day["weekday"] # 0 for Sunday
            count = day["contributionCount"]
            
            level = 0
            if count > 0:
                if count >= thresholds[2]: level = 4
                elif count >= thresholds[1]: level = 3
                elif count >= thresholds[0]: level = 2
                else: level = 1
                
            padded_week[weekday] = level
            
        for day_level in padded_week:
            levels.append(day_level if day_level is not None else 0)
            
    return levels

def generate_svg(levels):
    weeks = len(levels) // 7
    if len(levels) % 7 != 0:
        weeks += 1

    cell_size = 12
    cell_gap = 4
    padding_x = 20
    padding_y = 40
    svg_width = max(weeks * (cell_size + cell_gap) + padding_x * 2, 800)
    svg_height = 7 * (cell_size + cell_gap) + padding_y * 2 + 30

    colors = {
        0: "#141414",
        1: "#333333",
        2: "#666666",
        3: "#aaaaaa",
        4: "#ffffff"
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
    
    svg_elements.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" rx="8" />')
    svg_elements.append(f'<text x="{padding_x}" y="25" class="text">NIGHT SHIFT // DEV</text>')

    road_y = 35
    road_height = 14
    svg_elements.append(f'<rect x="0" y="{road_y}" width="{svg_width}" height="{road_height}" fill="#1a1a1a" />')
    svg_elements.append(f'<rect x="0" y="{road_y}" width="{svg_width}" height="1" fill="#333333" />')
    svg_elements.append(f'<rect x="0" y="{road_y + road_height - 1}" width="{svg_width}" height="1" fill="#333333" />')
    
    for wx in range(0, svg_width, 30):
        svg_elements.append(f'<rect x="{wx}" y="{road_y + (road_height/2) - 1}" width="15" height="2" fill="#555555" />')

    car_y = road_y + 3
    svg_elements.append(f'<g class="car" transform="translate(0, {car_y})">')
    svg_elements.append('<rect x="0" y="0" width="20" height="8" fill="#eeeeee" rx="2" />')
    svg_elements.append('<rect x="13" y="1" width="3" height="6" fill="#000000" />')
    svg_elements.append('<rect x="2" y="1" width="3" height="6" fill="#000000" />')
    svg_elements.append('<rect x="18" y="0" width="2" height="2" fill="#ffffff" />')
    svg_elements.append('<rect x="18" y="6" width="2" height="2" fill="#ffffff" />')
    svg_elements.append('<rect x="0" y="0" width="1" height="2" fill="#555555" />')
    svg_elements.append('<rect x="0" y="6" width="1" height="2" fill="#555555" />')
    svg_elements.append('<polygon points="20,1 45,-6 45,4" fill="#ffffff" opacity="0.15" />')
    svg_elements.append('<polygon points="20,7 45,4 45,14" fill="#ffffff" opacity="0.15" />')
    svg_elements.append('</g>')

    grid_width = weeks * (cell_size + cell_gap)
    offset_x = (svg_width - grid_width) / 2
    if offset_x < padding_x:
        offset_x = padding_x

    start_y = road_y + road_height + 20

    for i, level in enumerate(levels):
        week = i // 7
        day = i % 7
        x = offset_x + week * (cell_size + cell_gap)
        y = start_y + day * (cell_size + cell_gap)
        color = colors.get(level, "#141414")
        
        if level > 0:
            svg_elements.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" />')
            window_size = 4
            wx = x + (cell_size - window_size) / 2
            wy = y + (cell_size - window_size) / 2
            window_color = "#ffffff" if level > 2 else "#888888"
            svg_elements.append(f'<rect class="window" x="{wx}" y="{wy}" width="{window_size}" height="{window_size}" fill="{window_color}" rx="1"/>')
        else:
            svg_elements.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" />')

    svg_elements.append('</svg>')
    return "\n".join(svg_elements)

def main():
    levels = []
    if not TOKEN:
        print("GITHUB_TOKEN missing. Trying to fetch HTML as fallback.")
        levels = fetch_contributions_html(USERNAME)
    else:
        try:
            print(f"Fetching GraphQL data for {USERNAME}...")
            calendar_data = fetch_contributions_graphql(USERNAME, TOKEN)
            levels = get_levels_from_data(calendar_data)
        except Exception as e:
            print(f"Error fetching GraphQL: {e}")
            print("Trying HTML fallback...")
            levels = fetch_contributions_html(USERNAME)

    if not levels:
        print("Error: Could not retrieve any contribution data.")
        return

    os.makedirs("assets", exist_ok=True)
    svg_content = generate_svg(levels)
    with open("assets/gta_contribution.svg", "w") as f:
        f.write(svg_content)
    print("Updated assets/gta_contribution.svg successfully.")

if __name__ == "__main__":
    main()
