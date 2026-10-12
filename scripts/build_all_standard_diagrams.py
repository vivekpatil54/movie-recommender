import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

os.makedirs('reports/figures', exist_ok=True)
DESKTOP_DIR = r"C:\Users\satis\OneDrive\Desktop"

plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# 1. DFD LEVEL 0 (CONTEXT LEVEL DIAGRAM) - CLEAN & STANDARD
# -------------------------------------------------------------
def generate_standard_dfd_level0():
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 18)
    ax.set_ylim(1.0, 11.2)
    ax.axis('off')
    
    font = 'Segoe UI'
    
    # Title Block
    title_box = FancyBboxPatch((3.5, 9.9), 11.0, 1.0,
                               boxstyle="round,pad=0.08,rounding_size=0.15",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    ax.text(9.0, 10.5, "Data Flow Diagram (DFD) - Level 0", 
            ha='center', va='center', fontsize=21, fontweight='bold', color='#0F172A', fontfamily=font)
    ax.text(9.0, 10.1, "Context Level Diagram | Movie Recommendation and Discovery System", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)

    # External Entity: [ USER / MOVIE BUFF ] (Left)
    ent_w, ent_h = 3.6, 7.2
    ent_x, ent_y = 1.0, 1.8
    
    # Drop shadow & Box
    ax.add_patch(patches.Rectangle((ent_x + 0.08, ent_y - 0.08), ent_w, ent_h, facecolor='#94A3B8', edgecolor='none', alpha=0.18))
    ax.add_patch(patches.Rectangle((ent_x, ent_y), ent_w, ent_h, facecolor='#F8FAFC', edgecolor='#1D4ED8', lw=2.8))
    ax.plot([ent_x + 0.22, ent_x + 0.22], [ent_y + 0.25, ent_y + ent_h - 0.25], color='#93C5FD', lw=2.2, linestyle='--')
    
    ax.text(ent_x + ent_w/2.0, ent_y + ent_h - 0.75, "External Entity", ha='center', va='center', fontsize=11.5, fontweight='bold', color='#3B82F6', fontfamily=font)
    ax.plot([ent_x + 0.5, ent_x + ent_w - 0.5], [ent_y + ent_h - 1.15, ent_y + ent_h - 1.15], color='#BFDBFE', lw=1.5)
    
    ax.text(ent_x + ent_w/2.0, ent_y + ent_h/2.0 + 0.4, "USER", ha='center', va='center', fontsize=26, fontweight='bold', color='#1E3A8A', fontfamily=font)
    ax.text(ent_x + ent_w/2.0, ent_y + ent_h/2.0 - 0.3, "(Movie Explorer)", ha='center', va='center', fontsize=14, fontweight='bold', color='#475569', fontfamily=font)
    ax.text(ent_x + ent_w/2.0, ent_y + ent_h/2.0 - 1.0, "[Web Browser / Client]", ha='center', va='center', fontsize=11, color='#64748B', fontfamily=font)

    # Process Circle 0.0: [ MOVIE RECOMMENDATION SYSTEM ] (Right)
    proc_cx = 14.5
    proc_cy = 5.4
    proc_r = 2.9
    
    ax.add_patch(patches.Circle((proc_cx + 0.08, proc_cy - 0.08), proc_r, facecolor='#94A3B8', edgecolor='none', alpha=0.18))
    ax.add_patch(patches.Circle((proc_cx, proc_cy), proc_r, facecolor='#F0FDF4', edgecolor='#16A34A', lw=3.2))
    
    div_y = proc_cy + 1.25
    chord_w = 2.0 * math.sqrt(proc_r**2 - (div_y - proc_cy)**2)
    ax.plot([proc_cx - chord_w/2.0 + 0.2, proc_cx + chord_w/2.0 - 0.2], [div_y, div_y], color='#86EFAC', lw=2.0)
    
    ax.text(proc_cx, proc_cy + 1.95, "0.0", ha='center', va='center', fontsize=19, fontweight='bold', color='#15803D', fontfamily=font)
    ax.text(proc_cx, proc_cy + 0.55, "Movie", ha='center', va='center', fontsize=17, fontweight='bold', color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 0.05, "Recommendation", ha='center', va='center', fontsize=17, fontweight='bold', color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 0.65, "System", ha='center', va='center', fontsize=17, fontweight='bold', color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 1.35, "(TF-IDF, SVD & ANN)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#16A34A', fontfamily=font)

    # 6 Parallel Perfectly Horizontal Flow Lines between Entity & Process
    flows = [
        # (y_pos, is_forward, title_num, label, color, bg_pill, border_pill)
        (7.9, True, "1.", "User Registration & Login Credentials", "#1E40AF", "#EFF6FF", "#BFDBFE"),
        (6.9, True, "2.", "Movie Search Queries & Genre Filter Preferences", "#1E40AF", "#EFF6FF", "#BFDBFE"),
        (5.9, True, "3.", "1-to-5 Star User Ratings & Watchlist Additions", "#1E40AF", "#EFF6FF", "#BFDBFE"),
        (4.9, False, "4.", "Top-N Movie Recommendations & Likelihood Scores", "#15803D", "#F0FDF4", "#BBF7D0"),
        (3.9, False, "5.", "Movie Posters, Overview Synopses & Cast Details", "#15803D", "#F0FDF4", "#BBF7D0"),
        (2.9, False, "6.", "Personalized Taste Profile Radar Analytics", "#7C3AED", "#F5F3FF", "#DDD6FE"),
    ]
    
    for y_pos, is_fwd, num_str, label_text, arrow_color, bg_pill, border_pill in flows:
        # Straight Horizontal Arrow
        x_start = ent_x + ent_w # 4.6
        # Circle edge x at this y:
        dx = math.sqrt(max(0, proc_r**2 - (y_pos - proc_cy)**2))
        x_end = proc_cx - dx - 0.1
        
        if is_fwd:
            ax.annotate("", xy=(x_end, y_pos), xytext=(x_start, y_pos),
                        arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.2, mutation_scale=16), zorder=2)
        else:
            ax.annotate("", xy=(x_start, y_pos), xytext=(x_end, y_pos),
                        arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.2, mutation_scale=16), zorder=2)
            
        # Centered Pill Box
        pill_cx = (x_start + x_end) / 2.0
        pill_w = 5.6
        pill_h = 0.55
        
        pill = FancyBboxPatch((pill_cx - pill_w/2.0, y_pos - pill_h/2.0), pill_w, pill_h,
                              boxstyle="round,pad=0.04,rounding_size=0.15",
                              facecolor=bg_pill, edgecolor=border_pill, lw=1.4, zorder=3)
        ax.add_patch(pill)
        
        ax.text(pill_cx - pill_w/2.0 + 0.35, y_pos, num_str, ha='center', va='center', 
                fontsize=11.5, fontweight='bold', color=arrow_color, fontfamily=font, zorder=4)
        ax.text(pill_cx - pill_w/2.0 + 0.65, y_pos, label_text, ha='left', va='center', 
                fontsize=10.5, fontweight='bold', color='#1E293B', fontfamily=font, zorder=4)

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_0.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_0_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Standard DFD Level 0 to", p1, "and", p2)

# -------------------------------------------------------------
# 2. DFD LEVEL 1 (FUNCTIONAL DECOMPOSITION) - GANE-SARSON & STRAIGHT
# -------------------------------------------------------------
def generate_standard_dfd_level1():
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 20)
    ax.set_ylim(0.8, 14.2)
    ax.axis('off')
    font = 'Segoe UI'

    # Title
    title_box = FancyBboxPatch((4.0, 12.8), 12.0, 1.0, boxstyle="round,pad=0.08,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    ax.text(10.0, 13.45, "Data Flow Diagram (DFD) - Level 1", ha='center', va='center', fontsize=21, fontweight='bold', color='#0F172A', fontfamily=font)
    ax.text(10.0, 13.05, "First Level Functional Decomposition | Movie Recommendation System", ha='center', va='center', fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)

    # Gane-Sarson Store Helper
    def draw_store(x, y, w, h, ds_id, ds_name):
        ax.add_patch(patches.Rectangle((x, y - h/2.0), w, h, facecolor='#FFFBEB', edgecolor='none', alpha=0.95))
        ax.plot([x, x + w], [y + h/2.0, y + h/2.0], color='#B45309', lw=2.4)
        ax.plot([x, x + w], [y - h/2.0, y - h/2.0], color='#B45309', lw=2.4)
        ax.plot([x, x], [y - h/2.0, y + h/2.0], color='#B45309', lw=2.4)
        id_w = 0.8
        ax.plot([x + id_w, x + id_w], [y - h/2.0, y + h/2.0], color='#D97706', lw=1.8)
        ax.text(x + id_w/2.0, y, ds_id, ha='center', va='center', fontsize=12, fontweight='bold', color='#B45309', fontfamily=font)
        ax.text(x + id_w + 0.2, y, ds_name, ha='left', va='center', fontsize=10.5, fontweight='bold', color='#78350F', fontfamily=font)

    # Process Circle Helper
    def draw_proc(cx, cy, r, num, line1, line2='', fill='#F0FDF4', border='#16A34A', num_c='#15803D'):
        ax.add_patch(patches.Circle((cx + 0.05, cy - 0.05), r, facecolor='#94A3B8', edgecolor='none', alpha=0.18))
        ax.add_patch(patches.Circle((cx, cy), r, facecolor=fill, edgecolor=border, lw=2.4))
        div_y = cy + r * 0.42
        chord_w = 2.0 * math.sqrt(r**2 - (div_y - cy)**2)
        ax.plot([cx - chord_w/2.0 + 0.1, cx + chord_w/2.0 - 0.1], [div_y, div_y], color=border, lw=1.5, alpha=0.6)
        ax.text(cx, cy + r * 0.68, num, ha='center', va='center', fontsize=13, fontweight='bold', color=num_c, fontfamily=font)
        if line2:
            ax.text(cx, cy - 0.05, line1, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#064E3B', fontfamily=font)
            ax.text(cx, cy - 0.55, line2, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#064E3B', fontfamily=font)
        else:
            ax.text(cx, cy - 0.25, line1, ha='center', va='center', fontsize=11, fontweight='bold', color='#064E3B', fontfamily=font)

    # Entity: USER (Left)
    ax.add_patch(patches.Rectangle((0.8, 3.8), 2.8, 6.2, facecolor='#F8FAFC', edgecolor='#1D4ED8', lw=2.6))
    ax.plot([1.0, 1.0], [4.0, 9.8], color='#93C5FD', lw=2.0, linestyle='--')
    ax.text(2.2, 9.4, "External Entity", ha='center', va='center', fontsize=10, fontweight='bold', color='#3B82F6', fontfamily=font)
    ax.text(2.2, 7.3, "USER", ha='center', va='center', fontsize=20, fontweight='bold', color='#1E3A8A', fontfamily=font)
    ax.text(2.2, 6.6, "(Movie Buff)", ha='center', va='center', fontsize=11, fontweight='bold', color='#475569', fontfamily=font)
    ax.text(2.2, 4.8, "[Web Client]", ha='center', va='center', fontsize=9.5, color='#64748B', fontfamily=font)

    # 5 Functional Processes
    draw_proc(6.5, 10.5, 1.3, "1.0", "User Auth &", "Profile Mgmt")
    draw_proc(6.5, 6.8, 1.3, "2.0", "Movie Search", "& Filtering")
    draw_proc(12.0, 6.8, 1.5, "3.0", "Hybrid Rec Engine", "(TF-IDF, SVD, ANN)", fill='#FEFCE8', border='#CA8A04', num_c='#A16207')
    draw_proc(6.5, 2.8, 1.3, "4.0", "Rating & Watchlist", "Interaction Mgmt")
    draw_proc(17.5, 2.8, 1.3, "5.0", "Taste Analytics &", "Radar Profiling")

    # 4 Data Stores
    draw_store(10.5, 10.5, 4.2, 0.9, "D1", "User Accounts Store")
    draw_store(15.5, 6.8, 3.8, 0.9, "D2", "Movie Features Store")
    draw_store(10.5, 2.8, 3.8, 0.9, "D3", "User Ratings Store")
    draw_store(15.0, 4.8, 4.2, 0.9, "D4", "Watchlist Database")

    # Straight / Orthogonal Flows Helper
    def draw_pill_label(cx, cy, text, color='#1E293B', bg='#FFFFFF', border='#CBD5E1'):
        w = len(text) * 0.12 + 0.4
        pill = FancyBboxPatch((cx - w/2.0, cy - 0.22), w, 0.44, boxstyle="round,pad=0.03,rounding_size=0.1", facecolor=bg, edgecolor=border, lw=1.0, zorder=4)
        ax.add_patch(pill)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color, fontfamily=font, zorder=5)

    # User -> 1.0 (Orthogonal: (3.6, 8.5) -> (4.5, 8.5) -> (4.5, 10.5) -> (5.2, 10.5))
    ax.plot([3.6, 4.5], [8.5, 8.5], color='#1E40AF', lw=1.8)
    ax.plot([4.5, 4.5], [8.5, 10.5], color='#1E40AF', lw=1.8)
    ax.annotate("", xy=(5.2, 10.5), xytext=(4.5, 10.5), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.8, mutation_scale=12))
    draw_pill_label(4.2, 9.5, "Credentials", '#1E40AF')

    # 1.0 <-> D1 (Straight Horizontal: (7.8, 10.5) -> (10.5, 10.5))
    ax.annotate("", xy=(10.5, 10.5), xytext=(7.8, 10.5), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.8, mutation_scale=12))
    draw_pill_label(9.1, 10.8, "Read/Write User Profile")

    # User -> 2.0 (Straight Horizontal: (3.6, 7.1) -> (5.2, 7.1))
    ax.annotate("", xy=(5.2, 7.1), xytext=(3.6, 7.1), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.8, mutation_scale=12))
    draw_pill_label(4.4, 7.4, "Search Query", '#1E40AF')

    # 2.0 -> User (Straight Horizontal: (5.2, 6.5) -> (3.6, 6.5))
    ax.annotate("", xy=(3.6, 6.5), xytext=(5.2, 6.5), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.8, mutation_scale=12))
    draw_pill_label(4.4, 6.2, "Movie Results", '#1E40AF')

    # 2.0 -> 3.0 (Straight Horizontal: (7.8, 6.8) -> (10.5, 6.8))
    ax.annotate("", xy=(10.5, 6.8), xytext=(7.8, 6.8), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.8, mutation_scale=12))
    draw_pill_label(9.1, 7.1, "Selected Movie", '#B45309')

    # D2 -> 3.0 (Straight Horizontal: (15.5, 6.8) -> (13.5, 6.8))
    ax.annotate("", xy=(13.5, 6.8), xytext=(15.5, 6.8), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.8, mutation_scale=12))
    draw_pill_label(14.5, 7.1, "TF-IDF Vectors", '#B45309')

    # D3 -> 3.0 (Straight Vertical: (12.0, 3.25) -> (12.0, 5.3))
    ax.annotate("", xy=(12.0, 5.3), xytext=(12.0, 3.25), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.8, mutation_scale=12))
    draw_pill_label(12.0, 4.3, "User Ratings Matrix", '#B45309')

    # 3.0 -> User (Orthogonal: (12.0, 8.3) -> (12.0, 9.2) -> (2.2, 9.2) -> (2.2, 10.0))
    ax.plot([12.0, 12.0], [8.3, 9.2], color='#15803D', lw=2.0)
    ax.plot([12.0, 2.2], [9.2, 9.2], color='#15803D', lw=2.0)
    ax.annotate("", xy=(2.2, 10.0), xytext=(2.2, 9.2), arrowprops=dict(arrowstyle="->", color='#15803D', lw=2.0, mutation_scale=12))
    draw_pill_label(7.1, 9.5, "Top-N Recommendations & Predicted Likelihood", '#15803D', '#F0FDF4', '#BBF7D0')

    # User -> 4.0 (Orthogonal: (3.6, 5.2) -> (4.5, 5.2) -> (4.5, 2.8) -> (5.2, 2.8))
    ax.plot([3.6, 4.5], [5.2, 5.2], color='#1E40AF', lw=1.8)
    ax.plot([4.5, 4.5], [5.2, 2.8], color='#1E40AF', lw=1.8)
    ax.annotate("", xy=(5.2, 2.8), xytext=(4.5, 2.8), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.8, mutation_scale=12))
    draw_pill_label(4.5, 4.0, "1-5 Star Rating & Watchlist", '#1E40AF')

    # 4.0 -> D3 (Straight Horizontal: (7.8, 2.8) -> (10.5, 2.8))
    ax.annotate("", xy=(10.5, 2.8), xytext=(7.8, 2.8), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.8, mutation_scale=12))
    draw_pill_label(9.1, 3.1, "Save Ratings", '#DC2626')

    # 4.0 -> D4 (Orthogonal: (7.8, 2.5) -> (9.5, 2.5) -> (9.5, 4.8) -> (15.0, 4.8))
    ax.plot([7.8, 9.5], [2.5, 2.5], color='#DC2626', lw=1.8)
    ax.plot([9.5, 9.5], [2.5, 4.8], color='#DC2626', lw=1.8)
    ax.annotate("", xy=(15.0, 4.8), xytext=(9.5, 4.8), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.8, mutation_scale=12))
    draw_pill_label(11.8, 5.1, "Save Watchlist Bookmarks", '#DC2626')

    # D3 -> 5.0 (Straight Horizontal: (14.3, 2.8) -> (16.2, 2.8))
    ax.annotate("", xy=(16.2, 2.8), xytext=(14.3, 2.8), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.8, mutation_scale=12))
    draw_pill_label(15.2, 3.1, "User Interactions")

    # 5.0 -> User (Orthogonal: (17.5, 1.5) -> (17.5, 1.1) -> (2.2, 1.1) -> (2.2, 3.8))
    ax.plot([17.5, 17.5], [1.5, 1.1], color='#7C3AED', lw=2.0)
    ax.plot([17.5, 2.2], [1.1, 1.1], color='#7C3AED', lw=2.0)
    ax.annotate("", xy=(2.2, 3.8), xytext=(2.2, 1.1), arrowprops=dict(arrowstyle="->", color='#7C3AED', lw=2.0, mutation_scale=12))
    draw_pill_label(9.8, 1.4, "Interactive Taste Radar Profile Analytics & Genre Breakdown", '#7C3AED', '#F5F3FF', '#DDD6FE')

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_1.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_1_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Standard DFD Level 1 to", p1, "and", p2)

# -------------------------------------------------------------
# 3. DFD LEVEL 2 (RECOMMENDATION PIPELINE) - CLEAN LINEAR STAGES
# -------------------------------------------------------------
def generate_standard_dfd_level2():
    fig, ax = plt.subplots(figsize=(19, 11), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 19)
    ax.set_ylim(0.8, 11.2)
    ax.axis('off')
    font = 'Segoe UI'

    title_box = FancyBboxPatch((3.5, 9.9), 12.0, 1.0, boxstyle="round,pad=0.08,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    ax.text(9.5, 10.5, "Data Flow Diagram (DFD) - Level 2", ha='center', va='center', fontsize=21, fontweight='bold', color='#0F172A', fontfamily=font)
    ax.text(9.5, 10.1, "Process 3.0: Hybrid Recommendation Engine & Deep ML Pipeline", ha='center', va='center', fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)

    def draw_store(x, y, w, h, ds_id, ds_name):
        ax.add_patch(patches.Rectangle((x, y - h/2.0), w, h, facecolor='#FFFBEB', edgecolor='none', alpha=0.95))
        ax.plot([x, x + w], [y + h/2.0, y + h/2.0], color='#B45309', lw=2.4)
        ax.plot([x, x + w], [y - h/2.0, y - h/2.0], color='#B45309', lw=2.4)
        ax.plot([x, x], [y - h/2.0, y + h/2.0], color='#B45309', lw=2.4)
        id_w = 0.8
        ax.plot([x + id_w, x + id_w], [y - h/2.0, y + h/2.0], color='#D97706', lw=1.8)
        ax.text(x + id_w/2.0, y, ds_id, ha='center', va='center', fontsize=12, fontweight='bold', color='#B45309', fontfamily=font)
        ax.text(x + id_w + 0.2, y, ds_name, ha='left', va='center', fontsize=10.5, fontweight='bold', color='#78350F', fontfamily=font)

    def draw_proc(cx, cy, r, num, line1, line2='', fill='#F0FDF4', border='#16A34A', num_c='#15803D'):
        ax.add_patch(patches.Circle((cx + 0.05, cy - 0.05), r, facecolor='#94A3B8', edgecolor='none', alpha=0.18))
        ax.add_patch(patches.Circle((cx, cy), r, facecolor=fill, edgecolor=border, lw=2.4))
        div_y = cy + r * 0.42
        chord_w = 2.0 * math.sqrt(r**2 - (div_y - cy)**2)
        ax.plot([cx - chord_w/2.0 + 0.1, cx + chord_w/2.0 - 0.1], [div_y, div_y], color=border, lw=1.5, alpha=0.6)
        ax.text(cx, cy + r * 0.68, num, ha='center', va='center', fontsize=13, fontweight='bold', color=num_c, fontfamily=font)
        if line2:
            ax.text(cx, cy - 0.05, line1, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#064E3B', fontfamily=font)
            ax.text(cx, cy - 0.55, line2, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#064E3B', fontfamily=font)
        else:
            ax.text(cx, cy - 0.25, line1, ha='center', va='center', fontsize=11, fontweight='bold', color='#064E3B', fontfamily=font)

    def draw_pill_label(cx, cy, text, color='#1E293B', bg='#FFFFFF', border='#CBD5E1'):
        w = len(text) * 0.12 + 0.4
        pill = FancyBboxPatch((cx - w/2.0, cy - 0.22), w, 0.44, boxstyle="round,pad=0.03,rounding_size=0.1", facecolor=bg, edgecolor=border, lw=1.0, zorder=4)
        ax.add_patch(pill)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color, fontfamily=font, zorder=5)

    # Input Data Stores (Left)
    draw_store(1.0, 7.5, 3.8, 0.9, "D2", "Movie Feature Vectors")
    draw_store(1.0, 3.5, 3.8, 0.9, "D3", "User Ratings Matrix")
    draw_store(6.5, 9.0, 3.8, 0.9, "D5", "Neural Network Weights")

    # Sub-Processes
    draw_proc(7.0, 7.0, 1.3, "3.1", "TF-IDF Vectorizer", "& Cosine Matching")
    draw_proc(7.0, 3.5, 1.3, "3.2", "Truncated SVD", "Matrix Factorization")
    draw_proc(12.0, 5.25, 1.4, "3.3", "3-Layer Keras ANN", "Likelihood Classifier")
    draw_proc(16.5, 5.25, 1.5, "3.4", "Hybrid Ranker &", "Diversity Filter", fill='#FEFCE8', border='#CA8A04', num_c='#A16207')

    # Output Box (Bottom Right)
    ax.add_patch(patches.Rectangle((14.8, 1.2), 3.4, 1.8, facecolor='#EFF6FF', edgecolor='#1D4ED8', lw=2.2))
    ax.text(16.5, 2.3, "USER INTERFACE", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E40AF', fontfamily=font)
    ax.text(16.5, 1.7, "Top-10 Recommended Films", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A', fontfamily=font)

    # D2 -> 3.1 (Straight Horizontal: (4.8, 7.5) -> (5.7, 7.5) -> (5.7, 7.0))
    ax.plot([4.8, 5.7], [7.5, 7.5], color='#334155', lw=1.8)
    ax.annotate("", xy=(5.7, 7.0), xytext=(5.7, 7.5), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.8, mutation_scale=12))
    draw_pill_label(5.2, 7.8, "Feature Vectors")

    # D3 -> 3.2 (Straight Horizontal: (4.8, 3.5) -> (5.7, 3.5))
    ax.annotate("", xy=(5.7, 3.5), xytext=(4.8, 3.5), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.8, mutation_scale=12))
    draw_pill_label(5.2, 3.8, "Ratings Matrix")

    # D5 -> 3.3 (Orthogonal: (10.3, 9.0) -> (12.0, 9.0) -> (12.0, 6.65))
    ax.plot([10.3, 12.0], [9.0, 9.0], color='#334155', lw=1.8)
    ax.annotate("", xy=(12.0, 6.65), xytext=(12.0, 9.0), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.8, mutation_scale=12))
    draw_pill_label(11.1, 9.3, "Trained Weights")

    # 3.1 -> 3.3 (Orthogonal: (8.3, 7.0) -> (9.5, 7.0) -> (9.5, 5.7) -> (10.6, 5.7))
    ax.plot([8.3, 9.5], [7.0, 7.0], color='#2563EB', lw=1.8)
    ax.plot([9.5, 9.5], [7.0, 5.7], color='#2563EB', lw=1.8)
    ax.annotate("", xy=(10.6, 5.7), xytext=(9.5, 5.7), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8, mutation_scale=12))
    draw_pill_label(8.9, 7.3, "Content Vectors", '#2563EB')

    # 3.2 -> 3.3 (Orthogonal: (8.3, 3.5) -> (9.5, 3.5) -> (9.5, 4.8) -> (10.6, 4.8))
    ax.plot([8.3, 9.5], [3.5, 3.5], color='#15803D', lw=1.8)
    ax.plot([9.5, 9.5], [3.5, 4.8], color='#15803D', lw=1.8)
    ax.annotate("", xy=(10.6, 4.8), xytext=(9.5, 4.8), arrowprops=dict(arrowstyle="->", color='#15803D', lw=1.8, mutation_scale=12))
    draw_pill_label(8.9, 3.2, "Latent Factors", '#15803D')

    # 3.1 -> 3.4 (Orthogonal: (8.3, 7.8) -> (15.5, 7.8) -> (15.5, 6.5))
    ax.plot([8.3, 15.5], [7.8, 7.8], color='#2563EB', lw=1.8)
    ax.annotate("", xy=(15.5, 6.5), xytext=(15.5, 7.8), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8, mutation_scale=12))
    draw_pill_label(11.9, 8.1, "Content Cosine Scores [0.0 - 1.0]", '#2563EB', '#EFF6FF', '#BFDBFE')

    # 3.2 -> 3.4 (Orthogonal: (8.3, 2.7) -> (15.5, 2.7) -> (15.5, 4.0))
    ax.plot([8.3, 15.5], [2.7, 2.7], color='#15803D', lw=1.8)
    ax.annotate("", xy=(15.5, 4.0), xytext=(15.5, 2.7), arrowprops=dict(arrowstyle="->", color='#15803D', lw=1.8, mutation_scale=12))
    draw_pill_label(11.9, 2.4, "Predicted SVD Ratings (1.0 - 5.0)", '#15803D', '#F0FDF4', '#BBF7D0')

    # 3.3 -> 3.4 (Straight Horizontal: (13.4, 5.25) -> (15.0, 5.25))
    ax.annotate("", xy=(15.0, 5.25), xytext=(13.4, 5.25), arrowprops=dict(arrowstyle="->", color='#7C3AED', lw=1.8, mutation_scale=12))
    draw_pill_label(14.2, 5.55, "P(Like)", '#7C3AED')

    # 3.4 -> Output Box (Straight Vertical: (16.5, 3.75) -> (16.5, 3.0))
    ax.annotate("", xy=(16.5, 3.0), xytext=(16.5, 3.75), arrowprops=dict(arrowstyle="->", color='#B45309', lw=2.2, mutation_scale=14))
    draw_pill_label(16.5, 3.4, "Top-N List", '#B45309')

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_2.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_2_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Standard DFD Level 2 to", p1, "and", p2)

# -------------------------------------------------------------
# 4. ER DIAGRAM (ACADEMIC RELATIONAL TABLE CARDS) - SOLID/DASHED UNDERLINES
# -------------------------------------------------------------
def generate_standard_er_diagram():
    fig, ax = plt.subplots(figsize=(22, 14), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 22)
    ax.set_ylim(0.5, 14.5)
    ax.axis('off')
    font = 'Segoe UI'

    # Title
    title_box = FancyBboxPatch((4.0, 13.0), 14.0, 1.0, boxstyle="round,pad=0.08,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(title_box)
    ax.text(11.0, 13.65, "Entity-Relationship (ER) Diagram", ha='center', va='center', fontsize=22, fontweight='bold', color='#0F172A', fontfamily=font)
    ax.text(11.0, 13.25, "Academic Relational Model | Solid Underline: Primary Key | Dashed Underline: Foreign Key | No PK/FK Text", ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1E40AF', fontfamily=font)

    # Table Card Helper
    def draw_table_card(x, y, w, h, title, category, cols, header_bg='#1E3A8A', border_c='#1E40AF'):
        # Drop shadow
        ax.add_patch(FancyBboxPatch((x - w/2.0 + 0.08, y - h/2.0 - 0.08), w, h, boxstyle="round,pad=0.04,rounding_size=0.15", facecolor='#94A3B8', edgecolor='none', alpha=0.2, zorder=2))
        # Body
        ax.add_patch(FancyBboxPatch((x - w/2.0, y - h/2.0), w, h, boxstyle="round,pad=0.04,rounding_size=0.15", facecolor='#FFFFFF', edgecolor=border_c, lw=2.4, zorder=3))
        # Header
        header_h = 1.0
        ax.add_patch(FancyBboxPatch((x - w/2.0, y + h/2.0 - header_h), w, header_h, boxstyle="round,pad=0.02,rounding_size=0.15", facecolor=header_bg, edgecolor=border_c, lw=2.0, zorder=4))
        ax.add_patch(patches.Rectangle((x - w/2.0 + 0.03, y + h/2.0 - header_h), w - 0.06, 0.4, facecolor=header_bg, edgecolor='none', zorder=4))
        
        ax.text(x, y + h/2.0 - 0.35, title, ha='center', va='center', fontsize=14, fontweight='bold', color='#FFFFFF', fontfamily=font, zorder=5)
        ax.text(x, y + h/2.0 - 0.72, f"«{category}»", ha='center', va='center', fontsize=10, fontweight='bold', color='#93C5FD', fontfamily=font, zorder=5)
        ax.plot([x - w/2.0, x + w/2.0], [y + h/2.0 - header_h, y + h/2.0 - header_h], color=border_c, lw=2.0, zorder=5)
        
        # Rows
        content_top = y + h/2.0 - header_h
        row_h = (h - header_h) / max(len(cols), 1)
        
        for idx, (col_name, col_type, is_pk, is_fk) in enumerate(cols):
            row_y = content_top - (idx + 0.5) * row_h
            bg_c = '#F8FAFC' if idx % 2 == 0 else '#FFFFFF'
            ax.add_patch(patches.Rectangle((x - w/2.0 + 0.02, row_y - row_h/2.0), w - 0.04, row_h, facecolor=bg_c, edgecolor='none', zorder=4))
            
            # Text position
            ax.text(x - w/2.0 + 0.35, row_y, col_name, ha='left', va='center', fontsize=10.5, fontweight='bold' if (is_pk or is_fk) else 'normal', color='#0F172A', fontfamily=font, zorder=5)
            ax.text(x + w/2.0 - 0.35, row_y, col_type, ha='right', va='center', fontsize=9.5, fontstyle='italic', color='#64748B', fontfamily=font, zorder=5)
            
            # Underline PK or FK
            tw = len(col_name) * 0.105
            if is_pk:
                ax.plot([x - w/2.0 + 0.35, x - w/2.0 + 0.35 + tw], [row_y - 0.14, row_y - 0.14], color='#0F172A', lw=1.8, zorder=6)
            elif is_fk:
                ax.plot([x - w/2.0 + 0.35, x - w/2.0 + 0.35 + tw], [row_y - 0.14, row_y - 0.14], color='#0F172A', lw=1.8, linestyle='--', zorder=6)

    # 5 Entity Tables
    # 1. users (Top Left)
    u_cols = [
        ("user_id", "INTEGER (PK)", True, False),
        ("username", "VARCHAR(50)", False, False),
        ("email", "VARCHAR(100)", False, False),
        ("password_hash", "VARCHAR(255)", False, False),
        ("created_at", "DATETIME", False, False)
    ]
    draw_table_card(4.0, 9.8, 4.4, 3.8, "users", "User Account Entity", u_cols, '#1E3A8A', '#1D4ED8')

    # 2. movies (Top Right)
    m_cols = [
        ("movie_id", "INTEGER (PK)", True, False),
        ("title", "VARCHAR(255)", False, False),
        ("release_year", "INTEGER", False, False),
        ("vote_average", "FLOAT", False, False),
        ("vote_count", "INTEGER", False, False),
        ("overview", "TEXT", False, False),
        ("poster_url", "VARCHAR(500)", False, False)
    ]
    draw_table_card(18.0, 9.8, 4.4, 4.8, "movies", "Movie Catalog Entity", m_cols, '#065F46', '#059669')

    # 3. ratings (Center Top)
    r_cols = [
        ("rating_id", "INTEGER (PK)", True, False),
        ("user_id", "INTEGER (FK)", False, True),
        ("movie_id", "INTEGER (FK)", False, True),
        ("rating_val", "FLOAT (0.5-5.0)", False, False),
        ("timestamp", "DATETIME", False, False)
    ]
    draw_table_card(11.0, 9.8, 4.4, 3.8, "ratings", "Interaction Assoc Entity", r_cols, '#B45309', '#D97706')

    # 4. watchlist (Bottom Left)
    w_cols = [
        ("watchlist_id", "INTEGER (PK)", True, False),
        ("user_id", "INTEGER (FK)", False, True),
        ("movie_id", "INTEGER (FK)", False, True),
        ("status", "VARCHAR(20)", False, False),
        ("added_date", "DATETIME", False, False)
    ]
    draw_table_card(4.0, 3.8, 4.4, 3.8, "watchlist", "User Bookmark Entity", w_cols, '#6B21A8', '#9333EA')

    # 5. movie_genres (Bottom Right)
    g_cols = [
        ("genre_id", "INTEGER (PK)", True, False),
        ("movie_id", "INTEGER (FK)", False, True),
        ("genre_name", "VARCHAR(50)", False, False)
    ]
    draw_table_card(18.0, 3.8, 4.4, 3.0, "movie_genres", "Genre Categorization", g_cols, '#991B1B', '#DC2626')

    # Straight Relationship Connectors & Cardinalities
    # users -> ratings (Straight Horizontal: (6.2, 9.8) -> (8.8, 9.8))
    ax.plot([6.2, 8.8], [9.8, 9.8], color='#1E40AF', lw=2.2, zorder=2)
    ax.text(6.5, 10.1, "1", fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)
    ax.text(8.5, 10.1, "0..*", fontsize=13, fontweight='bold', color='#1E40AF', fontfamily=font)
    ax.text(7.5, 9.4, "submits", fontsize=10, fontweight='bold', ha='center', color='#475569', fontfamily=font)

    # movies -> ratings (Straight Horizontal: (15.8, 9.8) -> (13.2, 9.8))
    ax.plot([15.8, 13.2], [9.8, 9.8], color='#059669', lw=2.2, zorder=2)
    ax.text(15.5, 10.1, "1", fontsize=13, fontweight='bold', color='#059669', fontfamily=font)
    ax.text(13.5, 10.1, "0..*", fontsize=13, fontweight='bold', color='#059669', fontfamily=font)
    ax.text(14.5, 9.4, "receives", fontsize=10, fontweight='bold', ha='center', color='#475569', fontfamily=font)

    # users -> watchlist (Straight Vertical: (4.0, 7.9) -> (4.0, 5.7))
    ax.plot([4.0, 4.0], [7.9, 5.7], color='#6B21A8', lw=2.2, zorder=2)
    ax.text(4.2, 7.5, "1", fontsize=13, fontweight='bold', color='#6B21A8', fontfamily=font)
    ax.text(4.2, 6.0, "0..*", fontsize=13, fontweight='bold', color='#6B21A8', fontfamily=font)
    ax.text(3.3, 6.8, "maintains", fontsize=10, fontweight='bold', color='#475569', fontfamily=font)

    # movies -> movie_genres (Straight Vertical: (18.0, 7.4) -> (18.0, 5.3))
    ax.plot([18.0, 18.0], [7.4, 5.3], color='#991B1B', lw=2.2, zorder=2)
    ax.text(18.2, 7.1, "1", fontsize=13, fontweight='bold', color='#991B1B', fontfamily=font)
    ax.text(18.2, 5.6, "1..*", fontsize=13, fontweight='bold', color='#991B1B', fontfamily=font)
    ax.text(17.1, 6.4, "belongs_to", fontsize=10, fontweight='bold', color='#475569', fontfamily=font)

    # watchlist -> movies (Orthogonal: (6.2, 3.8) -> (11.0, 3.8) -> (11.0, 7.4) -> (15.8, 7.4))
    ax.plot([6.2, 11.0], [3.8, 3.8], color='#334155', lw=1.8, zorder=2)
    ax.plot([11.0, 11.0], [3.8, 7.4], color='#334155', lw=1.8, zorder=2)
    ax.plot([11.0, 15.8], [7.4, 7.4], color='#334155', lw=1.8, zorder=2)
    ax.text(6.5, 4.1, "0..*", fontsize=12, fontweight='bold', color='#334155', fontfamily=font)
    ax.text(15.5, 7.7, "1", fontsize=12, fontweight='bold', color='#334155', fontfamily=font)
    ax.text(11.3, 5.5, "bookmarks", fontsize=10, fontweight='bold', color='#475569', fontfamily=font)

    # Academic Notation Legend Box (Center Bottom)
    leg = FancyBboxPatch((8.2, 1.0), 5.6, 1.4, boxstyle="round,pad=0.04,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#94A3B8', lw=1.2, zorder=3)
    ax.add_patch(leg)
    ax.text(11.0, 2.1, "Academic Relational Notation:", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1E293B', fontfamily=font)
    
    ax.plot([8.8, 9.8], [1.6, 1.6], color='#0F172A', lw=2.2)
    ax.text(10.1, 1.6, "Primary Key (Solid Underline)", ha='left', va='center', fontsize=9.5, color='#334155', fontfamily=font)
    
    ax.plot([8.8, 9.8], [1.25, 1.25], color='#0F172A', lw=2.2, linestyle='--')
    ax.text(10.1, 1.25, "Foreign Key (Dashed Underline)", ha='left', va='center', fontsize=9.5, color='#334155', fontfamily=font)

    plt.tight_layout()
    p1 = 'reports/figures/er_diagram_academic.png'
    p2 = os.path.join(DESKTOP_DIR, 'ER_Diagram_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Standard ER Diagram to", p1, "and", p2)

# -------------------------------------------------------------
# 5. USE CASE DIAGRAM (STANDARD UML 2.0)
# -------------------------------------------------------------
def generate_standard_use_case_diagram():
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
    ax.text(9.5, 11.45, "Movie Recommendation & Discovery System | Standard UML 2.0 Specification", ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1E40AF', fontfamily=font)

    # System Boundary Box
    ax.add_patch(patches.Rectangle((4.5, 1.0), 10.0, 9.8, facecolor='#F8FAFC', edgecolor='#0284C7', lw=2.8, zorder=1))
    ax.text(9.5, 10.4, "System: Movie Recommendation System", ha='center', va='center', fontsize=13, fontweight='bold', color='#0369A1', fontfamily=font)

    # Stick Figures Helper
    def draw_actor(x, y, label):
        ax.add_patch(patches.Circle((x, y + 0.9), 0.35, facecolor='#E2E8F0', edgecolor='#0F172A', lw=2.2, zorder=4))
        ax.plot([x, x], [y + 0.55, y - 0.4], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x - 0.6, x + 0.6], [y + 0.2, y + 0.2], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x, x - 0.5], [y - 0.4, y - 1.1], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x, x + 0.5], [y - 0.4, y - 1.1], color='#0F172A', lw=2.2, zorder=4)
        ax.text(x, y - 1.5, label, ha='center', va='top', fontsize=11, fontweight='bold', color='#0F172A', fontfamily=font)

    draw_actor(2.0, 6.0, "USER\n(Movie Buff)")
    draw_actor(17.0, 6.0, "ADMINISTRATOR\n/ ML ENGINEER")

    # Use Case Oval Helper
    def draw_uc(x, y, text, rx=1.45, ry=0.42, fill='#FFFFFF', border='#0284C7'):
        ax.add_patch(patches.Ellipse((x, y), rx*2, ry*2, facecolor=fill, edgecolor=border, lw=2.0, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A', fontfamily=font, zorder=4)

    # Column 1: User Direct Use Cases (x=7.2)
    draw_uc(7.2, 9.4, "Register / User Login")
    draw_uc(7.2, 8.1, "Search & Filter Movies")
    draw_uc(7.2, 6.8, "View Movie Details & Posters")
    draw_uc(7.2, 5.5, "Submit 1-5 Star Ratings")
    draw_uc(7.2, 4.2, "Get Content-Based Recs")
    draw_uc(7.2, 2.9, "Get Collaborative SVD Recs")
    draw_uc(7.2, 1.6, "Manage Watchlist & Bookmarks")

    # Column 2: Advanced Sub-processes & Admin Use Cases (x=11.8)
    draw_uc(11.8, 9.4, "Retrain / Update ML Models", fill='#FEF2F2', border='#DC2626')
    draw_uc(11.8, 8.1, "Evaluate Metrics (ROC/Loss)", fill='#FEF2F2', border='#DC2626')
    draw_uc(11.8, 6.5, "View Taste Radar Analytics")
    draw_uc(11.8, 4.2, "Extract TF-IDF Features", fill='#EFF6FF', border='#3B82F6')
    draw_uc(11.8, 2.9, "Predict Likelihood (ANN)", fill='#EFF6FF', border='#3B82F6')

    # Association Lines from User Actor (Straight ray connectors)
    user_hand = (2.6, 6.2)
    for uy in [9.4, 8.1, 6.8, 5.5, 4.2, 2.9, 1.6]:
        ax.plot([user_hand[0], 5.75], [user_hand[1], uy], color='#334155', lw=1.6, zorder=2)
    ax.plot([user_hand[0], 10.35], [user_hand[1], 6.5], color='#334155', lw=1.6, zorder=2)

    # Association Lines from Admin Actor
    admin_hand = (16.4, 6.2)
    ax.plot([admin_hand[0], 13.25], [admin_hand[1], 9.4], color='#DC2626', lw=1.6, zorder=2)
    ax.plot([admin_hand[0], 13.25], [admin_hand[1], 8.1], color='#DC2626', lw=1.6, zorder=2)

    # Include Relationship (Content Recs <<include>> Extract TF-IDF) - Horizontal
    ax.annotate("", xy=(10.35, 4.2), xytext=(8.65, 4.2),
                arrowprops=dict(arrowstyle="->", linestyle='--', color='#2563EB', lw=1.8, mutation_scale=12))
    ax.text(9.5, 4.5, "«include»", ha='center', va='center', fontsize=9, fontweight='bold', color='#2563EB', fontfamily=font)

    # Extend Relationship (Collaborative SVD <<extend>> Predict ANN) - Horizontal
    ax.annotate("", xy=(8.65, 2.9), xytext=(10.35, 2.9),
                arrowprops=dict(arrowstyle="->", linestyle='--', color='#7C3AED', lw=1.8, mutation_scale=12))
    ax.text(9.5, 3.2, "«extend»", ha='center', va='center', fontsize=9, fontweight='bold', color='#7C3AED', fontfamily=font)

    plt.tight_layout()
    p1 = 'reports/figures/use_case_diagram.png'
    p2 = os.path.join(DESKTOP_DIR, 'Use_Case_Diagram_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Standard Use Case Diagram to", p1, "and", p2)

if __name__ == '__main__':
    generate_standard_dfd_level0()
    generate_standard_dfd_level1()
    generate_standard_dfd_level2()
    generate_standard_er_diagram()
    generate_standard_use_case_diagram()
