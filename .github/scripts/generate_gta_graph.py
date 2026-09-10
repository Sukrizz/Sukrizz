import os
import json
import urllib.request
import math
import random

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
            weekday = day["weekday"]
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

def make_boom(x, y, level, t_start, total_dur):
    boom_dur = 0.4
    
    kf1 = 0.0001
    kf_end = boom_dur / total_dur
    kf_off = kf_end + 0.0001
    
    if kf_off > 1.0:
        kf_off = 1.0
        kf_end = 0.9999
        
    group_anim = f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{kf1:.6f};{kf_end:.6f};{kf_off:.6f};1" begin="{t_start:.3f}s" dur="{total_dur:.3f}s" repeatCount="indefinite" />'
    
    elements = []
    
    if level == 0:
        elements.append(f'<circle cx="0" cy="0" r="1.5" fill="#444444" />')
        elements.append(f'<animateTransform attributeName="transform" type="scale" values="0; 1.2; 1.2; 0; 0" keyTimes="0;{kf1:.6f};{kf_end:.6f};{kf_off:.6f};1" begin="{t_start:.3f}s" dur="{total_dur:.3f}s" repeatCount="indefinite" />')
    elif level == 1:
        elements.append(f'<circle cx="0" cy="0" r="3" fill="#aaaaaa" />')
        elements.append(f'<animateTransform attributeName="transform" type="scale" values="0; 1.5; 1.5; 0; 0" keyTimes="0;{kf1:.6f};{kf_end:.6f};{kf_off:.6f};1" begin="{t_start:.3f}s" dur="{total_dur:.3f}s" repeatCount="indefinite" />')
    elif level == 2:
        elements.append(f'<path d="M-6,0 L0,-6 L6,0 L0,6 Z" fill="#ffaa00" />')
        elements.append(f'<animateTransform attributeName="transform" type="scale" values="0; 2; 2; 0; 0" keyTimes="0;{kf1:.6f};{kf_end:.6f};{kf_off:.6f};1" begin="{t_start:.3f}s" dur="{total_dur:.3f}s" repeatCount="indefinite" />')
    elif level == 3:
        elements.append(f'<circle cx="0" cy="0" r="5" fill="#ff5500" />')
        elements.append(f'<circle cx="-8" cy="-8" r="2" fill="#ffaa00" />')
        elements.append(f'<circle cx="8" cy="8" r="2" fill="#ffaa00" />')
        elements.append(f'<circle cx="-8" cy="8" r="2" fill="#ffaa00" />')
        elements.append(f'<circle cx="8" cy="-8" r="2" fill="#ffaa00" />')
        elements.append(f'<animateTransform attributeName="transform" type="scale" values="0; 2.5; 2.5; 0; 0" keyTimes="0;{kf1:.6f};{kf_end:.6f};{kf_off:.6f};1" begin="{t_start:.3f}s" dur="{total_dur:.3f}s" repeatCount="indefinite" />')
    elif level >= 4:
        elements.append(f'<path d="M-10,0 L0,-10 L10,0 L0,10 Z" fill="#ff0000" />')
        elements.append(f'<path d="M-8,-8 L8,8 M-8,8 L8,-8" stroke="#ffaa00" stroke-width="2" />')
        elements.append(f'<text x="0" y="3" font-family="monospace" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">BOOM</text>')
        elements.append(f'<animateTransform attributeName="transform" type="scale" values="0; 1.5; 1.5; 0; 0" keyTimes="0;{kf1:.6f};{kf_end:.6f};{kf_off:.6f};1" begin="{t_start:.3f}s" dur="{total_dur:.3f}s" repeatCount="indefinite" />')

    g_content = "".join(elements)
    return f'<g transform="translate({x}, {y})"><g opacity="0">{group_anim}{g_content}</g></g>'

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

    # Points for tracking car movement
    points = []
    
    grid_width = weeks * (cell_size + cell_gap)
    offset_x = (svg_width - grid_width) / 2
    if offset_x < padding_x:
        offset_x = padding_x

    road_y = 35
    road_height = 14
    start_y = road_y + road_height + 20

    for i, level in enumerate(levels):
        week = i // 7
        day = i % 7
        x = offset_x + week * (cell_size + cell_gap) + cell_size / 2
        y = start_y + day * (cell_size + cell_gap) + cell_size / 2
        points.append((x, y, level))

    time_per_cell = 0.3
    time_jump = 0.1
    time_ret = 1.0
    
    total_time = 0.0
    timings = [0.0]
    
    for i in range(1, len(points)):
        week = i // 7
        prev_week = (i - 1) // 7
        if week != prev_week:
            total_time += time_jump
        else:
            total_time += time_per_cell
        timings.append(total_time)
        
    total_time += time_ret # For return to start
    
    # Generate CSS keyframes for the car
    car_keyframes = []
    for i in range(len(points) - 1):
        p_curr = points[i]
        p_next = points[i+1]
        
        x_curr, y_curr = p_curr[0], p_curr[1]
        x_next, y_next = p_next[0], p_next[1]
        
        dx = x_next - x_curr
        dy = y_next - y_curr
        rot = math.degrees(math.atan2(dy, dx))
        
        kf_start = (timings[i] / total_time) * 100
        kf_end = (timings[i+1] / total_time) * 100
        
        car_keyframes.append(f"  {kf_start:.3f}% {{ transform: translate({x_curr:.1f}px, {y_curr:.1f}px) rotate({rot:.1f}deg); }}")
        car_keyframes.append(f"  {kf_end - 0.001:.3f}% {{ transform: translate({x_next:.1f}px, {y_next:.1f}px) rotate({rot:.1f}deg); }}")

    dx_ret = points[0][0] - points[-1][0]
    dy_ret = points[0][1] - points[-1][1]
    rot_ret = math.degrees(math.atan2(dy_ret, dx_ret))
    
    kf_start_ret = (timings[-1] / total_time) * 100
    car_keyframes.append(f"  {kf_start_ret:.3f}% {{ transform: translate({points[-1][0]:.1f}px, {points[-1][1]:.1f}px) rotate({rot_ret:.1f}deg); }}")
    car_keyframes.append(f"  100% {{ transform: translate({points[0][0]:.1f}px, {points[0][1]:.1f}px) rotate({rot_ret:.1f}deg); }}")

    svg_elements = []
    svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%">')
    svg_elements.append('<style>')
    svg_elements.append('  .bg { fill: #050505; }')
    svg_elements.append(f'  .car {{ animation: drive {total_time:.3f}s linear infinite; }}')
    svg_elements.append(f'  @keyframes drive {{\n' + '\n'.join(car_keyframes) + '\n  }}')
    svg_elements.append('  .window { animation: flicker 4s infinite alternate; }')
    svg_elements.append('  @keyframes flicker { 0% { opacity: 0.7; } 100% { opacity: 1; } }')
    svg_elements.append('  .text { fill: #ffffff; font-family: "Courier New", Courier, monospace; font-size: 14px; font-weight: bold; letter-spacing: 2px; }')
    svg_elements.append('</style>')
    
    svg_elements.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" rx="8" />')
    svg_elements.append(f'<text x="{padding_x}" y="25" class="text">NIGHT SHIFT // DEV</text>')

    # Draw grid
    for i, p in enumerate(points):
        x_c, y_c, level = p
        # Get top-left
        x = x_c - cell_size / 2
        y = y_c - cell_size / 2
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

    # Add explosions
    for i, p in enumerate(points):
        x_c, y_c, level = p
        t_start = timings[i]
        boom_svg = make_boom(x_c, y_c, level, t_start, total_time)
        svg_elements.append(boom_svg)

    # Car definition facing right (0 degrees)
    car_svg = """
    <g class="car">
      <rect x="-10" y="-4" width="20" height="8" fill="#eeeeee" rx="2" />
      <rect x="3" y="-3" width="3" height="6" fill="#000000" />
      <rect x="-8" y="-3" width="3" height="6" fill="#000000" />
      <rect x="8" y="-4" width="2" height="2" fill="#ffffff" />
      <rect x="8" y="2" width="2" height="2" fill="#ffffff" />
      <rect x="-10" y="-4" width="1" height="2" fill="#ff0000" />
      <rect x="-10" y="2" width="1" height="2" fill="#ff0000" />
      <polygon points="10,-3 35,-10 35,-1" fill="#ffffff" opacity="0.15" />
      <polygon points="10,3 35,1 35,10" fill="#ffffff" opacity="0.15" />
    </g>
    """
    svg_elements.append(car_svg)

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
