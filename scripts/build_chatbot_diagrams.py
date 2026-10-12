import os
import math
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

os.makedirs('reports/figures_chatbot', exist_ok=True)
DESKTOP_DIR = r"C:\Users\satis\OneDrive\Desktop"

plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'

# =============================================================
# 1. DFD LEVEL 0 (CONTEXT LEVEL DIAGRAM - CHATBOT)
# =============================================================
def build_chatbot_dfd_level0():
    fig, ax = plt.subplots(figsize=(18, 10.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    ax.set_xlim(0, 18)
    ax.set_ylim(1.0, 11.4)
    ax.axis('off')
    
    font = 'Segoe UI'
    
    # Title Block
    title_box = FancyBboxPatch((3.5, 10.15), 11.0, 0.95,
                               boxstyle="round,pad=0.08,rounding_size=0.15",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    
    ax.text(9.0, 10.72, "DFD Level 0 – Context Diagram", 
            ha='center', va='center', fontsize=22, fontweight='bold', 
            color='#0F172A', fontfamily=font)
    
    ax.text(9.0, 10.32, "Movie Recommender Chatbot (Conversational AI System)", 
            ha='center', va='center', fontsize=14, fontweight='bold', 
            color='#1E40AF', fontfamily=font)

    # External Entity: [ USER ] (Left)
    ent_w = 3.6
    ent_h = 7.0
    ent_x = 1.0
    ent_y = 1.9
    
    # Soft drop-shadow
    ax.add_patch(patches.Rectangle((ent_x + 0.08, ent_y - 0.08), ent_w, ent_h,
                                   facecolor='#94A3B8', edgecolor='none', alpha=0.18))
    
    # External Entity Rectangle
    rect_ent = patches.Rectangle((ent_x, ent_y), ent_w, ent_h,
                                 facecolor='#F8FAFC', edgecolor='#1D4ED8', linewidth=2.8)
    ax.add_patch(rect_ent)
    
    ax.plot([ent_x + 0.22, ent_x + 0.22], [ent_y + 0.25, ent_y + ent_h - 0.25], 
            color='#93C5FD', lw=2.2, linestyle='--')
    
    ax.text(ent_x + ent_w / 2.0, ent_y + ent_h - 0.75, "External Entity", 
            ha='center', va='center', fontsize=11.5, fontweight='bold', 
            color='#3B82F6', fontfamily=font)
    
    ax.plot([ent_x + 0.5, ent_x + ent_w - 0.5], [ent_y + ent_h - 1.15, ent_y + ent_h - 1.15],
            color='#BFDBFE', lw=1.5)
    
    ax.text(ent_x + ent_w / 2.0, ent_y + ent_h / 2.0 + 0.2, "USER", 
            ha='center', va='center', fontsize=26, fontweight='bold', 
            color='#1E3A8A', fontfamily=font)
    ax.text(ent_x + ent_w / 2.0, ent_y + ent_h / 2.0 - 0.6, "(Movie Explorer)", 
            ha='center', va='center', fontsize=13, fontweight='bold', 
            color='#475569', fontfamily=font)

    # Process Circle 0.0: [ MOVIE RECOMMENDER CHATBOT ] (Right)
    proc_cx = 14.5
    proc_cy = 5.4
    proc_r = 3.0
    
    circle_shadow = patches.Circle((proc_cx + 0.08, proc_cy - 0.08), proc_r, 
                                   facecolor='#94A3B8', edgecolor='none', alpha=0.18)
    ax.add_patch(circle_shadow)
    
    proc_circle = patches.Circle((proc_cx, proc_cy), proc_r, 
                                 facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=3.2)
    ax.add_patch(proc_circle)
    
    div_y = proc_cy + 1.25
    chord_w = 2.0 * math.sqrt(proc_r**2 - (div_y - proc_cy)**2)
    ax.plot([proc_cx - chord_w / 2.0 + 0.2, proc_cx + chord_w / 2.0 - 0.2], [div_y, div_y], 
            color='#86EFAC', lw=2.0)
    
    ax.text(proc_cx, proc_cy + 2.05, "0.0", 
            ha='center', va='center', fontsize=20, fontweight='bold', 
            color='#15803D', fontfamily=font)
    
    ax.text(proc_cx, proc_cy + 0.55, "Movie Recommender", 
            ha='center', va='center', fontsize=16.5, fontweight='bold', 
            color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 0.05, "Chatbot System", 
            ha='center', va='center', fontsize=16.5, fontweight='bold', 
            color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 0.65, "(Gemini AI & Tools)", 
            ha='center', va='center', fontsize=14, fontweight='bold', 
            color='#15803D', fontfamily=font)

    x_user = ent_x + ent_w # 4.6
    
    # FLOW 1: SINGLE DIRECTED INPUT ARROW (USER -> CHATBOT)
    y_in = 6.4
    dy_in = y_in - proc_cy
    dx_in = math.sqrt(proc_r**2 - dy_in**2)
    x_target_in = proc_cx - dx_in
    
    ax.plot(x_user, y_in, marker='o', markersize=7, color='#1D4ED8')
    ax.annotate('', xy=(x_target_in, y_in), xytext=(x_user, y_in),
                arrowprops=dict(arrowstyle='->,head_width=0.75,head_length=0.9', 
                                color='#2563EB', lw=3.0))
    
    input_flows = [
        "Natural Language Chat Queries & Prompts",
        "Genre, Actor & Mood Preference Requests",
        "Movie Synopsis & Detail Inquiries",
        "Watchlist Bookmarking & Feedback Actions"
    ]
    
    label_center_x = (x_user + x_target_in) / 2.0
    
    for i, item in enumerate(input_flows):
        item_y = y_in + 0.28 + (3 - i) * 0.42
        ax.text(label_center_x, item_y, f"•  {item}", 
                ha='center', va='bottom', fontsize=11.5, fontweight='bold', 
                color='#1E3A8A', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.20', facecolor='#EFF6FF', edgecolor='#DBEAFE', lw=0.8))

    # FLOW 2: SINGLE DIRECTED OUTPUT ARROW (CHATBOT -> USER)
    y_out = 4.4
    dy_out = y_out - proc_cy
    dx_out = math.sqrt(proc_r**2 - dy_out**2)
    x_source_out = proc_cx - dx_out
    
    ax.plot(x_source_out, y_out, marker='o', markersize=6.5, color='#16A34A')
    ax.plot(x_user, y_out, marker='o', markersize=7, color='#059669')
    
    ax.annotate('', xy=(x_user, y_out), xytext=(x_source_out, y_out),
                arrowprops=dict(arrowstyle='->,head_width=0.75,head_length=0.9', 
                                color='#059669', lw=3.0))
    
    output_flows = [
        "Conversational AI Explanations & Dialogue",
        "Tailored Movie Recommendation Cards & Posters",
        "Film Synopses, Cast Info & Rating Overlays",
        "Updated User Taste Radar Analytics & History"
    ]
    
    label_center_out = (x_user + x_source_out) / 2.0
    
    for i, item in enumerate(output_flows):
        item_y = y_out - 0.28 - i * 0.42
        ax.text(label_center_out, item_y, f"•  {item}", 
                ha='center', va='top', fontsize=11.5, fontweight='bold', 
                color='#065F46', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.20', facecolor='#F0FDF4', edgecolor='#D1FAE5', lw=0.8))

    plt.tight_layout()
    p1 = 'reports/figures_chatbot/dfd_level_0.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_0_Movie_Recommender_Chatbot.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Chatbot DFD Level 0 to", p1, "and", p2)

# =============================================================
# 2. DFD LEVEL 1 (FUNCTIONAL DECOMPOSITION - CHATBOT)
# =============================================================
def draw_gane_sarson_store(ax, x, y, width, height, ds_id, ds_name, font='Segoe UI'):
    rect_bg = patches.Rectangle((x, y - height / 2.0), width, height,
                                facecolor='#FFFBEB', edgecolor='none', alpha=0.98)
    ax.add_patch(rect_bg)
    ax.plot([x, x + width], [y + height / 2.0, y + height / 2.0], color='#B45309', lw=3.2)
    ax.plot([x, x + width], [y - height / 2.0, y - height / 2.0], color='#B45309', lw=3.2)
    ax.plot([x, x], [y - height / 2.0, y + height / 2.0], color='#B45309', lw=3.2)
    id_w = 2.40
    ax.plot([x + id_w, x + id_w], [y - height / 2.0, y + height / 2.0], color='#D97706', lw=2.6)
    ax.text(x + id_w / 2.0, y, ds_id, ha='center', va='center',
            fontsize=32.0, fontweight='bold', color='#B45309', fontfamily=font)
    ax.text(x + id_w + 0.45, y, ds_name, ha='left', va='center',
            fontsize=26.0, fontweight='bold', color='#78350F', fontfamily=font)

def draw_dfd1_process(ax, cx, cy, r, proc_id, line1, line2='', font='Segoe UI'):
    circle_shadow = patches.Circle((cx + 0.10, cy - 0.10), r, 
                                   facecolor='#94A3B8', edgecolor='none', alpha=0.22)
    ax.add_patch(circle_shadow)
    proc_circle = patches.Circle((cx, cy), r, 
                                 facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=3.6)
    ax.add_patch(proc_circle)
    div_y = cy + r * 0.42
    chord_w = 2.0 * math.sqrt(r**2 - (div_y - cy)**2)
    ax.plot([cx - chord_w / 2.0 + 0.12, cx + chord_w / 2.0 - 0.12], [div_y, div_y], 
            color='#86EFAC', lw=2.6)
    ax.text(cx, cy + r * 0.68, proc_id, ha='center', va='center',
            fontsize=31.0, fontweight='bold', color='#15803D', fontfamily=font)
    if line2:
        ax.text(cx, cy - 0.08, line1, ha='center', va='center', 
                fontsize=24.0, fontweight='bold', color='#064E3B', fontfamily=font)
        ax.text(cx, cy - 0.68, line2, ha='center', va='center', 
                fontsize=24.0, fontweight='bold', color='#064E3B', fontfamily=font)
    else:
        ax.text(cx, cy - 0.35, line1, ha='center', va='center', 
                fontsize=26.0, fontweight='bold', color='#064E3B', fontfamily=font)

def build_chatbot_dfd_level1():
    fig, ax = plt.subplots(figsize=(36.0, 26.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    ax.set_xlim(0, 36.0)
    ax.set_ylim(-0.2, 26.0)
    ax.axis('off')
    font = 'Segoe UI'
    
    title_box = FancyBboxPatch((7.5, 23.9), 21.0, 1.45,
                               boxstyle="round,pad=0.08,rounding_size=0.16",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.6)
    ax.add_patch(title_box)
    
    ax.text(18.0, 24.75, "DFD Level 1 – Movie Recommender Chatbot System", 
            ha='center', va='center', fontsize=26.0, fontweight='bold', 
            color='#0F172A', fontfamily=font)
    
    ax.text(18.0, 24.25, "Decomposed Level 1 Architecture: 5 Core Processes, 1 External Entity (E1) & 5 Implemented Database Tables", 
            ha='center', va='center', fontsize=14.0, fontweight='bold', 
            color='#1E40AF', fontfamily=font)

    # External Entity: E1 USER
    ent_w = 3.6
    ent_h = 22.4
    ent_x = 0.9
    ent_y = 0.6
    
    ax.add_patch(patches.Rectangle((ent_x + 0.1, ent_y - 0.1), ent_w, ent_h,
                                   facecolor='#94A3B8', edgecolor='none', alpha=0.20))
    rect_ent = patches.Rectangle((ent_x, ent_y), ent_w, ent_h,
                                 facecolor='#F8FAFC', edgecolor='#1D4ED8', linewidth=3.2)
    ax.add_patch(rect_ent)
    
    ax.plot([ent_x + 0.25, ent_x + 0.25], [ent_y + 0.30, ent_y + ent_h - 0.30], 
            color='#93C5FD', lw=2.4, linestyle='--')
    
    cy_ent = ent_y + ent_h / 2.0
    ax.text(ent_x + ent_w / 2.0, cy_ent + 1.20, "E1", 
            ha='center', va='center', fontsize=28.0, fontweight='bold', 
            color='#2563EB', fontfamily=font)
    ax.text(ent_x + ent_w / 2.0, cy_ent - 0.50, "USER", 
            ha='center', va='center', fontsize=34.0, fontweight='bold', 
            color='#1E3A8A', fontfamily=font)
    ax.text(ent_x + ent_w / 2.0, cy_ent - 1.80, "(Chatbot Client)", 
            ha='center', va='center', fontsize=18.0, fontweight='bold', 
            color='#475569', fontfamily=font)

    # 5 Processes (Middle Column)
    p_cx = 13.5
    p_r = 1.95
    p_y = [21.0, 16.4, 11.8, 7.2, 2.6]
    
    draw_dfd1_process(ax, p_cx, p_y[0], p_r, "1.0", "User Auth &", "Session Management")
    draw_dfd1_process(ax, p_cx, p_y[1], p_r, "2.0", "NLU & Natural Language", "Intent Parsing")
    draw_dfd1_process(ax, p_cx, p_y[2], p_r, "3.0", "Conversational AI Agent", "(Gemini LLM & Tools)")
    draw_dfd1_process(ax, p_cx, p_y[3], p_r, "4.0", "Recommendation Engine", "& Catalog Query")
    draw_dfd1_process(ax, p_cx, p_y[4], p_r, "5.0", "Chat History & Memory", "Persistence Engine")

    # 5 Gane-Sarson Stores (Right Column)
    s_x = 23.5
    s_w = 11.0
    s_h = 1.7
    
    draw_gane_sarson_store(ax, s_x, p_y[0], s_w, s_h, "D1", "users (Auth Accounts)")
    draw_gane_sarson_store(ax, s_x, p_y[1], s_w, s_h, "D2", "movies (Metadata & Features)")
    draw_gane_sarson_store(ax, s_x, p_y[2], s_w, s_h, "D3", "chat_sessions (Multi-Turn History)")
    draw_gane_sarson_store(ax, s_x, p_y[3], s_w, s_h, "D4", "ratings (User Preferences)")
    draw_gane_sarson_store(ax, s_x, p_y[4], s_w, s_h, "D5", "watchlist (Bookmarked Movies)")

    left_flows = [
        ("Login & Signup Request", "Authentication Token & Session", p_y[0]),
        ("Natural Language Chat Query", "Extracted Intent & Entities", p_y[1]),
        ("Conversational Recommendation Request", "AI Response & Movie Cards", p_y[2]),
        ("Ask for Details / Genre Filter", "Matched Movie Catalog Items", p_y[3]),
        ("Chat History Retrieval & Clear", "Past Session Messages & Context", p_y[4])
    ]
    
    x_ent_edge = ent_x + ent_w
    
    for req, res, cy in left_flows:
        ax.annotate('', xy=(p_cx - p_r, cy + 0.45), xytext=(x_ent_edge, cy + 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
        ax.text((x_ent_edge + p_cx - p_r) / 2.0, cy + 0.85, f"• {req}",
                ha='center', va='bottom', fontsize=12.5, fontweight='bold', color='#1E3A8A', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))
        
        ax.annotate('', xy=(x_ent_edge, cy - 0.45), xytext=(p_cx - p_r, cy - 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#059669', lw=2.6))
        ax.text((x_ent_edge + p_cx - p_r) / 2.0, cy - 0.85, f"• {res}",
                ha='center', va='top', fontsize=12.5, fontweight='bold', color='#065F46', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.0))

    right_flows = [
        ("Verify / Create User Credentials", "User Session Record", p_y[0]),
        ("Query Genre & Title Index", "Token Match & Feature Vectors", p_y[1]),
        ("Read/Write Multi-Turn Context", "Historical Conversation Context", p_y[2]),
        ("Execute Recommendation Query", "Top-N Movie Records & Posters", p_y[3]),
        ("Persist Chat Turn & Watchlist", "Saved Message Timestamp & Status", p_y[4])
    ]
    
    for req, res, cy in right_flows:
        ax.annotate('', xy=(s_x, cy + 0.45), xytext=(p_cx + p_r, cy + 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
        ax.text((p_cx + p_r + s_x) / 2.0, cy + 0.85, f"• {req}",
                ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))
        
        ax.annotate('', xy=(p_cx + p_r, cy - 0.45), xytext=(s_x, cy - 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#B45309', lw=2.6))
        ax.text((p_cx + p_r + s_x) / 2.0, cy - 0.85, f"• {res}",
                ha='center', va='top', fontsize=12.0, fontweight='bold', color='#78350F', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFBEB', edgecolor='#FCD34D', lw=1.0))

    plt.tight_layout()
    p1 = 'reports/figures_chatbot/dfd_level_1.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_1_Movie_Recommender_Chatbot.png')
    fig.savefig(p1, bbox_inches='tight', pad_inches=0.35, dpi=300)
    fig.savefig(p2, bbox_inches='tight', pad_inches=0.35, dpi=300)
    plt.close()
    print("Saved Chatbot DFD Level 1 to", p1, "and", p2)

# =============================================================
# 3. DFD LEVEL 2 (PROCESS 3.0: CONVERSATIONAL AI & TOOL PIPELINE)
# =============================================================
def draw_dfd2_store(ax, x, y, width, height, ds_id, ds_name, font='Segoe UI'):
    rect_bg = patches.Rectangle((x, y - height / 2.0), width, height,
                                facecolor='#FFFBEB', edgecolor='none', alpha=0.98)
    ax.add_patch(rect_bg)
    ax.plot([x, x + width], [y + height / 2.0, y + height / 2.0], color='#B45309', lw=2.8)
    ax.plot([x, x + width], [y - height / 2.0, y - height / 2.0], color='#B45309', lw=2.8)
    ax.plot([x, x], [y - height / 2.0, y + height / 2.0], color='#B45309', lw=2.8)
    id_w = 1.60
    ax.plot([x + id_w, x + id_w], [y - height / 2.0, y + height / 2.0], color='#D97706', lw=2.2)
    ax.text(x + id_w / 2.0, y, ds_id, ha='center', va='center',
            fontsize=20.0, fontweight='bold', color='#B45309', fontfamily=font)
    ax.text(x + id_w + 0.30, y, ds_name, ha='left', va='center',
            fontsize=15.0, fontweight='bold', color='#78350F', fontfamily=font)

def build_chatbot_dfd_level2():
    fig, ax = plt.subplots(figsize=(30.0, 16.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    ax.set_xlim(0, 30.0)
    ax.set_ylim(1.0, 16.2)
    ax.axis('off')
    font = 'Segoe UI'
    
    # Title Block
    title_box = FancyBboxPatch((4.5, 14.7), 21.0, 1.25,
                               boxstyle="round,pad=0.08,rounding_size=0.16",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.6)
    ax.add_patch(title_box)
    
    ax.text(15.0, 15.48, "DFD Level 2 – Process 3.0: Conversational AI Agent Subsystem", 
            ha='center', va='center', fontsize=22.0, fontweight='bold', 
            color='#0F172A', fontfamily=font)
    
    ax.text(15.0, 15.02, "Decomposed Subsystem Architecture: Prompt Assembly, Gemini LLM Reasoning, Tool Execution & Output Card Formatting", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', 
            color='#1E40AF', fontfamily=font)

    # 1. External Entity: E1 USER (Left)
    ent_w = 2.8
    ent_h = 5.8
    ent_x = 0.8
    ent_y = 5.3
    
    ax.add_patch(patches.Rectangle((ent_x + 0.08, ent_y - 0.08), ent_w, ent_h,
                                   facecolor='#94A3B8', edgecolor='none', alpha=0.20))
    rect_ent = patches.Rectangle((ent_x, ent_y), ent_w, ent_h,
                                 facecolor='#F8FAFC', edgecolor='#1D4ED8', linewidth=3.0)
    ax.add_patch(rect_ent)
    
    ax.plot([ent_x + 0.22, ent_x + 0.22], [ent_y + 0.25, ent_y + ent_h - 0.25], 
            color='#93C5FD', lw=2.2, linestyle='--')
    
    ax.text(ent_x + ent_w / 2.0, ent_y + ent_h / 2.0 + 1.15, "E1", 
            ha='center', va='center', fontsize=22.0, fontweight='bold', 
            color='#2563EB', fontfamily=font)
    ax.text(ent_x + ent_w / 2.0, ent_y + ent_h / 2.0 - 0.10, "USER", 
            ha='center', va='center', fontsize=26.0, fontweight='bold', 
            color='#1E3A8A', fontfamily=font)
    ax.text(ent_x + ent_w / 2.0, ent_y + ent_h / 2.0 - 1.25, "(Chat Client)", 
            ha='center', va='center', fontsize=14.0, fontweight='bold', 
            color='#475569', fontfamily=font)

    # 2. Four Sequential Processes (y = 8.2)
    p_r = 1.95
    p_y = 8.2
    p_xs = [7.5, 14.0, 20.5, 27.0]
    
    draw_dfd1_process(ax, p_xs[0], p_y, p_r, "3.1", "Prompt Assembly &", "Context Merger")
    draw_dfd1_process(ax, p_xs[1], p_y, p_r, "3.2", "Google Gemini LLM", "Reasoning Engine")
    draw_dfd1_process(ax, p_xs[2], p_y, p_r, "3.3", "Recommender Tool", "Execution Engine")
    draw_dfd1_process(ax, p_xs[3], p_y, p_r, "3.4", "Response Formatter &", "Movie Card Builder")

    # 3. Two Gane-Sarson Data Stores (Top Level)
    draw_dfd2_store(ax, 4.6, 12.6, 5.8, 1.3, "D3", "chat_sessions (Memory)")
    draw_dfd2_store(ax, 17.6, 12.6, 5.8, 1.3, "D2", "movies (TMDB Catalog)")

    # --- FLOW 1: E1 -> 3.1 (User Natural Language Prompt) ---
    ax.annotate('', xy=(p_xs[0] - p_r, p_y), xytext=(ent_x + ent_w, p_y),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.8))
    ax.text((ent_x + ent_w + p_xs[0] - p_r) / 2.0, p_y + 0.65, "• User Natural Language Prompt", 
            ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.2))

    # --- FLOW 2: D3 -> 3.1 (History Retrieval) ---
    ax.annotate('', xy=(p_xs[0], p_y + p_r), xytext=(p_xs[0], 12.6 - 0.65),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.8))
    ax.text(p_xs[0] + 0.35, 11.0, "• Prior 10 Turns History", 
            ha='left', va='center', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.2))

    # --- FLOW 3: 3.1 -> 3.2 (Augmented Prompt with Tools) ---
    ax.annotate('', xy=(p_xs[1] - p_r, p_y), xytext=(p_xs[0] + p_r, p_y),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.8))
    ax.text((p_xs[0] + p_r + p_xs[1] - p_r) / 2.0, p_y + 0.65, "• Augmented Context Prompt", 
            ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.2))

    # --- FLOW 4: 3.2 -> 3.3 (Tool Call Payload) ---
    ax.annotate('', xy=(p_xs[2] - p_r, p_y), xytext=(p_xs[1] + p_r, p_y),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#B45309', lw=2.8))
    ax.text((p_xs[1] + p_r + p_xs[2] - p_r) / 2.0, p_y + 0.65, "• Tool Calling Schema (JSON)", 
            ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#78350F', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFBEB', edgecolor='#FCD34D', lw=1.2))

    # --- FLOW 5: D2 -> 3.3 (TF-IDF & Movie Metadata) ---
    ax.annotate('', xy=(p_xs[2], p_y + p_r), xytext=(p_xs[2], 12.6 - 0.65),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.8))
    ax.text(p_xs[2] + 0.35, 11.0, "• TF-IDF Vectors & Metadata", 
            ha='left', va='center', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.2))

    # --- FLOW 6: 3.3 -> 3.4 (Verified Match Results) ---
    ax.annotate('', xy=(p_xs[3] - p_r, p_y), xytext=(p_xs[2] + p_r, p_y),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#059669', lw=2.8))
    ax.text((p_xs[2] + p_r + p_xs[3] - p_r) / 2.0, p_y + 0.65, "• Verified Movie Candidates", 
            ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#065F46', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.2))

    # --- FLOW 7: 3.4 -> E1 (Interactive Response Return Bus along bottom) ---
    y_bus_bottom = 2.4
    ax.plot([p_xs[3], p_xs[3]], [p_y - p_r, y_bus_bottom], color='#059669', lw=2.6)
    ax.plot([p_xs[3], ent_x + ent_w / 2.0], [y_bus_bottom, y_bus_bottom], color='#059669', lw=2.6)
    ax.annotate('', xy=(ent_x + ent_w / 2.0, ent_y), xytext=(ent_x + ent_w / 2.0, y_bus_bottom),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#059669', lw=2.8))
    
    ax.text(15.0, y_bus_bottom - 0.45, "• Interactive MovieBot Dialogue, Tailored Movie Cards, High-Res Posters & Watchlist Actions", 
            ha='center', va='top', fontsize=13.0, fontweight='bold', color='#065F46', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.4))

    # --- FLOW 8: 3.4 -> D3 (Session History Persistence Bus along top) ---
    y_bus_top = 14.1
    ax.plot([p_xs[3], p_xs[3]], [p_y + p_r, y_bus_top], color='#7C3AED', lw=2.4)
    ax.plot([p_xs[3], p_xs[0]], [y_bus_top, y_bus_top], color='#7C3AED', lw=2.4)
    ax.annotate('', xy=(p_xs[0], 12.6 + 0.65), xytext=(p_xs[0], y_bus_top),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#7C3AED', lw=2.6))
    
    ax.text(17.2, y_bus_top + 0.30, "• Append Assistant Response & Update Multi-Turn Session Memory Buffer", 
            ha='center', va='bottom', fontsize=12.5, fontweight='bold', color='#7C3AED', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.24', facecolor='#F5F3FF', edgecolor='#DDD6FE', lw=1.2))

    plt.tight_layout()
    p1 = 'reports/figures_chatbot/dfd_level_2.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_2_Movie_Recommender_Chatbot.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Chatbot DFD Level 2 to", p1, "and", p2)

# =============================================================
# 4. ER DIAGRAM (ACADEMIC RELATIONAL TABLE CARDS - CHATBOT)
# =============================================================
def build_chatbot_er_diagram():
    fig, ax = plt.subplots(figsize=(22, 14), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 22)
    ax.set_ylim(0.5, 14.5)
    ax.axis('off')
    font = 'Segoe UI'

    title_box = FancyBboxPatch((4.0, 13.0), 14.0, 1.0, boxstyle="round,pad=0.08,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    ax.text(11.0, 13.65, "Entity-Relationship (ER) Diagram", ha='center', va='center', fontsize=22, fontweight='bold', color='#0F172A', fontfamily=font)
    ax.text(11.0, 13.25, "Academic Relational Model | Movie Recommender Chatbot System | Solid: PK, Dashed: FK", ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1E40AF', fontfamily=font)

    def draw_table_card(x, y, w, h, title, category, cols, header_bg='#1E3A8A', border_c='#1E40AF'):
        ax.add_patch(FancyBboxPatch((x - w/2.0 + 0.08, y - h/2.0 - 0.08), w, h, boxstyle="round,pad=0.04,rounding_size=0.15", facecolor='#94A3B8', edgecolor='none', alpha=0.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x - w/2.0, y - h/2.0), w, h, boxstyle="round,pad=0.04,rounding_size=0.15", facecolor='#FFFFFF', edgecolor=border_c, lw=2.4, zorder=3))
        header_h = 1.0
        ax.add_patch(FancyBboxPatch((x - w/2.0, y + h/2.0 - header_h), w, header_h, boxstyle="round,pad=0.02,rounding_size=0.15", facecolor=header_bg, edgecolor=border_c, lw=2.0, zorder=4))
        ax.add_patch(patches.Rectangle((x - w/2.0 + 0.03, y + h/2.0 - header_h), w - 0.06, 0.4, facecolor=header_bg, edgecolor='none', zorder=4))
        
        ax.text(x, y + h/2.0 - 0.35, title, ha='center', va='center', fontsize=14, fontweight='bold', color='#FFFFFF', fontfamily=font, zorder=5)
        ax.text(x, y + h/2.0 - 0.72, f"«{category}»", ha='center', va='center', fontsize=10, fontweight='bold', color='#93C5FD', fontfamily=font, zorder=5)
        ax.plot([x - w/2.0, x + w/2.0], [y + h/2.0 - header_h, y + h/2.0 - header_h], color=border_c, lw=2.0, zorder=5)
        
        content_top = y + h/2.0 - header_h
        row_h = (h - header_h) / max(len(cols), 1)
        
        for idx, (col_name, col_type, is_pk, is_fk) in enumerate(cols):
            row_y = content_top - (idx + 0.5) * row_h
            bg_c = '#F8FAFC' if idx % 2 == 0 else '#FFFFFF'
            ax.add_patch(patches.Rectangle((x - w/2.0 + 0.02, row_y - row_h/2.0), w - 0.04, row_h, facecolor=bg_c, edgecolor='none', zorder=4))
            
            ax.text(x - w/2.0 + 0.35, row_y, col_name, ha='left', va='center', fontsize=10.5, fontweight='bold' if (is_pk or is_fk) else 'normal', color='#0F172A', fontfamily=font, zorder=5)
            ax.text(x + w/2.0 - 0.35, row_y, col_type, ha='right', va='center', fontsize=9.5, fontstyle='italic', color='#64748B', fontfamily=font, zorder=5)
            
            tw = len(col_name) * 0.105
            if is_pk:
                ax.plot([x - w/2.0 + 0.35, x - w/2.0 + 0.35 + tw], [row_y - 0.14, row_y - 0.14], color='#0F172A', lw=1.8, zorder=6)
            elif is_fk:
                ax.plot([x - w/2.0 + 0.35, x - w/2.0 + 0.35 + tw], [row_y - 0.14, row_y - 0.14], color='#0F172A', lw=1.8, linestyle='--', zorder=6)

    # 1. users (Top Left)
    u_cols = [
        ("user_id", "INTEGER", True, False),
        ("username", "VARCHAR(50)", False, False),
        ("email", "VARCHAR(100)", False, False),
        ("password_hash", "VARCHAR(255)", False, False),
        ("created_at", "DATETIME", False, False)
    ]
    draw_table_card(4.0, 9.8, 4.4, 3.8, "users", "User Account Entity", u_cols, '#1E3A8A', '#1D4ED8')

    # 2. chat_sessions (Center Top)
    s_cols = [
        ("session_id", "VARCHAR(64)", True, False),
        ("user_id", "INTEGER", False, True),
        ("session_title", "VARCHAR(100)", False, False),
        ("created_at", "DATETIME", False, False),
        ("last_active", "DATETIME", False, False)
    ]
    draw_table_card(11.0, 9.8, 4.4, 3.8, "chat_sessions", "Multi-Turn Session", s_cols, '#065F46', '#059669')

    # 3. chat_messages (Bottom Center)
    msg_cols = [
        ("message_id", "INTEGER", True, False),
        ("session_id", "VARCHAR(64)", False, True),
        ("role", "VARCHAR(20)", False, False),
        ("content", "TEXT", False, False),
        ("tool_calls_json", "TEXT", False, False),
        ("timestamp", "DATETIME", False, False)
    ]
    draw_table_card(11.0, 3.8, 4.4, 4.4, "chat_messages", "Conversational History", msg_cols, '#065F46', '#059669')

    # 4. movies (Top Right)
    m_cols = [
        ("movie_id", "INTEGER", True, False),
        ("title", "VARCHAR(255)", False, False),
        ("release_year", "INTEGER", False, False),
        ("vote_average", "FLOAT", False, False),
        ("overview", "TEXT", False, False),
        ("poster_url", "VARCHAR(500)", False, False)
    ]
    draw_table_card(18.0, 9.8, 4.4, 4.2, "movies", "Movie Catalog Entity", m_cols, '#B45309', '#D97706')

    # 5. watchlist (Bottom Left)
    w_cols = [
        ("watchlist_id", "INTEGER", True, False),
        ("user_id", "INTEGER", False, True),
        ("movie_id", "INTEGER", False, True),
        ("added_date", "DATETIME", False, False)
    ]
    draw_table_card(4.0, 3.8, 4.4, 3.4, "watchlist", "User Bookmarks", w_cols, '#6B21A8', '#9333EA')

    # Connectors
    # users -> chat_sessions
    ax.plot([6.2, 8.8], [9.8, 9.8], color='#1E40AF', lw=2.2, zorder=2)
    ax.text(6.5, 10.1, "1", fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)
    ax.text(8.5, 10.1, "0..*", fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)
    ax.text(7.5, 9.4, "initiates", fontsize=10, fontweight='bold', ha='center', color='#475569', fontfamily=font)

    # chat_sessions -> chat_messages
    ax.plot([11.0, 11.0], [7.9, 6.0], color='#065F46', lw=2.2, zorder=2)
    ax.text(11.2, 7.5, "1", fontsize=13, fontweight='bold', color='#065F46', fontfamily=font)
    ax.text(11.2, 6.3, "1..*", fontsize=13, fontweight='bold', color='#065F46', fontfamily=font)
    ax.text(10.1, 7.0, "contains", fontsize=10, fontweight='bold', color='#475569', fontfamily=font)

    # users -> watchlist
    ax.plot([4.0, 4.0], [7.9, 5.5], color='#6B21A8', lw=2.2, zorder=2)
    ax.text(4.2, 7.5, "1", fontsize=13, fontweight='bold', color='#6B21A8', fontfamily=font)
    ax.text(4.2, 5.8, "0..*", fontsize=13, fontweight='bold', color='#6B21A8', fontfamily=font)
    ax.text(3.3, 6.7, "maintains", fontsize=10, fontweight='bold', color='#475569', fontfamily=font)

    # watchlist -> movies
    ax.plot([6.2, 18.0], [3.8, 3.8], color='#334155', lw=1.8, zorder=2)
    ax.plot([18.0, 18.0], [3.8, 7.7], color='#334155', lw=1.8, zorder=2)
    ax.text(6.5, 4.1, "0..*", fontsize=12, fontweight='bold', color='#334155', fontfamily=font)
    ax.text(18.2, 7.3, "1", fontsize=12, fontweight='bold', color='#334155', fontfamily=font)
    ax.text(12.0, 3.4, "references", fontsize=10, fontweight='bold', ha='center', color='#475569', fontfamily=font)

    plt.tight_layout()
    p1 = 'reports/figures_chatbot/er_diagram_academic.png'
    p2 = os.path.join(DESKTOP_DIR, 'ER_Diagram_Movie_Recommender_Chatbot.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Chatbot ER Diagram to", p1, "and", p2)

# =============================================================
# 5. USE CASE DIAGRAM (STANDARD UML 2.0 - CHATBOT)
# =============================================================
def build_chatbot_use_case_diagram():
    fig, ax = plt.subplots(figsize=(19, 12.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 19)
    ax.set_ylim(0.8, 12.5)
    ax.axis('off')
    font = 'Segoe UI'

    title_box = FancyBboxPatch((3.5, 11.2), 12.0, 1.0, boxstyle="round,pad=0.08,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    ax.text(9.5, 11.85, "Use Case Diagram", ha='center', va='center', fontsize=21, fontweight='bold', color='#0F172A', fontfamily=font)
    ax.text(9.5, 11.45, "Movie Recommender Chatbot | Standard UML 2.0 Specification", ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1E40AF', fontfamily=font)

    # System Boundary Box
    ax.add_patch(patches.Rectangle((4.5, 1.0), 10.0, 9.8, facecolor='#F8FAFC', edgecolor='#0284C7', lw=2.8, zorder=1))
    ax.text(9.5, 10.4, "System: Movie Recommender Chatbot Agent", ha='center', va='center', fontsize=13, fontweight='bold', color='#0369A1', fontfamily=font)

    def draw_actor(x, y, label):
        ax.add_patch(patches.Circle((x, y + 0.9), 0.35, facecolor='#E2E8F0', edgecolor='#0F172A', lw=2.2, zorder=4))
        ax.plot([x, x], [y + 0.55, y - 0.4], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x - 0.6, x + 0.6], [y + 0.2, y + 0.2], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x, x - 0.5], [y - 0.4, y - 1.1], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x, x + 0.5], [y - 0.4, y - 1.1], color='#0F172A', lw=2.2, zorder=4)
        ax.text(x, y - 1.5, label, ha='center', va='top', fontsize=11, fontweight='bold', color='#0F172A', fontfamily=font)

    draw_actor(2.0, 6.0, "USER\n(Chat Client)")
    draw_actor(17.0, 6.0, "GOOGLE GEMINI\nAPI SERVICE")

    def draw_uc(x, y, text, rx=1.45, ry=0.42, fill='#FFFFFF', border='#0284C7'):
        ax.add_patch(patches.Ellipse((x, y), rx*2, ry*2, facecolor=fill, edgecolor=border, lw=2.0, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A', fontfamily=font, zorder=4)

    # Column 1: User Direct Use Cases (x=7.2)
    draw_uc(7.2, 9.4, "Register / User Login")
    draw_uc(7.2, 8.1, "Chat in Natural Language")
    draw_uc(7.2, 6.8, "Ask for Movie Recs (Mood/Genre)")
    draw_uc(7.2, 5.5, "Inquire Film Synopsis & Cast")
    draw_uc(7.2, 4.2, "Receive AI Explanations")
    draw_uc(7.2, 2.9, "Add to Watchlist via Chat")
    draw_uc(7.2, 1.6, "View / Clear Chat History")

    # Column 2: Advanced Tool Use Cases (x=11.8)
    draw_uc(11.8, 9.4, "Process Multi-Turn LLM Prompt", fill='#EFF6FF', border='#3B82F6')
    draw_uc(11.8, 8.1, "Execute Tool: Search by Content", fill='#FEFCE8', border='#CA8A04')
    draw_uc(11.8, 6.5, "Execute Tool: Get Movie Details", fill='#FEFCE8', border='#CA8A04')
    draw_uc(11.8, 4.8, "Execute Tool: Genre Filtering", fill='#FEFCE8', border='#CA8A04')
    draw_uc(11.8, 3.2, "Generate Structured Card Output", fill='#F0FDF4', border='#16A34A')

    user_hand = (2.6, 6.2)
    for uy in [9.4, 8.1, 6.8, 5.5, 4.2, 2.9, 1.6]:
        ax.plot([user_hand[0], 5.75], [user_hand[1], uy], color='#334155', lw=1.6, zorder=2)

    gemini_hand = (16.4, 6.2)
    for gy in [9.4, 8.1, 6.5, 4.8, 3.2]:
        ax.plot([gemini_hand[0], 13.25], [gemini_hand[1], gy], color='#2563EB', lw=1.6, zorder=2)

    # Include Connectors
    ax.annotate("", xy=(10.35, 8.1), xytext=(8.65, 8.1),
                arrowprops=dict(arrowstyle="->", linestyle='--', color='#2563EB', lw=1.8, mutation_scale=12))
    ax.text(9.5, 8.4, "«include»", ha='center', va='center', fontsize=9, fontweight='bold', color='#2563EB', fontfamily=font)

    plt.tight_layout()
    p1 = 'reports/figures_chatbot/use_case_diagram.png'
    p2 = os.path.join(DESKTOP_DIR, 'Use_Case_Diagram_Movie_Recommender_Chatbot.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Chatbot Use Case Diagram to", p1, "and", p2)

if __name__ == '__main__':
    build_chatbot_dfd_level0()
    build_chatbot_dfd_level1()
    build_chatbot_dfd_level2()
    build_chatbot_er_diagram()
    build_chatbot_use_case_diagram()
