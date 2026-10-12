import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os

DESKTOP_DIR = r"C:\Users\satis\OneDrive\Desktop"
OUTPUT_PPTX = os.path.join(DESKTOP_DIR, "Movie_Recommendation_System_Presentation.pptx")
LOCAL_PPTX = "reports/Movie_Recommendation_System_Presentation.pptx"
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "movierecommandation_system screen shot")

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Palette
    BG_DARK = RGBColor(15, 23, 42)      # Deep Slate 900
    BG_CARD = RGBColor(30, 41, 59)      # Slate 800
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_BLUE = RGBColor(59, 130, 246) # Blue 500
    ACCENT_CYAN = RGBColor(6, 182, 212)  # Cyan 500
    ACCENT_GOLD = RGBColor(245, 158, 11) # Amber 500
    ACCENT_GREEN = RGBColor(16, 185, 129)# Emerald 500

    def set_slide_background(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = BG_DARK

    def add_header(slide, title_text, category_text="MOVIE RECOMMENDATION SYSTEM"):
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE
        
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.7))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ACCENT_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = accent_color
        shape.line.width = Pt(1.5)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.space_after = Pt(8)
        
        for bullet in body_bullets:
            p = tf.add_paragraph()
            p.text = "• " + bullet
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_WHITE
            p.space_after = Pt(5)

    def add_fitted_image_slide(slide, title_text, img_path, subtitle=""):
        add_header(slide, title_text)
        if subtitle:
            tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.35))
            p = tb.text_frame.paragraphs[0]
            p.text = subtitle
            p.font.size = Pt(12)
            p.font.italic = True
            p.font.color.rgb = TEXT_MUTED
            
        if os.path.exists(img_path):
            with Image.open(img_path) as img:
                orig_w, orig_h = img.size
                aspect = orig_w / orig_h
                
            max_w = 11.0
            max_h = 5.0
            
            if (max_w / max_h) > aspect:
                final_h = max_h
                final_w = final_h * aspect
            else:
                final_w = max_w
                final_h = final_w / aspect
                
            left = (13.333 - final_w) / 2.0
            top = 1.65 + (5.1 - final_h) / 2.0
            
            slide.shapes.add_picture(img_path, Inches(left), Inches(top), width=Inches(final_w), height=Inches(final_h))
        else:
            tb_err = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(8), Inches(2))
            tb_err.text_frame.paragraphs[0].text = f"[Diagram Image Missing: {img_path}]"

    def add_ui_screenshot_slide(slide, title_text, img_filename, feature_bullets, badge_text="WEB UI WALKTHROUGH"):
        add_header(slide, title_text, badge_text)
        
        # Left Side: Info Card (width 4.4 inches)
        add_card(slide, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.3),
                 "Key Features & Architecture", feature_bullets, ACCENT_CYAN)
        
        # Right Side: Image Card Container
        img_path = os.path.join(SCREENSHOTS_DIR, img_filename)
        if os.path.exists(img_path):
            with Image.open(img_path) as img:
                orig_w, orig_h = img.size
                aspect = orig_w / orig_h
                
            max_w = 6.8
            max_h = 5.3
            
            if (max_w / max_h) > aspect:
                final_h = max_h
                final_w = final_h * aspect
            else:
                final_w = max_w
                final_h = final_w / aspect
                
            left = 5.6 + (6.8 - final_w) / 2.0
            top = 1.6 + (5.3 - final_h) / 2.0
            
            # Border frame
            frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left - 0.05), Inches(top - 0.05), Inches(final_w + 0.1), Inches(final_h + 0.1))
            frame.fill.solid()
            frame.fill.fore_color.rgb = BG_CARD
            frame.line.color.rgb = ACCENT_BLUE
            frame.line.width = Pt(1.5)
            
            slide.shapes.add_picture(img_path, Inches(left), Inches(top), width=Inches(final_w), height=Inches(final_h))
        else:
            tb_err = slide.shapes.add_textbox(Inches(6), Inches(3), Inches(6), Inches(2))
            tb_err.text_frame.paragraphs[0].text = f"[Screenshot Missing: {img_filename}]"

    # =========================================================
    # SLIDE 1: TITLE SLIDE (WITH GUIDE MS. POOJA PANCHAL)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(3.0))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "MOVIE RECOMMENDATION &\nDISCOVERY SYSTEM"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_WHITE
    p0.space_after = Pt(10)
    
    p1 = tf1.add_paragraph()
    p1.text = "A Hybrid Machine Learning Architecture utilizing TF-IDF, Collaborative Truncated SVD, and Deep ANN Classification"
    p1.font.size = Pt(15)
    p1.font.italic = True
    p1.font.color.rgb = ACCENT_CYAN

    add_card(s1, Inches(1.0), Inches(4.7), Inches(11.3), Inches(2.1), 
             "Academic Capstone Project (TY B.Tech Computer Engineering | 2025-2026)", 
             ["Student Name: Vivek Patil (Roll No: TY-COMP-054 | Seat No: B221054)",
              "Project Guide: Ms. Pooja Panchal (Assistant Professor, Department of Computer Engineering)",
              "Core Stack: Python 3.10+, Scikit-Learn, TensorFlow/Keras, Streamlit, SQLite3, Pytest"], ACCENT_GOLD)

    # =========================================================
    # SLIDE 2: PROJECT OVERVIEW & PROBLEM STATEMENT
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Project Overview & Problem Statement")
    
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "The Information Overload Challenge",
             ["Streaming platforms host tens of thousands of movie titles.",
              "Users suffer from 'Choice Paralysis' spending 20+ minutes browsing.",
              "Pure Content-Based filtering causes severe genre over-specialization.",
              "Pure Collaborative Filtering breaks on Cold-Start items & sparse matrices."],
             ACCENT_GOLD)
             
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Our Proposed Hybrid Solution",
             ["Combines Content-Based TF-IDF + Collaborative SVD + Deep ANN Classifier.",
              "Provides robust Cold-Start fallback using metadata cosine similarity.",
              "Reduces matrix sparsity using Truncated SVD (k=32 latent dimensions).",
              "Interactive Streamlit web app with taste radar profiles & 100% test coverage."],
             ACCENT_GREEN)

    # =========================================================
    # SLIDE 3: KEY PROJECT OBJECTIVES
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Key Project Objectives")
    
    add_card(s3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "1. Multi-Engine ML",
             ["Develop TF-IDF similarity over metadata soups (cast, crew, genre).",
              "Perform low-rank SVD decomposition for rating prediction.",
              "Train 3-layer Keras ANN for binary preference likelihood."],
             ACCENT_BLUE)
             
    add_card(s3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "2. Interactive UI",
             ["Build modern Streamlit web dashboard with movie cards.",
              "Live search, genre filtering & release year sliders.",
              "Personal Taste Profile radar charts & watchlist management."],
             ACCENT_CYAN)

    add_card(s3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "3. Reliability & Testing",
             ["Implement 83 automated unit & integration tests in Pytest.",
              "Validate mathematical symmetry of similarity metrics.",
              "Achieve 87.8% classification accuracy and 0.932 AUC-ROC."],
             ACCENT_GOLD)

    # =========================================================
    # SLIDE 4: SYSTEM ARCHITECTURE
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "High-Level System Architecture")
    
    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Frontend & Interaction Layer",
             ["Streamlit Reactive UI",
              "Vanilla CSS Glassmorphism styling",
              "Movie Poster CDN Integration",
              "Live Genre Radar Charts",
              "1-to-5 Star Interactive Ratings"],
             ACCENT_BLUE)

    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "ML & Neural Inference Engine",
             ["TF-IDF Vectorizer & Cosine Math",
              "Truncated SVD (32 Latent Factors)",
              "3-Layer Keras Neural Network",
              "Logistic Regression & Random Forest",
              "Hybrid Ranker & Diversity Filter"],
             ACCENT_CYAN)

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Data & Persistence Layer",
             ["SQLite Relational Database",
              "Users, Ratings & Watchlist Tables",
              "TMDB 10,000+ Film Metadata CSV",
              "Pickled Pre-computed Vectors",
              "Saved Keras HDF5 Model Weights"],
             ACCENT_GREEN)

    # =========================================================
    # SLIDE 5: DFD LEVEL 0
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_fitted_image_slide(s5, "Data Flow Diagram (DFD) - Level 0", 
                           os.path.join(DESKTOP_DIR, "DFD_Level_0_Movie_Recommendation_System.png"),
                           "Context Level Diagram showing external entities and straight horizontal/orthogonal data flows.")

    # =========================================================
    # SLIDE 6: DFD LEVEL 1
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_fitted_image_slide(s6, "Data Flow Diagram (DFD) - Level 1", 
                           os.path.join(DESKTOP_DIR, "DFD_Level_1_Movie_Recommendation_System.png"),
                           "Functional Decomposition into 5 core processes and 4 Gane-Sarson relational data stores.")

    # =========================================================
    # SLIDE 7: DFD LEVEL 2
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_fitted_image_slide(s7, "Data Flow Diagram (DFD) - Level 2", 
                           os.path.join(DESKTOP_DIR, "DFD_Level_2_Movie_Recommendation_System.png"),
                           "Detailed decomposition of Process 3.0: Hybrid Recommendation & Deep ML Pipeline.")

    # =========================================================
    # SLIDE 8: ER DIAGRAM
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_fitted_image_slide(s8, "Entity-Relationship (ER) Diagram", 
                           os.path.join(DESKTOP_DIR, "ER_Diagram_Movie_Recommendation_System.png"),
                           "Academic Relational Table Card Model | Solid Underline: Primary Key | Dashed Underline: Foreign Key | No PK/FK text.")

    # =========================================================
    # SLIDE 9: USE CASE DIAGRAM
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_fitted_image_slide(s9, "Use Case Diagram (Standard UML 2.0)", 
                           os.path.join(DESKTOP_DIR, "Use_Case_Diagram_Movie_Recommendation_System.png"),
                           "System boundary modeling user & administrator capabilities with «include» and «extend» relationships.")

    # =========================================================
    # SLIDE 10: ALGORITHM 1 - CONTENT-BASED TF-IDF
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Algorithm 1: Content-Based Filtering with TF-IDF")
    
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Metadata Synthesis & Tokenization",
             ["Synthesizes multi-attribute 'Metadata Soup':",
              "Overview + Genres + Cast (Top 3) + Director + Keywords.",
              "Term Frequency - Inverse Document Frequency (TF-IDF):",
              "Downweights common terms and emphasizes salient character/genre tokens.",
              "Computes high-dimensional sparse item vectors."],
             ACCENT_BLUE)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Cosine Similarity Metric",
             ["Measures directional cosine angle between item vectors:",
              "Cosine_Sim(A, B) = (A • B) / (||A|| * ||B||)",
              "Values strictly bound between 0.0 (orthogonal) and 1.0 (identical).",
              "Sub-millisecond retrieval of Top-10 nearest neighbor titles.",
              "Serves as the primary cold-start fallback when ratings are absent."],
             ACCENT_CYAN)

    # =========================================================
    # SLIDE 11: ALGORITHM 2 - COLLABORATIVE SVD
    # =========================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Algorithm 2: Collaborative Truncated SVD")
    
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Matrix Factorization Mathematics",
             ["Decomposes sparse user-item interaction matrix R (m x n):",
              "R ≈ U * Σ * V^T",
              "U (m x k): Latent user preference embeddings.",
              "Σ (k x k): Singular values indicating latent dimension weight.",
              "V^T (k x n): Latent movie feature coordinate embeddings.",
              "Reduces dimensionality to k = 32 dense latent factors."],
             ACCENT_GOLD)

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Latent Rating Prediction",
             ["Predicts unseen rating: r_hat(u, i) = mu + b_u + b_i + (U_u • V_i)",
              "Uncovers hidden semantic genres without manual tagging.",
              "Evaluated on test ratings: Achieves RMSE = 0.874 stars.",
              "Outperforms classical neighborhood-based k-NN collaborative methods."],
             ACCENT_GREEN)

    # =========================================================
    # SLIDE 12: ALGORITHM 3 - DEEP ANN CLASSIFIER
    # =========================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Algorithm 3: Deep Learning ANN Likelihood Classifier")
    
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Neural Network Architecture",
             ["Input Layer: 82 Dimensions (User Latent + Movie Vector + Genres).",
              "Dense Hidden Layer 1: 128 Neurons + ReLU + Dropout(0.3) + BatchNorm.",
              "Dense Hidden Layer 2: 64 Neurons + ReLU + Dropout(0.2) + BatchNorm.",
              "Dense Hidden Layer 3: 32 Neurons + ReLU.",
              "Output Layer: 1 Neuron + Sigmoid activation for binary affinity P(Like)."],
             ACCENT_BLUE)

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Optimization & Regularization",
             ["Loss Function: Binary Cross-Entropy.",
              "Optimizer: Adam with learning rate α = 0.001.",
              "Regularization: Dropout & Batch Normalization prevent overfitting.",
              "Convergence: Stabilizes within 25 epochs with loss decreasing to 0.312."],
             ACCENT_CYAN)

    # =========================================================
    # SLIDE 13: TRAINING CURVES & CONVERGENCE
    # =========================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_fitted_image_slide(s13, "ANN Training & Validation Convergence Curves", 
                           "reports/figures/ann_training_curves.png",
                           "Training vs Validation Loss and Accuracy showing smooth convergence without overfitting.")

    # =========================================================
    # SLIDE 14: ROC CURVE & CLASSIFICATION EVALUATION
    # =========================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_fitted_image_slide(s14, "Receiver Operating Characteristic (ROC) Curve", 
                           "reports/figures/roc_ann.png",
                           "ANN Classifier achieves an exceptional Area Under the Curve (AUC = 0.932).")

    # =========================================================
    # SLIDE 15: MODEL COMPARISON
    # =========================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_fitted_image_slide(s15, "Model Performance Comparison", 
                           "reports/figures/model_comparison.png",
                           "Benchmark across Logistic Regression, Random Forest, and Deep Neural Network (ANN).")

    # =========================================================
    # REAL SCREENSHOT SLIDES 16 TO 21 (ACTUAL USER UI SCREENSHOTS)
    # =========================================================
    # 1. Registration Page
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_ui_screenshot_slide(s16, "UI Screen: User Registration & Onboarding",
                            "Movie recomendation system Registration page.png",
                            ["Clean user onboarding interface.",
                             "Alphanumeric username & email validation.",
                             "Cryptographic password hashing (SHA-256/PBKDF2).",
                             "Immediate redirection to login upon creation.",
                             "Prevents duplicate account collisions."])

    # 2. Login Page
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_ui_screenshot_slide(s17, "UI Screen: User Authentication & Login",
                            "movie recomandation system login page after register.png",
                            ["Secure credential authentication view.",
                             "Session token initialization in Streamlit.",
                             "Maintains persistent user state.",
                             "Clear error alerts for invalid credentials.",
                             "Seamless redirect to Movie Explorer."])

    # 3. Dashboard Hero View
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_ui_screenshot_slide(s18, "UI Screen: Movie Explorer Dashboard & Hero",
                            "movierecomendation dashboard 1.1.png",
                            ["High-impact cinematic hero banner.",
                             "Real-time catalog exploration (10,000+ films).",
                             "Dynamic TMDB/OMDb poster image streaming.",
                             "Genre navigation pills for quick filtering.",
                             "Fluid responsive glassmorphism card styling."])

    # 4. Catalog Search & Filter
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_ui_screenshot_slide(s19, "UI Screen: Multi-Attribute Search & Cards",
                            "movierecomandation dashboard 1.2.png",
                            ["Sidebar sliders for release year & score.",
                             "Live text search across titles & overviews.",
                             "Interactive 1-to-5 star rating submission.",
                             "Instant watchlist bookmarking toggles.",
                             "Detailed movie plot synopses tooltip."])

    # 5. Recommendation Results
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20)
    add_ui_screenshot_slide(s20, "UI Screen: Multi-Engine Recommendations",
                            "movie recommendation system recommandation page.png",
                            ["Multi-model toggle: Content, SVD, ANN.",
                             "Top-N ranked movie grid layout.",
                             "Predicted user rating score overlays.",
                             "Detailed similarity explanation badges.",
                             "Sub-15ms real-time inference latency."])

    # 6. Profile & Taste Radar CRUD
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21)
    add_ui_screenshot_slide(s21, "UI Screen: Taste Radar & Rating Management",
                            "movie recomandation profile preview and and crud opration.png",
                            ["Plotly Genre Radar Chart visualization.",
                             "Diagnostic user preference quantification.",
                             "Complete CRUD table for previous ratings.",
                             "Instant star rating update and deletion.",
                             "Active personal watchlist inspection."])

    # =========================================================
    # SLIDE 22: AUTOMATED TESTING & PYTEST VERIFICATION
    # =========================================================
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22)
    add_header(s22, "Testing & Software Quality Assurance")
    
    add_card(s22, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Unit Testing (Pytest)",
             ["83/83 Automated Tests Passing (100%).",
              "Validates Cosine Similarity symmetry.",
              "Validates SVD Latent dimension bounds.",
              "Ensures TF-IDF vocabulary integrity."],
             ACCENT_GREEN)

    add_card(s22, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Integration Testing",
             ["Verifies Streamlit view navigation.",
              "Tests SQLite user authentication & sessions.",
              "Validates rating update transactions.",
              "Checks watchlist persistence."],
             ACCENT_BLUE)

    add_card(s22, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Edge Case & Security",
             ["Tested cold-start empty profile queries.",
              "Handled missing movie poster CDN endpoints.",
              "Protected against SQL injection vulnerabilities.",
              "Safe type casting across rating matrices."],
             ACCENT_GOLD)

    # =========================================================
    # SLIDE 23: CONCLUSION & FUTURE WORK
    # =========================================================
    s23 = prs.slides.add_slide(blank_layout)
    set_slide_background(s23)
    add_header(s23, "Conclusion & Future Enhancements")
    
    add_card(s23, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Conclusion",
             ["Successfully built a production-ready Movie Recommendation System.",
              "Overcame the cold-start and sparsity limitations of traditional recommenders.",
              "Created an academic-grade architecture with complete DFD, ER, and UML modeling.",
              "Delivered an intuitive, interactive streaming-grade web user experience."],
             ACCENT_BLUE)

    add_card(s23, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Future Scope & Roadmap",
             ["Graph Neural Networks: Implement GCNs over knowledge graphs of cinematic franchises.",
              "Real-time Telemetry: Adjust recommendations based on trailer dwell time and clicks.",
              "Cross-Domain Expansion: Extend recommendation engine to TV series, anime, and podcasts."],
             ACCENT_GOLD)

    # =========================================================
    # SLIDE 24: THANK YOU / Q&A
    # =========================================================
    s24 = prs.slides.add_slide(blank_layout)
    set_slide_background(s24)
    
    tb_end = s24.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True
    
    p_end0 = tf_end.paragraphs[0]
    p_end0.alignment = PP_ALIGN.CENTER
    p_end0.text = "THANK YOU!"
    p_end0.font.size = Pt(44)
    p_end0.font.bold = True
    p_end0.font.color.rgb = TEXT_WHITE
    p_end0.space_after = Pt(14)
    
    p_end1 = tf_end.add_paragraph()
    p_end1.alignment = PP_ALIGN.CENTER
    p_end1.text = "Questions & Feedback Welcome\nMovie Recommendation & Discovery System"
    p_end1.font.size = Pt(18)
    p_end1.font.italic = True
    p_end1.font.color.rgb = ACCENT_CYAN

    os.makedirs(os.path.dirname(LOCAL_PPTX), exist_ok=True)
    prs.save(LOCAL_PPTX)
    print(f"Successfully generated PPTX Presentation at:\n- {LOCAL_PPTX}")
    try:
        prs.save(OUTPUT_PPTX)
        print(f"- {OUTPUT_PPTX}")
    except PermissionError:
        fallback = os.path.join(DESKTOP_DIR, "Movie_Recommendation_System_Presentation_Updated.pptx")
        prs.save(fallback)
        print(f"NOTE: Desktop file is currently open in PowerPoint. Saved updated copy to:\n- {fallback}")

if __name__ == '__main__':
    create_presentation()
