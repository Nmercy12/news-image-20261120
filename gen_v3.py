#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# Ensure output goes to repo root entry.png
OUT_PATH = "entry.png"
WIDTH, HEIGHT = 1024, 1024

# Colors
COLOR_PAPER = "#f6f1e5"
COLOR_INK = "#111111"
COLOR_RED = "#b42318"
COLOR_NAVY = "#1e3a5f"
COLOR_GREY = "#666666"

# Region Colors
REGION_COLORS = {
    "Europe": "#1d4ed8",
    "Asia-Pacific": "#b91c1c",
    "Middle East": "#a16207",
    "Africa": "#15803d",
    "Americas": "#7c3aed",
    "Oceania": "#0e7490",
    "Global": "#4b5563"
}

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
FONT_SERIF_BOLD = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
FONT_SERIF_ITALIC = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")
FONT_SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
FONT_SANS_BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_image():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_PAPER)
    draw = ImageDraw.Draw(img)

    # Fonts
    f_kicker = get_font(FONT_SANS_BOLD, 12)
    f_masthead = get_font(FONT_SERIF_BOLD, 62)
    f_subhead = get_font(FONT_SERIF_ITALIC, 18)
    f_utc = get_font(FONT_SANS_BOLD, 10.5)
    f_utc_text = get_font(FONT_SANS, 10.5)
    f_kpi_num = get_font(FONT_SANS_BOLD, 26)
    f_kpi_lbl = get_font(FONT_SANS, 9.5)
    f_region = get_font(FONT_SANS_BOLD, 12)
    
    # 1. Kicker (y 8-26)
    draw.text((16, 10), "THE WORLD IN ONE DAY", fill=COLOR_RED, font=f_kicker)
    right_kicker = "38 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    w_rk = f_kicker.getlength(right_kicker) if hasattr(f_kicker, 'getlength') else len(right_kicker)*6
    draw.text((WIDTH - 16 - w_rk, 10), right_kicker, fill=COLOR_INK, font=f_kicker)
    
    # Black rule at y 28
    draw.line([(16, 28), (WIDTH - 16, 28)], fill=COLOR_INK, width=2)

    # 2. Masthead (y 32-96)
    masthead_text = "Friday 20 November 2026"
    w_mh = f_masthead.getlength(masthead_text) if hasattr(f_masthead, 'getlength') else len(masthead_text)*30
    draw.text(((WIDTH - w_mh) // 2, 32), masthead_text, fill=COLOR_INK, font=f_masthead)

    # Sub-headline (y 100-120)
    sub_text = "Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · An AI sell-off sinks Asia's markets · UK and EU seal a deal"
    f_sub = get_font(FONT_SERIF_ITALIC, 17)
    w_sub = f_sub.getlength(sub_text) if hasattr(f_sub, 'getlength') else len(sub_text)*8
    draw.text(((WIDTH - w_sub) // 2, 98), sub_text, fill=COLOR_INK, font=f_sub)

    # Black rule at y 124
    draw.line([(16, 122), (WIDTH - 16, 122)], fill=COLOR_INK, width=1)

    # 3. THE DAY IN UTC strip (y 126-150, ONE line)
    draw.rectangle([16, 125, WIDTH - 16, 149], fill="#ece4d0")
    draw.text((20, 131), "THE DAY IN UTC:", fill=COLOR_RED, font=f_utc)
    utc_items = [
        "00:00 Kyiv bridges", "02:00 Akvan landfall", "05:30 Taiwan −6.2%",
        "05:50 Missile in Poland", "15:00 COP31 deadline", "19:10 Nvidia probe", "21:00 S&P −3.7%"
    ]
    ux = 135
    for item in utc_items:
        parts = item.split(" ", 1)
        draw.text((ux, 131), parts[0], fill=COLOR_RED, font=f_utc)
        tw = f_utc.getlength(parts[0]) if hasattr(f_utc, 'getlength') else len(parts[0])*6
        draw.text((ux + tw + 2, 131), parts[1], fill=COLOR_INK, font=f_utc_text)
        ux += tw + 2 + (f_utc_text.getlength(parts[1]) if hasattr(f_utc_text, 'getlength') else len(parts[1])*6) + 16

    # 4. KPI strip (y 152-193) - Defect 1 fixed
    draw.rectangle([16, 152, WIDTH - 16, 193], fill="#ffffff", outline="#dcd6c8")
    kpis = [
        ("3", "bridges over\nDnipro in Kyiv", True),
        ("372,000", "people moved to\nshelters pre-Akvan", False),
        ("−6.2%", "Taiwan index,\nFriday close", True),
        ("100,000", "youth visas\nin UK-EU deal", False),
        ("2.3%", "Japan consumer\ninflation in Oct", False),
        ("118", "runs by Phillips\nagainst India", False)
    ]
    kpi_w = (WIDTH - 32) / 6
    for i, (num, lbl, is_neg) in enumerate(kpis):
        kx = 16 + i * kpi_w
        if i > 0:
            draw.line([(kx, 155), (kx, 190)], fill=COLOR_RED, width=1)
        num_color = COLOR_RED if is_neg else COLOR_INK
        nw = f_kpi_num.getlength(num) if hasattr(f_kpi_num, 'getlength') else len(num)*14
        draw.text((kx + (kpi_w - nw)/2, 153), num, fill=num_color, font=f_kpi_num)
        ly = 176
        for line in lbl.split("\n"):
            lw = f_kpi_lbl.getlength(line) if hasattr(f_kpi_lbl, 'getlength') else len(line)*5
            draw.text((kx + (kpi_w - lw)/2, ly), line, fill=COLOR_INK, font=f_kpi_lbl)
            ly += 11

    # 5. Region bar (y 197-217) - Defect 2 fixed (7 segments, correct order, Global min_w 70px)
    regions = [
        ("Europe (11)", 11, REGION_COLORS["Europe"]),
        ("Asia-Pacific (9)", 9, REGION_COLORS["Asia-Pacific"]),
        ("Middle East (4)", 4, REGION_COLORS["Middle East"]),
        ("Africa (5)", 5, REGION_COLORS["Africa"]),
        ("Americas (5)", 5, REGION_COLORS["Americas"]),
        ("Oceania (3)", 3, REGION_COLORS["Oceania"]),
        ("Global (1)", 1, REGION_COLORS["Global"])
    ]
    total_stories = 38
    avail_w = WIDTH - 32
    
    raw_widths = [(count / total_stories) * avail_w for _, count, _ in regions]
    min_global_w = 70
    if raw_widths[6] < min_global_w:
        diff = min_global_w - raw_widths[6]
        raw_widths[6] = min_global_w
        take_europe = diff * (11 / 20)
        take_asia = diff * (9 / 20)
        raw_widths[0] -= take_europe
        raw_widths[1] -= take_asia

    rx = 16
    for (name, count, color_hex), seg_w in zip(regions, raw_widths):
        draw.rectangle([rx, 197, rx + seg_w, 217], fill=color_hex)
        tw = f_region.getlength(name) if hasattr(f_region, 'getlength') else len(name)*6
        if seg_w > tw + 6:
            draw.text((rx + (seg_w - tw)/2, 201), name, fill="#ffffff", font=f_region)
        rx += seg_w

    # 6. Lead row (y 221-512)
    col_w = 320
    col_gap = 16
    
    leads = [
        {
            "num": "1", "kicker": "KYIV, UKRAINE · WAR", "region": "Europe",
            "banner": "KYIV — 3 BRIDGES HIT", "caption": "Officials' count · Kyiv Independent",
            "headline": "Russian missiles hit three Kyiv bridges",
            "body": "An overnight barrage of 400+ drones and 110+ missiles, 27 ballistic, killed nine across Ukraine and cut power and water in the capital. (Kyiv Independent, BBC)",
            "badge": "OFFICIAL",
            "type": "lead1"
        },
        {
            "num": "2", "kicker": "ODISHA, INDIA · CYCLONE", "region": "Asia-Pacific",
            "banner": "CYCLONE AKVAN", "caption": "Weather office · IMD",
            "headline": "Cyclone Akvan comes ashore in eastern India",
            "body": "The storm crossed the coast near Gopalpur from about 8 am; 372,000 people were moved to shelters and 423 rescue teams deployed. No deaths reported. (IMD, PTI)",
            "badge": "OFFICIAL",
            "type": "lead2"
        },
        {
            "num": "3", "kicker": "TAIPEI · SEOUL · TOKYO · MARKETS", "region": "Asia-Pacific",
            "banner": "AI SELL-OFF", "caption": "Closing prices · Al Jazeera",
            "headline": "AI sell-off sinks Asia's stock markets",
            "body": "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide; Nvidia fell 14% on SEC probe. (Al Jazeera, AP)",
            "badge": "CONFIRMED",
            "type": "lead3"
        }
    ]

    for i, lead in enumerate(leads):
        lx = 16 + i * (col_w + col_gap)
        ly = 221
        
        draw.rectangle([lx, ly, lx + col_w, ly + 288], fill="#ffffff", outline="#dcd6c8")
        
        # (a) Red Banner
        draw.rectangle([lx, ly, lx + col_w, ly + 22], fill=COLOR_RED)
        bw = f_region.getlength(lead["banner"]) if hasattr(f_region, 'getlength') else len(lead["banner"])*7
        draw.text((lx + (col_w - bw)/2, ly + 4), lead["banner"], fill="#ffffff", font=f_region)
        
        # (b) Drawn image area
        img_y = ly + 22
        img_h = 150
        draw.rectangle([lx, img_y, lx + col_w, img_y + img_h], fill=COLOR_NAVY if lead["type"]=="lead1" or lead["type"]=="lead3" else "#e2dcc8")
        
        if lead["type"] == "lead1":
            draw.rectangle([lx+10, img_y+80, lx+col_w-10, img_y+img_h], fill="#16263b")
            for wx in range(lx+20, lx+col_w-20, 16):
                for wy in range(img_y+90, img_y+img_h-10, 12):
                    draw.rectangle([wx, wy, wx+8, wy+8], fill="#fde047")
            for bx_offset in [40, 140, 240]:
                draw.arc([lx + bx_offset, img_y+50, lx + bx_offset + 90, img_y+100], 180, 360, fill="#ffffff", width=3)
            draw.line([(lx+30, img_y+30), (lx+120, img_y+70)], fill="#facc15", width=2)
            draw.line([(lx+180, img_y+20), (lx+250, img_y+60)], fill="#facc15", width=2)
            draw.ellipse([lx+110, img_y+55, lx+135, img_y+80], fill="#ea580c")
            draw.ellipse([lx+240, img_y+45, lx+265, img_y+70], fill="#ea580c")
            
        elif lead["type"] == "lead2":
            draw.rectangle([lx+10, img_y+10, lx+col_w-10, img_y+img_h-10], fill="#cce3de")
            draw.polygon([(lx+10, img_y+10), (lx+120, img_y+10), (lx+80, img_y+img_h-10), (lx+10, img_y+img_h-10)], fill="#e3d5ca")
            draw.arc([lx+100, img_y+20, lx+280, img_y+130], 0, 360, fill="#ffffff", width=4)
            draw.arc([lx+130, img_y+35, lx+250, img_y+115], 0, 360, fill="#38bdf8", width=3)
            draw.ellipse([lx+70, img_y+85, lx+80, img_y+95], fill=COLOR_RED)
            draw.text((lx+85, img_y+83), "Gopalpur", fill=COLOR_RED, font=f_utc)
            
        elif lead["type"] == "lead3":
            draw.rectangle([lx+15, img_y+15, lx+col_w-15, img_y+img_h-15], fill="#0f172a")
            points = [(lx+25, img_y+35), (lx+90, img_y+50), (lx+160, img_y+75), (lx+230, img_y+110), (lx+295, img_y+125)]
            draw.line(points, fill=COLOR_RED, width=4)
            for pt in points:
                draw.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill="#ffffff")
            draw.text((lx+30, img_y+15), "TAIPEI −6.2%  ·  SEOUL −5.2%  ·  TOKYO −5.1%", fill="#f87171", font=f_utc)

        # (c) Caption strip
        cap_y = img_y + img_h
        draw.rectangle([lx, cap_y, lx + col_w, cap_y + 16], fill="#ece4d0")
        draw.text((lx + 6, cap_y + 2), lead["caption"], fill=COLOR_INK, font=f_utc)

        # (d) Kicker
        k_y = cap_y + 18
        ktext = f"{lead['num']}  {lead['kicker']}"
        draw.text((lx + 8, k_y), ktext, fill=COLOR_RED, font=f_region)

        # (e) Headline
        h_y = k_y + 16
        f_lead_h = get_font(FONT_SERIF_BOLD, 17)
        words = lead["headline"].split(" ")
        lines = []
        cur_line = ""
        for w in words:
            test_line = cur_line + (" " if cur_line else "") + w
            if (f_lead_h.getlength(test_line) if hasattr(f_lead_h, 'getlength') else len(test_line)*8) < col_w - 16:
                cur_line = test_line
            else:
                lines.append(cur_line)
                cur_line = w
        if cur_line:
            lines.append(cur_line)
        
        for hl in lines[:2]:
            draw.text((lx + 8, h_y), hl, fill=COLOR_INK, font=f_lead_h)
            h_y += 20

        # (f) Body
        b_y = h_y + 2
        f_lead_b = get_font(FONT_SANS, 11)
        bwords = lead["body"].split(" ")
        blines = []
        cur_line = ""
        for w in bwords:
            test_line = cur_line + (" " if cur_line else "") + w
            if (f_lead_b.getlength(test_line) if hasattr(f_lead_b, 'getlength') else len(test_line)*6) < col_w - 16:
                cur_line = test_line
            else:
                blines.append(cur_line)
                cur_line = w
        if cur_line:
            blines.append(cur_line)

        for bl in blines[:3]:
            draw.text((lx + 8, b_y), bl, fill=COLOR_INK, font=f_lead_b)
            b_y += 15

        # (g) Badge - Defect 3 fixed (measured text width, fully inside panel)
        badge_text = lead["badge"]
        bw_text = f_region.getlength(badge_text) if hasattr(f_region, 'getlength') else len(badge_text)*7
        badge_w = int(bw_text + 12)
        badge_h = 16
        bx = lx + col_w - badge_w - 6
        by = ly + 288 - badge_h - 6
        draw.rectangle([bx, by, bx + badge_w, by + badge_h], fill=COLOR_RED)
        draw.text((bx + 6, by + 2), badge_text, fill="#ffffff", font=f_region)

    # 7. Small panels (2 rows x 5 columns) - Defect 5 fixed (dense scene fills for all 10 panels)
    panels = [
        {
            "num": "4", "kicker": "BRUSSELS · DIPLOMACY",
            "banner": "UK-EU RESET", "source": "Reuters",
            "headline": "UK and EU seal a 'reset' deal",
            "body": "Food trade, youth visas, carbon link. 100,000 visas a year.",
            "badge": "CONFIRMED", "type": "p4"
        },
        {
            "num": "5", "kicker": "ANTALYA · CLIMATE",
            "banner": "COP31 DEADLINE", "source": "UN News",
            "headline": "COP31 reaches final day with no deal",
            "body": "Draft text leaves out fossil fuels; talks run past deadline.",
            "badge": "OFFICIAL", "type": "p5"
        },
        {
            "num": "6", "kicker": "EAST POLAND · SECURITY",
            "banner": "MISSILE FALL", "source": "Reuters",
            "headline": "Russian cruise missile lands in Poland",
            "body": "Fell in a field 50 km inside Poland; two airports paused.",
            "badge": "OFFICIAL", "type": "p6"
        },
        {
            "num": "7", "kicker": "CENTRAL IRAQ · SECURITY",
            "banner": "MILITIA BASE", "source": "Reuters",
            "headline": "Iraqi army enters a militia stronghold",
            "body": "Troops deploy in Jurf al-Sakhar.",
            "badge": "REPORTED", "type": "p7"
        },
        {
            "num": "8", "kicker": "ITALY · LABOUR",
            "banner": "GENERAL STRIKE", "source": "Reuters",
            "headline": "General strike over Italy's budget",
            "body": "Workers and students march in about 100 squares.",
            "badge": "REPORTED", "type": "p8"
        },
        {
            "num": "9", "kicker": "TOKYO · ECONOMY",
            "banner": "INFLATION 2.3%", "source": "Reuters",
            "headline": "Japan inflation picks up to 2.3%",
            "body": "Headline CPI 2.3% in Oct, core 2.2%. Rate rise in view.",
            "badge": "OFFICIAL", "type": "p9"
        },
        {
            "num": "10", "kicker": "SEOUL · POLITICS",
            "banner": "IMPEACH MOVE", "source": "Korea Herald",
            "headline": "Korea ruling party to impeach judge",
            "body": "It follows an overturned conviction.",
            "badge": "REPORTED", "type": "p10"
        },
        {
            "num": "11", "kicker": "TURKANA · ENERGY",
            "banner": "FIRST OIL WELL", "source": "allAfrica",
            "headline": "Kenya starts drilling first oil well",
            "body": "First crude is due on 1 December.",
            "badge": "CONFIRMED", "type": "p11"
        },
        {
            "num": "12", "kicker": "SAN SALVADOR · POLITICS",
            "banner": "THIRD TERM", "source": "AP",
            "headline": "Bukele files to run for a third term",
            "body": "The vote is set on 28 February 2027.",
            "badge": "CONFIRMED", "type": "p12"
        },
        {
            "num": "13", "kicker": "WELLINGTON · CRICKET",
            "banner": "CENTURY 118", "source": "ICC",
            "headline": "Phillips hits 118 against India",
            "body": "First NZ batter with centuries in all three formats vs India.",
            "badge": "CONFIRMED", "type": "p13"
        }
    ]

    p_w = 186
    p_gap = 10
    
    for idx, panel in enumerate(panels):
        row = idx // 5
        col = idx % 5
        px = 16 + col * (p_w + p_gap)
        py = 518 if row == 0 else 652
        ph = 130
        
        draw.rectangle([px, py, px + p_w, py + ph], fill="#ffffff", outline="#dcd6c8")
        
        strip_y = py
        draw.rectangle([px, strip_y, px + p_w, strip_y + 44], fill=COLOR_NAVY if row==0 else "#e2dcc8")
        
        # Red Banner
        draw.rectangle([px, strip_y, px + p_w, strip_y + 12], fill=COLOR_RED)
        bw = f_utc.getlength(panel["banner"]) if hasattr(f_utc, 'getlength') else len(panel["banner"])*5
        draw.text((px + (p_w - bw)/2, strip_y + 1), panel["banner"], fill="#ffffff", font=f_utc)
        
        # Rich graphical scene area (strip_y + 12 to strip_y + 32, height 20px)
        scene_y1 = strip_y + 12
        scene_y2 = strip_y + 32
        ptype = panel["type"]
        
        if ptype == "p4": # Brussels UK-EU
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#1e3a5f")
            for sx in range(px+10, px+p_w-10, 16):
                draw.ellipse([sx, scene_y1+6, sx+4, scene_y1+10], fill="#fde047")
            draw.line([(px+20, scene_y1+10), (px+p_w-20, scene_y1+10)], fill="#ffffff", width=1)
        elif ptype == "p5": # Antalya COP31
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#b45309")
            draw.ellipse([px+12, scene_y1+4, px+28, scene_y1+16], fill="#f59e0b")
            for bar_x in range(px+35, px+p_w-10, 12):
                draw.rectangle([bar_x, scene_y1+4, bar_x+8, scene_y2-4], fill="#ef4444")
        elif ptype == "p6": # East Poland Missile
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#334155")
            draw.rectangle([px+4, scene_y2-8, px+p_w-4, scene_y2-2], fill="#166534")
            draw.line([(px+15, scene_y1+4), (px+p_w-25, scene_y2-6)], fill="#ef4444", width=2)
            draw.ellipse([px+p_w-30, scene_y2-10, px+p_w-20, scene_y2-2], fill="#f59e0b")
        elif ptype == "p7": # Central Iraq Militia
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#d97706")
            draw.rectangle([px+15, scene_y1+10, px+55, scene_y2-4], fill="#475569")
            draw.rectangle([px+70, scene_y1+8, px+110, scene_y2-4], fill="#475569")
            draw.rectangle([px+125, scene_y1+12, px+165, scene_y2-4], fill="#475569")
        elif ptype == "p8": # Italy General Strike
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#1e293b")
            for bx_off in range(px+15, px+p_w-15, 25):
                draw.rectangle([bx_off, scene_y1+6, bx_off+18, scene_y2-4], fill="#dc2626")
                draw.line([(bx_off+9, scene_y1+2), (bx_off+9, scene_y1+6)], fill="#ffffff", width=1)
        elif ptype == "p9": # Tokyo Inflation
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#0f172a")
            chart_pts = [(px+10, scene_y2-6), (px+50, scene_y2-10), (px+90, scene_y1+12), (px+130, scene_y1+8), (px+p_w-10, scene_y1+4)]
            draw.line(chart_pts, fill="#22c55e", width=2)
            for pt in chart_pts:
                draw.ellipse([pt[0]-2, pt[1]-2, pt[0]+2, pt[1]+2], fill="#ffffff")
        elif ptype == "p10": # Seoul Impeach
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#475569")
            for col_x in range(px+20, px+p_w-20, 22):
                draw.rectangle([col_x, scene_y1+3, col_x+10, scene_y2-3], fill="#f8fafc")
        elif ptype == "p11": # Turkana Kenya oil
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#ca8a04")
            draw.polygon([(px+70, scene_y1+2), (px+90, scene_y2-2), (px+50, scene_y2-2)], fill="#1e293b")
            draw.line([(px+70, scene_y1+2), (px+70, scene_y2-2)], fill="#ffffff", width=1)
        elif ptype == "p12": # San Salvador Bukele
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#0284c7")
            draw.rectangle([px+50, scene_y1+6, px+p_w-50, scene_y2-4], fill="#ffffff")
            draw.rectangle([px+70, scene_y1+10, px+90, scene_y1+12], fill="#0f172a")
        elif ptype == "p13": # Wellington Cricket
            draw.rectangle([px+4, scene_y1+2, px+p_w-4, scene_y2-2], fill="#15803d")
            draw.rectangle([px+40, scene_y1+8, px+p_w-40, scene_y2-8], fill="#fef08a")
            draw.arc([px+30, scene_y1+2, px+p_w-30, scene_y2+10], 180, 360, fill="#ffffff", width=2)

        # Source strip
        draw.rectangle([px, strip_y + 32, px + p_w, strip_y + 44], fill="#ece4d0")
        draw.text((px + 4, strip_y + 33), f"Source: {panel['source']}", fill=COLOR_INK, font=f_utc)

        ky = strip_y + 46
        draw.text((px + 4, ky), f"{panel['num']}  {panel['kicker']}", fill=COLOR_RED, font=f_utc)

        hy = ky + 12
        f_ph = get_font(FONT_SERIF_BOLD, 13)
        words = panel["headline"].split(" ")
        plines = []
        cur_line = ""
        for w in words:
            test_line = cur_line + (" " if cur_line else "") + w
            if (f_ph.getlength(test_line) if hasattr(f_ph, 'getlength') else len(test_line)*6) < p_w - 8:
                cur_line = test_line
            else:
                plines.append(cur_line)
                cur_line = w
        if cur_line:
            plines.append(cur_line)

        for pl in plines[:2]:
            draw.text((px + 4, hy), pl, fill=COLOR_INK, font=f_ph)
            hy += 14

        by_text = hy + 2
        f_pb = get_font(FONT_SANS, 9.5)
        bwords = panel["body"].split(" ")
        blines = []
        cur_line = ""
        for w in bwords:
            test_line = cur_line + (" " if cur_line else "") + w
            if (f_pb.getlength(test_line) if hasattr(f_pb, 'getlength') else len(test_line)*5) < p_w - 8:
                cur_line = test_line
            else:
                blines.append(cur_line)
                cur_line = w
        if cur_line:
            blines.append(cur_line)

        for bl in blines[:2]:
            draw.text((px + 4, by_text), bl, fill=COLOR_INK, font=f_pb)
            by_text += 12

        # Badge - Defect 3 fixed (measured text width, fully inside panel)
        badge_text = panel["badge"]
        bw_text = f_utc.getlength(badge_text) if hasattr(f_utc, 'getlength') else len(badge_text)*5.5
        badge_w = int(bw_text + 8)
        badge_h = 13
        bx_b = px + p_w - badge_w - 4
        by_b = py + ph - badge_h - 4
        draw.rectangle([bx_b, by_b, bx_b + badge_w, by_b + badge_h], fill=COLOR_RED)
        draw.text((bx_b + 4, by_b + 1), badge_text, fill="#ffffff", font=f_utc)

    # 8. Map + ALSO ON (y 788-958) - Defect 4 & Defect 6 fixed
    map_y = 788
    map_h = 168
    draw.rectangle([16, map_y, WIDTH - 16, map_y + map_h], fill="#ffffff", outline="#dcd6c8")
    
    # Map area (Defect 6: darker/warmer tan continents, ocean background, larger pins)
    draw.rectangle([16, map_y, 330, map_y + map_h], fill="#d9c9b0")
    draw.text((22, map_y + 6), "WHERE IT HAPPENED (1–13)", fill=COLOR_RED, font=f_region)
    draw.rectangle([30, map_y + 30, 316, map_y + 130], fill="#c8b196")
    draw.ellipse([45, map_y + 45, 95, map_y + 90], fill="#b8977a")
    draw.ellipse([140, map_y + 35, 190, map_y + 85], fill="#b8977a")
    draw.ellipse([210, map_y + 40, 280, map_y + 100], fill="#b8977a")
    
    pins = [
        (1, 150, 45), (2, 240, 85), (3, 260, 75), (4, 155, 38),
        (5, 170, 50), (6, 165, 40), (7, 190, 60), (8, 148, 48),
        (9, 275, 68), (10, 265, 65), (11, 175, 105), (12, 55, 80), (13, 290, 115)
    ]
    for pnum, px_off, py_off in pins:
        draw.ellipse([px_off - 5, py_off - 5 + map_y, px_off + 5, py_off + 5 + map_y], fill=COLOR_RED)
        draw.text((px_off + 7, py_off - 7 + map_y), str(pnum), fill=COLOR_INK, font=f_region)
    
    draw.text((22, map_y + 138), "Each number links to a story on this page.", fill=COLOR_GREY, font=f_utc)

    # ALSO ON area (Defect 4: word wrapping for all briefs so brief #34 and others fit inside column right edge x=1008)
    draw.rectangle([340, map_y, WIDTH - 16, map_y + map_h], fill="#ffffff")
    draw.text((350, map_y + 6), "ALSO ON FRIDAY 20 NOVEMBER — 25 MORE STORIES (14–38)", fill=COLOR_RED, font=f_region)
    
    briefs = [
        (14, "Lviv: A strike on a railway station kills two", "Europe", "(BBC)"),
        (15, "Moscow: Russia declares Estonia border shut", "Europe", "(Reuters)"),
        (16, "Berlin: School pupils strike against military service", "Europe", "(Al Jazeera)"),
        (17, "London: General says UK runs cyber attacks abroad", "Europe", "(Sky News)"),
        (18, "Beijing: China holds loan rates for an 18th month", "Asia-Pacific", "(Xinhua)"),
        (19, "Tokyo: SoftBank shares fall more than 14%", "Asia-Pacific", "(Al Jazeera)"),
        (20, "Seoul: KOSPI index ends the week 7.9% lower", "Asia-Pacific", "(Anadolu)"),
        (21, "Ganjam: 209 mm of rain as Akvan crosses", "Asia-Pacific", "(PTI)"),
        (22, "Lebanon: Israeli air strikes hit the south and east", "Middle East", "(Anadolu)"),
        (23, "Yemen: Gunmen fire on a cargo ship off the coast", "Middle East", "(UKMTO)"),
        (24, "Abuja: Court bars new evidence against Tinubu", "Africa", "(Channels TV)"),
        (25, "Kampala: Police told to enforce Ebola ban on rallies", "Africa", "(allAfrica)"),
        (26, "Malawi: Fuel crisis brings night-long queues", "Africa", "(Al Jazeera)"),
        (27, "Africa: AfDB says 22 countries near debt distress", "Africa", "(allAfrica)"),
        (28, "New York: Nasdaq futures fall 1.6% before the bell", "Americas", "(24/7 Wall St)"),
        (29, "Washington: Democrats query law firm's free work", "Americas", "(Al Jazeera)"),
        (30, "Sydney: Australian shares fall 1.8% in the sell-off", "Oceania", "(Reuters)"),
        (31, "Wellington: Nicholls makes 175 in a 216-run stand", "Oceania", "(ICC)"),
        (32, "Antalya: Panama asks COP31 to cap world oil output", "Europe", "(Anadolu)"),
        (33, "Turin: ATP backs plan to lift player pay past $350m", "Europe", "(Anadolu)"),
        (34, "Hormuz: Tanker set ablaze off Oman; Iran's Guards blame a mine", "Middle East", "(UKMTO)"),
        (35, "New Delhi: Pakistan PM visits, first since May clash", "Asia-Pacific", "(PTI/Dawn)"),
        (36, "Health: Cancer pill, 60.7% respond in 61-patient trial", "Global", "(Reuters)"),
        (37, "Buenos Aires: Argentina's country risk tops 1,070", "JPM", "(JPM)"),
        (38, "Las Vegas: Russell fastest in wet GP practice", "Americas", "(F1.com)")
    ]

    col1 = briefs[:13]
    col2 = briefs[13:]

    def draw_brief_column(items, start_x, start_y, col_width=315):
        by = start_y
        f_brief = get_font(FONT_SANS, 9.5)
        for num, text, reg, src in items:
            color = REGION_COLORS.get(reg, COLOR_INK)
            num_str = f"{num}."
            draw.text((start_x, by), num_str, fill=color, font=f_region)
            full_text = f"{text} {src}"
            
            max_w = col_width - 26
            words = full_text.split(" ")
            lines = []
            cur_line = ""
            for w in words:
                test_line = cur_line + (" " if cur_line else "") + w
                tw = f_brief.getlength(test_line) if hasattr(f_brief, 'getlength') else len(test_line)*5
                if tw < max_w:
                    cur_line = test_line
                else:
                    if cur_line:
                        lines.append(cur_line)
                    cur_line = w
            if cur_line:
                lines.append(cur_line)
            
            for line_idx, line in enumerate(lines):
                draw.text((start_x + 26, by), line, fill=COLOR_INK, font=f_brief)
                if line_idx < len(lines) - 1:
                    by += 10
            by += 10.5

    draw_brief_column(col1, 350, map_y + 24)
    draw_brief_column(col2, 680, map_y + 24)

    # 9. DATE CHECK (y 960-984) - Defect 7 fixed
    date_check_y = 960
    draw.rectangle([16, date_check_y, WIDTH - 16, date_check_y + 22], outline=COLOR_RED, width=1, fill="#fdfbf7")
    dc_label = "DATE CHECK:"
    draw.text((22, date_check_y + 4), dc_label, fill=COLOR_RED, font=f_region)
    dc_text = "Left out as Thursday 19 November's news: the World Court's ruling on Myanmar, the three-leader declaration in Shenzhen, Tonga's drought emergency and the migrant boat lost off Senegal. Not yet happened, so not shown: BepiColombo's Mercury orbit entry and any final COP31 text."
    
    lbl_w = f_region.getlength(dc_label) if hasattr(f_region, 'getlength') else len(dc_label)*7
    dc_x = 22 + lbl_w + 6
    max_w = (WIDTH - 16) - dc_x - 6
    
    dc_font_size = 11.5
    while dc_font_size >= 10.0:
        f_dc = get_font(FONT_SANS, dc_font_size)
        if hasattr(f_dc, 'getlength'):
            tw = f_dc.getlength(dc_text)
        elif hasattr(f_dc, 'getbbox'):
            bbox = f_dc.getbbox(dc_text)
            tw = bbox[2] - bbox[0] if bbox else len(dc_text) * 5
        else:
            tw = len(dc_text) * 5
        if tw <= max_w:
            break
        dc_font_size -= 0.25
    f_dc = get_font(FONT_SANS, max(10.0, dc_font_size))
    draw.text((dc_x, date_check_y + 5), dc_text, fill=COLOR_INK, font=f_dc)

    # 10. Footer (y 988-1008)
    footer_y = 988
    f_footer = get_font(FONT_SANS, 9.5)
    footer_left = "Every story here happened, or was first reported, on Friday 20 November 2026. Officials' counts attributed."
    footer_right = "Sources named beside each story · original drawings"
    draw.text((16, footer_y), footer_left, fill=COLOR_GREY, font=f_footer)
    w_fr = f_footer.getlength(footer_right) if hasattr(f_footer, 'getlength') else len(footer_right)*5
    draw.text((WIDTH - 16 - w_fr, footer_y), footer_right, fill=COLOR_GREY, font=f_footer)

    img.save(OUT_PATH, "PNG", optimize=True)
    print(f"Successfully generated {OUT_PATH}")

if __name__ == "__main__":
    create_image()
