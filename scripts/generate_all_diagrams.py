import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('reports/figures', exist_ok=True)
DESKTOP_DIR = r"C:\Users\satis\OneDrive\Desktop"

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# 1. DFD LEVEL 0 (CONTEXT LEVEL) - 100% STRAIGHT ORTHOGONAL LINES
# -------------------------------------------------------------
def generate_dfd_level0():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 90)
    ax.axis('off')
    
    # Title
    ax.text(80, 84, "DATA FLOW DIAGRAM (DFD) - LEVEL 0", 
            fontsize=17, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(80, 80, "Context Level Diagram | Movie Recommendation & Discovery System", 
            fontsize=11.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # Styles
    c_ent_bg = '#EFF6FF'
    c_ent_border = '#1E40AF'
    c_proc_bg = '#F0FDF4'
    c_proc_border = '#15803D'
    c_ext_bg = '#FFFBEB'
    c_ext_border = '#B45309'

    # 1. External Entity: USER (Left)
    ax.add_patch(patches.Rectangle((10, 25), 28, 36, facecolor=c_ent_bg, edgecolor=c_ent_border, lw=2.2, zorder=3))
    ax.text(24, 54, "EXTERNAL ENTITY", fontsize=8.5, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(24, 45, "USER\n(Movie Buff)", fontsize=12, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(24, 34, "[Web Browser / Client]", fontsize=8.5, ha='center', color='#64748B')

    # 2. Central Process 0.0 (Center)
    circ_proc = patches.Circle((80, 43), 18, facecolor=c_proc_bg, edgecolor=c_proc_border, lw=2.5, zorder=3)
    ax.add_patch(circ_proc)
    ax.plot([62.5, 97.5], [51, 51], color=c_proc_border, lw=1.5, zorder=4)
    ax.text(80, 55.5, "0.0", fontsize=12, fontweight='bold', ha='center', va='center', color='#15803D', zorder=4)
    ax.text(80, 43, "MOVIE\nRECOMMENDATION\nSYSTEM", fontsize=11, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)
    ax.text(80, 31, "(TF-IDF, SVD & ANN)", fontsize=8.5, fontweight='bold', ha='center', color='#15803D', zorder=4)

    # 3. External Entity: ADMINISTRATOR (Top Right)
    ax.add_patch(patches.Rectangle((122, 48), 28, 24, facecolor=c_ent_bg, edgecolor=c_ent_border, lw=2.2, zorder=3))
    ax.text(136, 66, "EXTERNAL ENTITY", fontsize=8.5, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(136, 58, "ADMINISTRATOR", fontsize=11.5, fontweight='bold', ha='center', va='center', color='#0F172A')

    # 4. External Entity: TMDB / OMDb API (Bottom Right)
    ax.add_patch(patches.Rectangle((122, 14), 28, 24, facecolor=c_ext_bg, edgecolor=c_ext_border, lw=2.2, zorder=3))
    ax.text(136, 32, "EXTERNAL SERVICE", fontsize=8.5, fontweight='bold', ha='center', color='#B45309')
    ax.text(136, 24, "TMDB / OMDb API\nPOSTER SERVICE", fontsize=10.5, fontweight='bold', ha='center', va='center', color='#0F172A')

    # --- PERFECT STRAIGHT HORIZONTAL & ORTHOGONAL FLOW ARROWS ---
    # User -> Process (Straight Horizontal line at y=50)
    ax.annotate("", xy=(62, 50), xytext=(38, 50),
                arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.8, mutation_scale=14), zorder=2)
    ax.text(50, 53.5, "1. Search Query, Ratings (1-5★),\nWatchlist & User Preferences", 
            fontsize=8, fontweight='bold', ha='center', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # Process -> User (Straight Horizontal line at y=36)
    ax.annotate("", xy=(38, 36), xytext=(62, 36),
                arrowprops=dict(arrowstyle="->", color='#059669', lw=1.8, mutation_scale=14), zorder=2)
    ax.text(50, 32.5, "2. Top-N Movie Recommendations,\nPosters & Taste Radar Charts", 
            fontsize=8, fontweight='bold', ha='center', color='#059669',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # Admin -> Process (Orthogonal 90-degree step: From Admin (122, 63) -> (100, 63) -> (100, 50) -> Process)
    ax.plot([122, 102], [63, 63], color='#1E40AF', lw=1.8, zorder=2)
    ax.plot([102, 102], [63, 50], color='#1E40AF', lw=1.8, zorder=2)
    ax.annotate("", xy=(97, 50), xytext=(102, 50),
                arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.8, mutation_scale=14), zorder=2)
    ax.text(112, 66, "3. Retrain Trigger & Hyperparameters", fontsize=7.5, fontweight='bold', ha='center', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # Process -> Admin (Orthogonal 90-degree step: From Process (97, 43) -> (110, 43) -> (110, 54) -> (122, 54))
    ax.plot([97, 110], [43, 43], color='#059669', lw=1.8, zorder=2)
    ax.plot([110, 110], [43, 54], color='#059669', lw=1.8, zorder=2)
    ax.annotate("", xy=(122, 54), xytext=(110, 54),
                arrowprops=dict(arrowstyle="->", color='#059669', lw=1.8, mutation_scale=14), zorder=2)
    ax.text(110, 40, "4. Evaluation Metrics (ROC, Loss)", fontsize=7.5, fontweight='bold', ha='center', color='#059669',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # Process -> API (Orthogonal 90-degree step: From Process (97, 36) -> (110, 36) -> (110, 29) -> (122, 29))
    ax.plot([97, 110], [36, 36], color='#B45309', lw=1.8, zorder=2)
    ax.plot([110, 110], [36, 29], color='#B45309', lw=1.8, zorder=2)
    ax.annotate("", xy=(122, 29), xytext=(110, 29),
                arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.8, mutation_scale=14), zorder=2)
    ax.text(110, 38.5, "5. Metadata Fetch Query", fontsize=7.5, fontweight='bold', ha='center', color='#B45309',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # API -> Process (Orthogonal 90-degree step: From API (122, 19) -> (100, 19) -> (100, 36) -> (97, 36))
    ax.plot([122, 100], [19, 19], color='#B45309', lw=1.8, zorder=2)
    ax.plot([100, 100], [19, 36], color='#B45309', lw=1.8, zorder=2)
    ax.annotate("", xy=(97, 36), xytext=(100, 36),
                arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.8, mutation_scale=14), zorder=2)
    ax.text(111, 16, "6. Posters & Cast Details", fontsize=7.5, fontweight='bold', ha='center', color='#B45309',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_0.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_0_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Straight-Line DFD Level 0 to", p1, "and", p2)

# -------------------------------------------------------------
# 2. DFD LEVEL 1 (FUNCTIONAL DECOMPOSITION) - 100% ORTHOGONAL
# -------------------------------------------------------------
def generate_dfd_level1():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # Title
    ax.text(90, 114, "DATA FLOW DIAGRAM (DFD) - LEVEL 1", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(90, 110, "Functional Decomposition | All Straight Orthogonal (90°) Flow Lines", 
            fontsize=11.5, fontstyle='italic', ha='center', va='center', color='#475569')

    c_ent_bg = '#EFF6FF'
    c_ent_border = '#1E40AF'
    c_proc_bg = '#F0FDF4'
    c_proc_border = '#15803D'
    c_store_bg = '#FEF2F2'
    c_store_border = '#DC2626'
    
    # 1. External Entity: USER (Left)
    ax.add_patch(patches.Rectangle((6, 40), 22, 42, facecolor=c_ent_bg, edgecolor=c_ent_border, lw=2.2, zorder=3))
    ax.text(17, 75, "EXTERNAL ENTITY", fontsize=8, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(17, 63, "USER\n(Movie Buff)", fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(17, 50, "[Web Client]", fontsize=8, ha='center', color='#64748B')

    # 2. External Entity: ADMIN (Top Right)
    ax.add_patch(patches.Rectangle((152, 90), 22, 22, facecolor=c_ent_bg, edgecolor=c_ent_border, lw=2.2, zorder=3))
    ax.text(163, 106, "EXTERNAL ENTITY", fontsize=8, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(163, 98, "ADMINISTRATOR", fontsize=10.5, fontweight='bold', ha='center', va='center')

    # Draw Process Circle
    def draw_proc(cx, cy, r, num, title, fill=c_proc_bg, border=c_proc_border):
        circ = patches.Circle((cx, cy), r, facecolor=fill, edgecolor=border, lw=2.2, zorder=3)
        ax.add_patch(circ)
        chord_y = cy + r*0.35
        half_w = (r**2 - (chord_y - cy)**2)**0.5
        ax.plot([cx - half_w, cx + half_w], [chord_y, chord_y], color=border, lw=1.2, zorder=4)
        ax.text(cx, cy + r*0.65, num, fontsize=9.5, fontweight='bold', ha='center', va='center', color=border, zorder=4)
        ax.text(cx, cy - r*0.15, title, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)

    # Draw Data Store
    def draw_store(x, y, w, h, code, name):
        ax.plot([x, x+w, x+w, x], [y+h, y+h, y, y], color=c_store_border, lw=1.8, zorder=3)
        ax.plot([x+6, x+6], [y, y+h], color=c_store_border, lw=1.2, zorder=3)
        ax.fill_between([x, x+w], [y, y], [y+h, y+h], color=c_store_bg, zorder=1)
        ax.text(x+3, y+h/2, code, fontsize=8, fontweight='bold', ha='center', va='center', color='#991B1B', zorder=4)
        ax.text(x+8+(w-8)/2, y+h/2, name, fontsize=8, fontweight='bold', ha='center', va='center', color='#7F1D1D', zorder=4)

    # 5 Processes in clean grid
    draw_proc(55, 95, 11, "1.0", "User Auth &\nProfile Mgmt")
    draw_proc(55, 60, 11, "2.0", "Movie Search\n& Filter Engine")
    draw_proc(105, 60, 13, "3.0", "Hybrid Rec Engine\n(TF-IDF, SVD & ANN)", fill='#FEFCE8', border='#CA8A04')
    draw_proc(55, 25, 11, "4.0", "Rating & Watchlist\nManagement")
    draw_proc(155, 25, 11, "5.0", "Taste Analytics &\nRadar Profiling")

    # 4 Data Stores
    draw_store(92, 91, 38, 8, "D1", "User Accounts & Profiles")
    draw_store(142, 56, 34, 8, "D2", "Movie Metadata & Vectors")
    draw_store(92, 21, 34, 8, "D3", "User Ratings Database")
    draw_store(142, 40, 34, 8, "D4", "Watchlist & Interactions")

    # --- ALL FLOWS DRAWN USING EXACT STRAIGHT & ORTHOGONAL SEGMENTS ---
    # User -> 1.0 (Orthogonal: (28, 75) -> (40, 75) -> (40, 95) -> (44, 95))
    ax.plot([28, 40], [75, 75], color='#1E40AF', lw=1.6)
    ax.plot([40, 40], [75, 95], color='#1E40AF', lw=1.6)
    ax.annotate("", xy=(44, 95), xytext=(40, 95), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.6, mutation_scale=12))
    ax.text(34, 85, "Login / Signup", fontsize=7.5, fontweight='bold', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # 1.0 <-> D1 (Straight Horizontal line at y=95)
    ax.annotate("", xy=(92, 95), xytext=(66, 95), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6, mutation_scale=12))
    ax.text(79, 98, "User Read/Write", fontsize=7.5, ha='center', color='#334155')

    # User -> 2.0 (Straight Horizontal line at y=63)
    ax.annotate("", xy=(44, 63), xytext=(28, 63), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.6, mutation_scale=12))
    ax.text(36, 66, "Search Query", fontsize=7.5, ha='center', color='#1E40AF')

    # 2.0 -> User (Straight Horizontal line at y=57)
    ax.annotate("", xy=(28, 57), xytext=(44, 57), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.6, mutation_scale=12))
    ax.text(36, 53, "Movie Results", fontsize=7.5, ha='center', color='#1E40AF')

    # 2.0 -> 3.0 (Straight Horizontal line at y=60)
    ax.annotate("", xy=(92, 60), xytext=(66, 60), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.6, mutation_scale=12))
    ax.text(79, 63, "Selected Film", fontsize=7.5, ha='center', color='#B45309')

    # D2 -> 3.0 (Straight Horizontal line at y=60)
    ax.annotate("", xy=(118, 60), xytext=(142, 60), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.6, mutation_scale=12))
    ax.text(130, 63, "TF-IDF Vectors", fontsize=7.5, ha='center', color='#B45309')

    # D3 -> 3.0 (Straight Vertical line at x=105)
    ax.annotate("", xy=(105, 47), xytext=(105, 29), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.6, mutation_scale=12))
    ax.text(105, 38, "User Ratings Matrix", fontsize=7.5, ha='center', color='#B45309',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # 3.0 -> User (Orthogonal line from (105, 73) -> (105, 83) -> (28, 83))
    ax.plot([105, 105], [73, 83], color='#059669', lw=1.8)
    ax.plot([105, 28], [83, 83], color='#059669', lw=1.8)
    ax.annotate("", xy=(28, 80), xytext=(28, 83), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.8, mutation_scale=12))
    ax.text(66, 86, "Top-N Recommendations & Predicted Likelihood", fontsize=8, fontweight='bold', ha='center', color='#059669',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # User -> 4.0 (Orthogonal line from (28, 45) -> (40, 45) -> (40, 25) -> (44, 25))
    ax.plot([28, 40], [45, 45], color='#1E40AF', lw=1.6)
    ax.plot([40, 40], [45, 25], color='#1E40AF', lw=1.6)
    ax.annotate("", xy=(44, 25), xytext=(40, 25), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.6, mutation_scale=12))
    ax.text(34, 35, "1-5★ Rating & Watchlist Add", fontsize=7.5, fontweight='bold', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # 4.0 -> D3 (Straight Horizontal line at y=25)
    ax.annotate("", xy=(92, 25), xytext=(66, 25), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.6, mutation_scale=12))
    ax.text(79, 28, "Save Ratings", fontsize=7.5, ha='center', color='#DC2626')

    # 4.0 -> D4 (Orthogonal from (66, 22) -> (80, 22) -> (80, 44) -> (142, 44))
    ax.plot([66, 80], [22, 22], color='#DC2626', lw=1.6)
    ax.plot([80, 80], [22, 44], color='#DC2626', lw=1.6)
    ax.annotate("", xy=(142, 44), xytext=(80, 44), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.6, mutation_scale=12))
    ax.text(111, 46.5, "Save Watchlist", fontsize=7.5, ha='center', color='#DC2626')

    # D3 -> 5.0 (Straight Horizontal line at y=25)
    ax.annotate("", xy=(144, 25), xytext=(126, 25), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6, mutation_scale=12))
    ax.text(135, 28, "User History", fontsize=7.5, ha='center', color='#334155')

    # 5.0 -> User (Orthogonal line from (155, 14) -> (155, 8) -> (17, 8) -> (17, 40))
    ax.plot([155, 155], [14, 8], color='#7C3AED', lw=1.8)
    ax.plot([155, 17], [8, 8], color='#7C3AED', lw=1.8)
    ax.annotate("", xy=(17, 40), xytext=(17, 8), arrowprops=dict(arrowstyle="->", color='#7C3AED', lw=1.8, mutation_scale=12))
    ax.text(86, 11, "Interactive Taste Radar Analytics & Genre Breakdown", fontsize=8, fontweight='bold', ha='center', color='#7C3AED',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # Admin <-> 3.0 (Orthogonal: (152, 101) -> (105, 101) -> (105, 73))
    ax.plot([152, 110], [101, 101], color='#1E40AF', lw=1.6)
    ax.annotate("", xy=(110, 73), xytext=(110, 101), arrowprops=dict(arrowstyle="->", color='#1E40AF', lw=1.6, mutation_scale=12))
    ax.text(131, 104, "Retrain Command & Model Config", fontsize=7.5, fontweight='bold', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_1.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_1_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Straight-Line DFD Level 1 to", p1, "and", p2)

# -------------------------------------------------------------
# 3. DFD LEVEL 2 (RECOMMENDATION PIPELINE) - 100% ORTHOGONAL
# -------------------------------------------------------------
def generate_dfd_level2():
    fig, ax = plt.subplots(figsize=(18, 10), dpi=300)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(90, 95, "DATA FLOW DIAGRAM (DFD) - LEVEL 2", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(90, 90.5, "Process 3.0: Hybrid Recommendation Engine & Deep ML Pipeline | Straight Orthogonal Lines", 
            fontsize=11.5, fontstyle='italic', ha='center', va='center', color='#475569')

    c_proc_bg = '#F0FDF4'
    c_proc_border = '#15803D'
    c_store_bg = '#FEF2F2'
    c_store_border = '#DC2626'

    def draw_store(x, y, w, h, code, name):
        ax.plot([x, x+w, x+w, x], [y+h, y+h, y, y], color=c_store_border, lw=1.8, zorder=3)
        ax.plot([x+6, x+6], [y, y+h], color=c_store_border, lw=1.2, zorder=3)
        ax.fill_between([x, x+w], [y, y], [y+h, y+h], color=c_store_bg, zorder=1)
        ax.text(x+3, y+h/2, code, fontsize=8, fontweight='bold', ha='center', va='center', color='#991B1B', zorder=4)
        ax.text(x+8+(w-8)/2, y+h/2, name, fontsize=8, fontweight='bold', ha='center', va='center', color='#7F1D1D', zorder=4)

    def draw_proc(cx, cy, r, num, title, fill=c_proc_bg, border=c_proc_border):
        circ = patches.Circle((cx, cy), r, facecolor=fill, edgecolor=border, lw=2.2, zorder=3)
        ax.add_patch(circ)
        chord_y = cy + r*0.35
        half_w = (r**2 - (chord_y - cy)**2)**0.5
        ax.plot([cx - half_w, cx + half_w], [chord_y, chord_y], color=border, lw=1.2, zorder=4)
        ax.text(cx, cy + r*0.65, num, fontsize=9.5, fontweight='bold', ha='center', va='center', color=border, zorder=4)
        ax.text(cx, cy - r*0.15, title, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)

    # Data Stores on Left
    draw_store(8, 68, 32, 8, "D2", "Movie Feature Vectors")
    draw_store(8, 26, 32, 8, "D3", "User Ratings Matrix")
    draw_store(60, 80, 32, 8, "D5", "Neural Network Weights")

    # 4 Sub-Processes in Pipeline
    draw_proc(65, 62, 11, "3.1", "TF-IDF Vectorizer\n& Cosine Matching")
    draw_proc(65, 30, 11, "3.2", "Truncated SVD\nMatrix Factorization")
    draw_proc(115, 46, 12, "3.3", "3-Layer Keras ANN\nLikelihood Classifier")
    draw_proc(155, 46, 12, "3.4", "Hybrid Ranker &\nDiversity Filter", fill='#FEFCE8', border='#CA8A04')

    # Output Box (Bottom Right)
    ax.add_patch(patches.Rectangle((140, 10), 30, 18, facecolor='#EFF6FF', edgecolor='#1D4ED8', lw=2, zorder=3))
    ax.text(155, 21, "USER INTERFACE\nTop-10 Recommended Films", fontsize=9, fontweight='bold', ha='center', va='center', color='#1E40AF')

    # --- ALL FLOWS DRAWN USING EXACT STRAIGHT & ORTHOGONAL LINES ---
    # D2 -> 3.1 (Straight Horizontal: (40, 72) -> (54, 72) -> (54, 62))
    ax.plot([40, 54], [72, 72], color='#334155', lw=1.6)
    ax.annotate("", xy=(54, 62), xytext=(54, 72), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6, mutation_scale=12))
    ax.text(47, 75, "Feature Matrix", fontsize=7.5, ha='center', color='#334155')

    # D3 -> 3.2 (Straight Horizontal line at y=30)
    ax.annotate("", xy=(54, 30), xytext=(40, 30), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6, mutation_scale=12))
    ax.text(47, 33, "Ratings Matrix", fontsize=7.5, ha='center', color='#334155')

    # D5 -> 3.3 (Orthogonal line from (92, 84) -> (115, 84) -> (115, 58))
    ax.plot([92, 115], [84, 84], color='#334155', lw=1.6)
    ax.annotate("", xy=(115, 58), xytext=(115, 84), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6, mutation_scale=12))
    ax.text(103, 87, "Trained Dense Weights", fontsize=7.5, ha='center', color='#334155')

    # 3.1 -> 3.3 (Orthogonal line from (76, 62) -> (90, 62) -> (90, 50) -> (103, 50))
    ax.plot([76, 90], [62, 62], color='#2563EB', lw=1.6)
    ax.plot([90, 90], [62, 50], color='#2563EB', lw=1.6)
    ax.annotate("", xy=(103, 50), xytext=(90, 50), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.6, mutation_scale=12))
    ax.text(83, 65, "Content Vectors", fontsize=7.5, color='#2563EB')

    # 3.2 -> 3.3 (Orthogonal line from (76, 30) -> (90, 30) -> (90, 42) -> (103, 42))
    ax.plot([76, 90], [30, 30], color='#059669', lw=1.6)
    ax.plot([90, 90], [30, 42], color='#059669', lw=1.6)
    ax.annotate("", xy=(103, 42), xytext=(90, 42), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.6, mutation_scale=12))
    ax.text(83, 27, "Latent Factors", fontsize=7.5, color='#059669')

    # 3.1 -> 3.4 (Orthogonal line from (76, 68) -> (138, 68) -> (146, 56))
    ax.plot([76, 146], [68, 68], color='#2563EB', lw=1.6)
    ax.annotate("", xy=(146, 56), xytext=(146, 68), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.6, mutation_scale=12))
    ax.text(111, 71, "Content Cosine Scores [0.0 - 1.0]", fontsize=8, fontweight='bold', ha='center', color='#2563EB',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # 3.2 -> 3.4 (Orthogonal line from (76, 24) -> (146, 24) -> (146, 36))
    ax.plot([76, 146], [24, 24], color='#059669', lw=1.6)
    ax.annotate("", xy=(146, 36), xytext=(146, 24), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.6, mutation_scale=12))
    ax.text(111, 20.5, "Predicted SVD Ratings (1.0 - 5.0)", fontsize=8, fontweight='bold', ha='center', color='#059669',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.6))

    # 3.3 -> 3.4 (Straight Horizontal line at y=46)
    ax.annotate("", xy=(143, 46), xytext=(127, 46), arrowprops=dict(arrowstyle="->", color='#7C3AED', lw=1.6, mutation_scale=12))
    ax.text(135, 49, "P(Like)", fontsize=8, fontweight='bold', ha='center', color='#7C3AED')

    # 3.4 -> Output Box (Straight Vertical line at x=155)
    ax.annotate("", xy=(155, 28), xytext=(155, 34), arrowprops=dict(arrowstyle="->", color='#B45309', lw=1.8, mutation_scale=14))
    ax.text(155, 31, "Top-N", fontsize=7.5, fontweight='bold', ha='center', color='#B45309')

    plt.tight_layout()
    p1 = 'reports/figures/dfd_level_2.png'
    p2 = os.path.join(DESKTOP_DIR, 'DFD_Level_2_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Straight-Line DFD Level 2 to", p1, "and", p2)

# -------------------------------------------------------------
# 4. ER DIAGRAM (ACADEMIC CHEN NOTATION - PERFECT RECTANGULAR GRID)
# -------------------------------------------------------------
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(20, 13), dpi=300)
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 130)
    ax.axis('off')

    # Title
    ax.text(100, 124, "ENTITY-RELATIONSHIP (ER) DIAGRAM", 
            fontsize=19, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(100, 120, "Academic Chen Notation Model | Solid Underline = Primary Key | Dashed Underline = Foreign Key | No PK/FK Labels", 
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#475569')

    c_ent_bg = '#EFF6FF'
    c_ent_border = '#1D4ED8'
    c_rel_bg = '#FEFCE8'
    c_rel_border = '#CA8A04'
    c_att_bg = '#FFFFFF'
    c_att_border = '#64748B'
    c_line = '#475569'

    def draw_entity(x, y, w, h, name):
        ax.add_patch(patches.Rectangle((x-w/2, y-h/2), w, h, facecolor=c_ent_bg, edgecolor=c_ent_border, lw=2.2, zorder=3))
        ax.text(x, y, name, fontsize=12, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)

    def draw_relationship(x, y, size_w, size_h, name):
        pts = [[x, y+size_h], [x+size_w, y], [x, y-size_h], [x-size_w, y]]
        ax.add_patch(patches.Polygon(pts, facecolor=c_rel_bg, edgecolor=c_rel_border, lw=2.2, zorder=3))
        ax.text(x, y, name, fontsize=10, fontweight='bold', ha='center', va='center', color='#854D0E', zorder=4)

    def draw_attr(x, y, name, ent_x, ent_y, is_pk=False, is_fk=False, rx=8.0, ry=3.2):
        # Straight connecting line to entity boundary
        ax.plot([x, ent_x], [y, ent_y], color=c_line, lw=1.2, zorder=1)
        ax.add_patch(patches.Ellipse((x, y), rx*2, ry*2, facecolor=c_att_bg, edgecolor=c_att_border, lw=1.4, zorder=3))
        ax.text(x, y, name, fontsize=8.5, ha='center', va='center', color='#0F172A', zorder=4)
        
        tw = len(name) * 0.42
        if is_pk:
            ax.plot([x-tw, x+tw], [y-1.4, y-1.4], color='#0F172A', lw=1.6, zorder=5)
        elif is_fk:
            ax.plot([x-tw, x+tw], [y-1.4, y-1.4], color='#0F172A', lw=1.6, linestyle='--', zorder=5)

    # 4 Entities in clean square grid
    draw_entity(45, 85, 26, 12, "USER")
    draw_entity(155, 85, 26, 12, "MOVIE")
    draw_entity(155, 30, 26, 12, "GENRE")
    draw_entity(45, 30, 26, 12, "WATCHLIST")

    # 4 Relationships
    # 1. USER - RATES - MOVIE (Straight Horizontal line at y=85)
    draw_relationship(100, 85, 10, 6, "RATES")
    ax.plot([58, 90], [85, 85], color=c_line, lw=2)
    ax.plot([110, 142], [85, 85], color=c_line, lw=2)
    ax.text(62, 88, "1", fontsize=11, fontweight='bold', color='#1E40AF')
    ax.text(138, 88, "N", fontsize=11, fontweight='bold', color='#1E40AF')

    # Attributes of RATES
    draw_attr(100, 102, "rating_val", 100, 91)
    draw_attr(100, 68, "timestamp", 100, 79)

    # 2. MOVIE - BELONGS_TO - GENRE (Straight Vertical line at x=155)
    draw_relationship(155, 57.5, 10, 6, "BELONGS_TO")
    ax.plot([155, 155], [79, 63.5], color=c_line, lw=2)
    ax.plot([155, 155], [51.5, 36], color=c_line, lw=2)
    ax.text(158, 74, "M", fontsize=10.5, fontweight='bold', color='#1E40AF')
    ax.text(158, 41, "N", fontsize=10.5, fontweight='bold', color='#1E40AF')

    # 3. USER - MAINTAINS - WATCHLIST (Straight Vertical line at x=45)
    draw_relationship(45, 57.5, 10, 6, "MAINTAINS")
    ax.plot([45, 45], [79, 63.5], color=c_line, lw=2)
    ax.plot([45, 45], [51.5, 36], color=c_line, lw=2)
    ax.text(48, 74, "1", fontsize=10.5, fontweight='bold', color='#1E40AF')
    ax.text(48, 41, "N", fontsize=10.5, fontweight='bold', color='#1E40AF')

    # 4. WATCHLIST - CONTAINS - MOVIE (Orthogonal: (58, 30) -> (100, 30) -> (142, 79))
    draw_relationship(100, 30, 10, 6, "CONTAINS")
    ax.plot([58, 90], [30, 30], color=c_line, lw=2)
    ax.plot([110, 135], [30, 30], color=c_line, lw=2)
    ax.plot([135, 155], [30, 79], color=c_line, lw=2)
    ax.text(62, 33, "N", fontsize=10.5, fontweight='bold', color='#1E40AF')
    ax.text(142, 60, "1", fontsize=10.5, fontweight='bold', color='#1E40AF')

    # USER Attributes (Spaced cleanly to left and top)
    draw_attr(18, 105, "user_id", 45, 85, is_pk=True)
    draw_attr(36, 110, "username", 45, 85)
    draw_attr(56, 110, "email", 45, 85)
    draw_attr(14, 88, "password_hash", 45, 85, rx=9.0)
    draw_attr(14, 72, "created_at", 45, 85)

    # MOVIE Attributes (Spaced cleanly to right and top)
    draw_attr(138, 110, "movie_id", 155, 85, is_pk=True)
    draw_attr(158, 110, "title", 155, 85)
    draw_attr(178, 110, "release_year", 155, 85, rx=8.5)
    draw_attr(188, 95, "vote_average", 155, 85, rx=8.5)
    draw_attr(188, 82, "vote_count", 155, 85)
    draw_attr(188, 69, "poster_url", 155, 85)
    draw_attr(128, 72, "overview", 155, 85)

    # GENRE Attributes
    draw_attr(140, 10, "genre_id", 155, 30, is_pk=True)
    draw_attr(170, 10, "genre_name", 155, 30)

    # WATCHLIST Attributes
    draw_attr(14, 42, "watchlist_id", 45, 30, is_pk=True, rx=9.0)
    draw_attr(14, 28, "user_id", 45, 30, is_fk=True)
    draw_attr(14, 14, "movie_id", 45, 30, is_fk=True)
    draw_attr(42, 10, "added_date", 45, 30)
    draw_attr(64, 10, "status", 45, 30)

    # Legend Box
    ax.add_patch(patches.Rectangle((72, 5), 56, 12, facecolor='#F8FAFC', edgecolor='#94A3B8', lw=1.2, zorder=3))
    ax.text(100, 13.5, "Academic Notation Convention:", fontsize=8.5, fontweight='bold', ha='center', color='#1E293B')
    ax.plot([78, 90], [9, 9], color='#0F172A', lw=2.0)
    ax.text(92, 8.5, "Primary Key (Solid Underline)", fontsize=8, color='#334155')
    ax.plot([78, 90], [5.5, 5.5], color='#0F172A', lw=2.0, linestyle='--')
    ax.text(92, 5, "Foreign Key (Dashed Underline)", fontsize=8, color='#334155')

    plt.tight_layout()
    p1 = 'reports/figures/er_diagram_academic.png'
    p2 = os.path.join(DESKTOP_DIR, 'ER_Diagram_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Straight-Line ER Diagram to", p1, "and", p2)

# -------------------------------------------------------------
# 5. USE CASE DIAGRAM (STANDARD UML 2.0 - STRAIGHT ALIGNED CONNECTORS)
# -------------------------------------------------------------
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # Title
    ax.text(90, 114, "USE CASE DIAGRAM", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(90, 110, "Movie Recommendation & Discovery System | Standard UML 2.0 Specification", 
            fontsize=11.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # System Boundary Box
    ax.add_patch(patches.Rectangle((42, 6), 96, 100, facecolor='#F8FAFC', edgecolor='#0284C7', lw=2.5, zorder=1))
    ax.text(90, 102, "System: Movie Recommendation System", fontsize=12, fontweight='bold', ha='center', color='#0369A1')

    # Stick Figures
    def draw_actor(x, y, label):
        ax.add_patch(patches.Circle((x, y+8), 3.2, facecolor='#E2E8F0', edgecolor='#0F172A', lw=2.2, zorder=4))
        ax.plot([x, x], [y+4.8, y-4], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x-5.5, x+5.5], [y+1.5, y+1.5], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x, x-4.5], [y-4, y-11], color='#0F172A', lw=2.2, zorder=4)
        ax.plot([x, x+4.5], [y-4, y-11], color='#0F172A', lw=2.2, zorder=4)
        ax.text(x, y-15, label, fontsize=9.5, fontweight='bold', ha='center', va='top', color='#0F172A')

    draw_actor(20, 60, "USER\n(Movie Buff)")
    draw_actor(160, 60, "ADMINISTRATOR\n/ ML ENGINEER")

    def draw_uc(x, y, text, rx=13.5, ry=3.8, fill='#FFFFFF', border='#0284C7'):
        ax.add_patch(patches.Ellipse((x, y), rx*2, ry*2, facecolor=fill, edgecolor=border, lw=1.8, zorder=3))
        ax.text(x, y, text, fontsize=8, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)

    # Column 1: User Direct Use Cases (x=68)
    draw_uc(68, 92, "Register / User Login")
    draw_uc(68, 79, "Search & Filter Movies")
    draw_uc(68, 66, "View Movie Details & Posters")
    draw_uc(68, 53, "Submit 1-5 Star Ratings")
    draw_uc(68, 40, "Get Content-Based Recs")
    draw_uc(68, 27, "Get Collaborative SVD Recs")
    draw_uc(68, 14, "Manage Watchlist & Favorites")

    # Column 2: Advanced Sub-processes & Admin Use Cases (x=112)
    draw_uc(112, 92, "Retrain / Update ML Models", fill='#FEF2F2', border='#DC2626')
    draw_uc(112, 79, "Evaluate Metrics (ROC/Loss)", fill='#FEF2F2', border='#DC2626')
    draw_uc(112, 63, "View Taste Radar Analytics")
    draw_uc(112, 40, "Extract TF-IDF Features", fill='#EFF6FF', border='#3B82F6')
    draw_uc(112, 27, "Predict Likelihood (ANN)", fill='#EFF6FF', border='#3B82F6')

    # Association Lines from User Actor (Straight ray connectors)
    user_hand = (26, 61.5)
    for uy in [92, 79, 66, 53, 40, 27, 14]:
        ax.plot([user_hand[0], 54.5], [user_hand[1], uy], color='#334155', lw=1.5, zorder=2)
    # User to Taste Radar
    ax.plot([user_hand[0], 98.5], [user_hand[1], 63], color='#334155', lw=1.5, zorder=2)

    # Association Lines from Admin Actor
    admin_hand = (154, 61.5)
    ax.plot([admin_hand[0], 125.5], [admin_hand[1], 92], color='#DC2626', lw=1.5, zorder=2)
    ax.plot([admin_hand[0], 125.5], [admin_hand[1], 79], color='#DC2626', lw=1.5, zorder=2)

    # Include Relationship (Content Recs <<include>> Extract TF-IDF) - Perfectly Horizontal
    ax.annotate("", xy=(98.5, 40), xytext=(81.5, 40),
                arrowprops=dict(arrowstyle="->", linestyle='--', color='#2563EB', lw=1.6, mutation_scale=12))
    ax.text(90, 43, "<<include>>", fontsize=7.5, fontweight='bold', ha='center', color='#2563EB')

    # Extend Relationship (Collaborative SVD <<extend>> Predict ANN) - Perfectly Horizontal
    ax.annotate("", xy=(81.5, 27), xytext=(98.5, 27),
                arrowprops=dict(arrowstyle="->", linestyle='--', color='#7C3AED', lw=1.6, mutation_scale=12))
    ax.text(90, 30, "<<extend>>", fontsize=7.5, fontweight='bold', ha='center', color='#7C3AED')

    plt.tight_layout()
    p1 = 'reports/figures/use_case_diagram.png'
    p2 = os.path.join(DESKTOP_DIR, 'Use_Case_Diagram_Movie_Recommendation_System.png')
    fig.savefig(p1, bbox_inches='tight', dpi=300)
    fig.savefig(p2, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Straight-Line Use Case Diagram to", p1, "and", p2)

if __name__ == '__main__':
    generate_dfd_level0()
    generate_dfd_level1()
    generate_dfd_level2()
    generate_er_diagram()
    generate_use_case_diagram()
