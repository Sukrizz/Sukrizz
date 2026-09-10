import os
import json
import urllib.request
import math

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

    grid_width = weeks * (cell_size + cell_gap)
    offset_x = (svg_width - grid_width) / 2
    if offset_x < padding_x:
        offset_x = padding_x

    road_y = 35
    road_height = 14
    start_y = road_y + road_height + 20

    # 1. Precalculate all valid cell coordinates in their logical 2D grid
    cells = []
    for i, level in enumerate(levels):
        week = i // 7
        day = i % 7
        x = offset_x + week * (cell_size + cell_gap) + cell_size / 2
        y = start_y + day * (cell_size + cell_gap) + cell_size / 2
        cells.append({'x': x, 'y': y, 'level': level, 'index': i})

    # 2. Build the serpentine / snake path
    points = []
    for row in range(7):
        if row % 2 == 0:
            cols = range(weeks)
        else:
            cols = range(weeks - 1, -1, -1)
            
        for col in cols:
            index = col * 7 + row
            if index < len(cells):
                points.append(cells[index])

    # 3. Calculate distance and timing
    time_per_px = 0.3 / (cell_size + cell_gap) # approx 0.3s per cell
    
    timings = [0.0]
    total_time = 0.0
    
    for i in range(1, len(points)):
        p1 = points[i-1]
        p2 = points[i]
        dist = math.hypot(p2['x'] - p1['x'], p2['y'] - p1['y'])
        total_time += dist * time_per_px
        timings.append(total_time)
        
    last_p = points[-1]
    first_p = points[0]
    
    # Exit animation (continue right if row 6, which is even, so going right)
    x_exit = last_p['x'] + 60
    y_exit = last_p['y']
    dist_exit = 60
    total_time += dist_exit * time_per_px
    time_exit = total_time
    
    # Pause out of sight
    total_time += 1.0
    time_pause_end = total_time
    
    # Entry animation (start from left to enter row 0)
    x_entry = first_p['x'] - 60
    y_entry = first_p['y']
    dist_entry = 60
    total_time += dist_entry * time_per_px
    time_loop_end = total_time
    
    total_loop_time = total_time

    # Generate CSS keyframes for the car
    car_keyframes = []
    def add_kf(percent, x, y, rot, opacity):
        car_keyframes.append(f"  {percent:.3f}% {{ transform: translate({x:.1f}px, {y:.1f}px) rotate({rot:.1f}deg); opacity: {opacity}; }}")

    # Initial frame
    add_kf(0.0, first_p['x'], first_p['y'], 0.0, 1)

    for i in range(1, len(points)):
        p_prev = points[i-1]
        p = points[i]
        percent = (timings[i] / total_loop_time) * 100
        
        dx = p['x'] - p_prev['x']
        dy = p['y'] - p_prev['y']
        
        rot = 0
        if dx > 0: rot = 0
        elif dx < 0: rot = 180
        elif dy > 0: rot = 90
        
        # Snap rotation just after leaving the previous cell to face movement direction
        percent_prev = (timings[i-1] / total_loop_time) * 100
        add_kf(percent_prev + 0.001, p_prev['x'], p_prev['y'], rot, 1)
        
        add_kf(percent, p['x'], p['y'], rot, 1)

    # Fade out and drive to exit
    percent_exit = (time_exit / total_loop_time) * 100
    add_kf(percent_exit - 0.5, x_exit - 5, y_exit, 0.0, 1) # Still visible right before exit
    add_kf(percent_exit, x_exit, y_exit, 0.0, 0)
    
    # Stay invisible until entry starts
    percent_pause_end = (time_pause_end / total_loop_time) * 100
    add_kf(percent_pause_end, x_entry, y_entry, 0.0, 0)
    
    # Drive in and fade in
    add_kf(percent_pause_end + 0.5, x_entry + 5, y_entry, 0.0, 1)
    add_kf(100.0, first_p['x'], first_p['y'], 0.0, 1)

    svg_elements = []
    svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%">')
    svg_elements.append('<style>')
    svg_elements.append('  .bg { fill: #050505; }')
    svg_elements.append(f'  .car {{ animation: drive {total_loop_time:.3f}s linear infinite; }}')
    svg_elements.append(f'  @keyframes drive {{\n' + '\n'.join(car_keyframes) + '\n  }}')
    svg_elements.append('  .window { animation: flicker 4s infinite alternate; }')
    svg_elements.append('  @keyframes flicker { 0% { opacity: 0.7; } 100% { opacity: 1; } }')
    svg_elements.append('  .text { fill: #ffffff; font-family: "Courier New", Courier, monospace; font-size: 14px; font-weight: bold; letter-spacing: 2px; }')
    svg_elements.append('</style>')
    
    svg_elements.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" rx="8" />')
    svg_elements.append(f'<text x="{padding_x}" y="25" class="text">NIGHT SHIFT // DEV</text>')

    # Draw the static grid from original cells array (so it's rendered visually normally)
    for p in cells:
        x_c, y_c, level = p['x'], p['y'], p['level']
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

    # Map explosion timings directly based on when the car visits each point in the snake path
    timing_map = {p['index']: timings[i] for i, p in enumerate(points)}

    # Add explosions for cells (using original cell list, timing looked up from map)
    for p in cells:
        x_c, y_c, level = p['x'], p['y'], p['level']
        t_start = timing_map.get(p['index'], 0)
        boom_svg = make_boom(x_c, y_c, level, t_start, total_loop_time)
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
