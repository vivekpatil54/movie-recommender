import os
import math
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

os.makedirs('reports/figures', exist_ok=True)
DESKTOP_DIR = r"C:\Users\satis\OneDrive\Desktop"

plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'

# =============================================================
# 1. DFD LEVEL 0 (CONTEXT LEVEL DIAGRAM)
# =============================================================
def build_dfd_level0():
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
    
    ax.text(9.0, 10.32, "Movie Recommendation and Discovery System", 
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

    # Process Circle 0.0: [ MOVIE RECOMMENDATION SYSTEM ] (Right)
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
    
    ax.text(proc_cx, proc_cy + 0.55, "Movie", 
            ha='center', va='center', fontsize=17, fontweight='bold', 
            color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 0.05, "Recommendation", 
            ha='center', va='center', fontsize=17, fontweight='bold', 
            color='#064E3B', fontfamily=font)
    ax.text(proc_cx, proc_cy - 0.65, "System", 
            ha='center', va='center', fontsize=17, fontweight='bold', 
            color='#064E3B', fontfamily=font)

    x_student = ent_x + ent_w # 4.6
    
    # FLOW 1: SINGLE DIRECTED INPUT ARROW (USER -> SYSTEM)
    y_in = 6.4
    dy_in = y_in - proc_cy
    dx_in = math.sqrt(proc_r**2 - dy_in**2)
    x_target_in = proc_cx - dx_in
    
    ax.plot(x_student, y_in, marker='o', markersize=7, color='#1D4ED8')
    ax.annotate('', xy=(x_target_in, y_in), xytext=(x_student, y_in),
                arrowprops=dict(arrowstyle='->,head_width=0.75,head_length=0.9', 
                                color='#2563EB', lw=3.0))
    
    input_flows = [
        "Login & Registration Credentials",
        "Movie Search & Genre Filter Preferences",
        "1-to-5 Star User Ratings",
        "Watchlist Bookmarking Requests"
    ]
    
    label_center_x = (x_student + x_target_in) / 2.0
    
    for i, item in enumerate(input_flows):
        item_y = y_in + 0.28 + (3 - i) * 0.42
        ax.text(label_center_x, item_y, f"•  {item}", 
                ha='center', va='bottom', fontsize=11.5, fontweight='bold', 
                color='#1E3A8A', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.20', facecolor='#EFF6FF', edgecolor='#DBEAFE', lw=0.8))

    # FLOW 2: SINGLE DIRECTED OUTPUT ARROW (SYSTEM -> USER)
    y_out = 4.4
    dy_out = y_out - proc_cy
    dx_out = math.sqrt(proc_r**2 - dy_out**2)
    x_source_out = proc_cx - dx_out
    
    ax.plot(x_source_out, y_out, marker='o', markersize=6.5, color='#16A34A')
    ax.plot(x_student, y_out, marker='o', markersize=7, color='#059669')
    
    ax.annotate('', xy=(x_student, y_out), xytext=(x_source_out, y_out),
                arrowprops=dict(arrowstyle='->,head_width=0.75,head_length=0.9', 
                                color='#059669', lw=3.0))
    
    output_flows = [
        "Authentication Session Tokens",
        "Top-N Ranked Movie Recommendations",
        "Movie Posters, Overviews & Metadata",
        "Personalized Taste Profile Radar Analytics"
    ]
    
    label_center_out = (x_student + x_source_out) / 2.0
    
    for i, item in enumerate(output_flows):
        item_y = y_out - 0.28 - i * 0.42
        ax.text(label_center_out, item_y, f"•  {item}", 
                ha='center', va='top', fontsize=11.5, fontweight='bold', 
                color='#065F46', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.20', facecolor='#F0FDF4', edgecolor='#D1FAE5', lw=0.8))

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_0.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_0_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Flawlessly generated DFD Level 0 to", p1, "and", p2)

# =============================================================
# 2. DFD LEVEL 1 (DECOMPOSED LEVEL 1 ARCHITECTURE)
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

def build_dfd_level1():
    fig, ax = plt.subplots(figsize=(36.0, 26.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    ax.set_xlim(0, 36.0)
    ax.set_ylim(-0.2, 26.0)
    ax.axis('off')
    
    font = 'Segoe UI'
    
    # Title Block
    title_box = FancyBboxPatch((7.5, 23.9), 21.0, 1.45,
                               boxstyle="round,pad=0.08,rounding_size=0.16",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.6)
    ax.add_patch(title_box)
    
    ax.text(18.0, 24.75, "DFD Level 1 – Movie Recommendation and Discovery System", 
            ha='center', va='center', fontsize=26.0, fontweight='bold', 
            color='#0F172A', fontfamily=font)
    
    ax.text(18.0, 24.25, "Decomposed Level 1 Architecture: 5 Major Processes, 1 External Entity (E1) & 5 Implemented Database Tables", 
            ha='center', va='center', fontsize=14.0, fontweight='bold', 
            color='#1E40AF', fontfamily=font)

    # External Entity: E1 USER (Left)
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
    ax.text(ent_x + ent_w / 2.0, cy_ent - 1.80, "(Movie Explorer)", 
            ha='center', va='center', fontsize=18.0, fontweight='bold', 
            color='#475569', fontfamily=font)

    # 5 Processes (Middle Column: cx = 13.5, r = 1.95)
    p_cx = 13.5
    p_r = 1.95
    p_y = [21.0, 16.4, 11.8, 7.2, 2.6]
    
    draw_dfd1_process(ax, p_cx, p_y[0], p_r, "1.0", "User Auth &", "Profile Management")
    draw_dfd1_process(ax, p_cx, p_y[1], p_r, "2.0", "Movie Search &", "Catalog Filtering")
    draw_dfd1_process(ax, p_cx, p_y[2], p_r, "3.0", "Hybrid Rec Engine", "(TF-IDF, SVD, ANN)")
    draw_dfd1_process(ax, p_cx, p_y[3], p_r, "4.0", "Rating & Watchlist", "Interaction Mgmt")
    draw_dfd1_process(ax, p_cx, p_y[4], p_r, "5.0", "Taste Profile &", "Analytics Engine")

    # 5 Gane-Sarson Stores (Right Column: x = 23.5, w = 11.0, h = 1.8)
    s_x = 23.5
    s_w = 11.0
    s_h = 1.7
    
    draw_gane_sarson_store(ax, s_x, p_y[0], s_w, s_h, "D1", "users (Accounts & Profiles)")
    draw_gane_sarson_store(ax, s_x, p_y[1], s_w, s_h, "D2", "movies (Metadata & Vectors)")
    draw_gane_sarson_store(ax, s_x, p_y[2], s_w, s_h, "D3", "ratings (User Ratings Matrix)")
    draw_gane_sarson_store(ax, s_x, p_y[3], s_w, s_h, "D4", "watchlist (Saved Bookmarks)")
    draw_gane_sarson_store(ax, s_x, p_y[4], s_w, s_h, "D5", "movie_genres (Genre Map)")

    # Left Flows (E1 <-> Each Process)
    left_flows = [
        ("Login & Signup Request", "Authentication Token & Profile", p_y[0]),
        ("Keyword & Genre Search Query", "Filtered Movie Catalog Results", p_y[1]),
        ("Recommendation Request", "Top-N Movie Recs & Likelihood", p_y[2]),
        ("Submit Star Rating & Watchlist", "Rating Recorded & Watchlist Updated", p_y[3]),
        ("Taste Profile Analytics Request", "Interactive Genre Radar Breakdown", p_y[4])
    ]
    
    x_ent_edge = ent_x + ent_w # 4.5
    
    for req, res, cy in left_flows:
        # Top Arrow (User -> Process)
        ax.annotate('', xy=(p_cx - p_r, cy + 0.45), xytext=(x_ent_edge, cy + 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
        ax.text((x_ent_edge + p_cx - p_r) / 2.0, cy + 0.85, f"• {req}",
                ha='center', va='bottom', fontsize=12.5, fontweight='bold', color='#1E3A8A', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))
        
        # Bottom Arrow (Process -> User)
        ax.annotate('', xy=(x_ent_edge, cy - 0.45), xytext=(p_cx - p_r, cy - 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#059669', lw=2.6))
        ax.text((x_ent_edge + p_cx - p_r) / 2.0, cy - 0.85, f"• {res}",
                ha='center', va='top', fontsize=12.5, fontweight='bold', color='#065F46', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.0))

    # Right Flows (Each Process <-> Data Store)
    right_flows = [
        ("Write User / Query Hash", "User Record & Session Data", p_y[0]),
        ("Query Genre & Year Bounds", "Movie Metadata & Poster URLs", p_y[1]),
        ("Fetch Ratings & Features", "User-Item Matrix & Latent Weights", p_y[2]),
        ("Insert / Update Rating & Watchlist", "Confirmation & Record Status", p_y[3]),
        ("Aggregate Genre Frequencies", "User Interaction History", p_y[4])
    ]
    
    for req, res, cy in right_flows:
        # Top Arrow (Process -> Store)
        ax.annotate('', xy=(s_x, cy + 0.45), xytext=(p_cx + p_r, cy + 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
        ax.text((p_cx + p_r + s_x) / 2.0, cy + 0.85, f"• {req}",
                ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))
        
        # Bottom Arrow (Store -> Process)
        ax.annotate('', xy=(p_cx + p_r, cy - 0.45), xytext=(s_x, cy - 0.45),
                    arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#B45309', lw=2.6))
        ax.text((p_cx + p_r + s_x) / 2.0, cy - 0.85, f"• {res}",
                ha='center', va='top', fontsize=12.0, fontweight='bold', color='#78350F', fontfamily=font,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFBEB', edgecolor='#FCD34D', lw=1.0))

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_1.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_1_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', pad_inches=0.35, dpi=300)
    fig.savefig(p2, bbox_inches='tight', pad_inches=0.35, dpi=300)
    plt.close()
    print("Flawlessly generated DFD Level 1 to", p1, "and", p2)

# =============================================================
# 3. DFD LEVEL 2 (PROCESS 3.0: HYBRID RECOMMENDATION ENGINE)
# =============================================================
def build_dfd_level2():
    fig, ax = plt.subplots(figsize=(32.0, 20.0), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    ax.set_xlim(0, 32.0)
    ax.set_ylim(0.5, 20.0)
    ax.axis('off')
    
    font = 'Segoe UI'
    
    # Title Block
    title_box = FancyBboxPatch((6.0, 18.2), 20.0, 1.35,
                               boxstyle="round,pad=0.08,rounding_size=0.16",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.6)
    ax.add_patch(title_box)
    
    ax.text(16.0, 19.05, "DFD Level 2 – Process 3.0: Hybrid Recommendation Engine", 
            ha='center', va='center', fontsize=24.0, fontweight='bold', 
            color='#0F172A', fontfamily=font)
    
    ax.text(16.0, 18.55, "Detailed Functional Decomposition: Content TF-IDF, Collaborative SVD, Keras ANN & Hybrid Ranker", 
            ha='center', va='center', fontsize=13.5, fontweight='bold', 
            color='#1E40AF', fontfamily=font)

    # Left Input Gane-Sarson Stores
    draw_gane_sarson_store(ax, 1.0, 14.0, 7.0, 1.8, "D2", "movies (Metadata)")
    draw_gane_sarson_store(ax, 1.0, 6.0, 7.0, 1.8, "D3", "ratings (Ratings Matrix)")

    # 4 Sub-Processes
    p_r = 1.95
    draw_dfd1_process(ax, 12.5, 14.0, p_r, "3.1", "TF-IDF Feature", "Extraction & Cosine")
    draw_dfd1_process(ax, 12.5, 6.0, p_r, "3.2", "Truncated SVD", "Matrix Factorization")
    draw_dfd1_process(ax, 20.5, 10.0, p_r, "3.3", "3-Layer Keras ANN", "Preference Classifier")
    draw_dfd1_process(ax, 28.0, 10.0, p_r, "3.4", "Hybrid Ranker &", "Diversity Filter")

    # D2 -> 3.1
    ax.annotate('', xy=(12.5 - p_r, 14.0), xytext=(8.0, 14.0),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
    ax.text(9.3, 14.4, "Movie Metadata Soup", ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))

    # D3 -> 3.2
    ax.annotate('', xy=(12.5 - p_r, 6.0), xytext=(8.0, 6.0),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
    ax.text(9.3, 6.4, "Sparse User-Item Matrix", ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))

    # 3.1 -> 3.3
    ax.annotate('', xy=(20.5 - p_r, 10.6), xytext=(12.5 + p_r, 13.5),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
    ax.text(15.8, 12.8, "TF-IDF Embeddings", ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))

    # 3.2 -> 3.3
    ax.annotate('', xy=(20.5 - p_r, 9.4), xytext=(12.5 + p_r, 6.5),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#15803D', lw=2.6))
    ax.text(15.8, 7.2, "User Latent Vectors", ha='center', va='top', fontsize=11.5, fontweight='bold', color='#065F46', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.0))

    # 3.1 -> 3.4 (Cosine scores)
    ax.plot([12.5, 12.5], [14.0 + p_r, 16.5], color='#2563EB', lw=2.4)
    ax.plot([12.5, 28.0], [16.5, 16.5], color='#2563EB', lw=2.4)
    ax.annotate('', xy=(28.0, 10.0 + p_r), xytext=(28.0, 16.5),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#2563EB', lw=2.6))
    ax.text(20.25, 16.8, "Cosine Similarity Scores [0.0 - 1.0]", ha='center', va='bottom', fontsize=12.0, fontweight='bold', color='#1E3A8A', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0))

    # 3.2 -> 3.4 (SVD Predicted Ratings)
    ax.plot([12.5, 12.5], [6.0 - p_r, 3.5], color='#15803D', lw=2.4)
    ax.plot([12.5, 28.0], [3.5, 3.5], color='#15803D', lw=2.4)
    ax.annotate('', xy=(28.0, 10.0 - p_r), xytext=(28.0, 3.5),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#15803D', lw=2.6))
    ax.text(20.25, 3.1, "Predicted SVD Star Ratings (1.0 - 5.0)", ha='center', va='top', fontsize=12.0, fontweight='bold', color='#065F46', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.0))

    # 3.3 -> 3.4 (ANN Likelihood)
    ax.annotate('', xy=(28.0 - p_r, 10.0), xytext=(20.5 + p_r, 10.0),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.8', color='#7C3AED', lw=2.6))
    ax.text(24.25, 10.4, "P(Like) Probability", ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#7C3AED', fontfamily=font,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F3FF', edgecolor='#DDD6FE', lw=1.0))

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_2.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_2_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Flawlessly generated DFD Level 2 to", p1, "and", p2)

if __name__ == '__main__':
    build_dfd_level0()
    build_dfd_level1()
    build_dfd_level2()
