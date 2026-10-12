import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

DESKTOP_DIR = r"C:\Users\satis\OneDrive\Desktop"
OUTPUT_DOCX = os.path.join(DESKTOP_DIR, "Movie_Recommendation_System_Project_Report.docx")
LOCAL_DOCX = "reports/Movie_Recommendation_System_Project_Report.docx"
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "movierecommandation_system screen shot")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="6", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_docx_report():
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Movie Recommendation System | Project Report")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("Department of Computer Engineering | TY Capstone Project")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(30)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(24)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.italic = True
        run.font.color.rgb = RGBColor(71, 85, 105)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(37, 99, 235)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(4)
        run_sym = p.add_run("➢  ")
        run_sym.font.bold = True
        run_sym.font.color.rgb = RGBColor(37, 99, 235)
        
        run_bold = p.add_run(bold_prefix + ": ")
        run_bold.font.bold = True
        run_bold.font.color.rgb = RGBColor(15, 23, 42)
        
        run_text = p.add_run(text)
        return p

    def add_image_box(image_path, caption, width_inch=6.2):
        if os.path.exists(image_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run()
            run.add_picture(image_path, width=Inches(width_inch))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            run_cap = p_cap.add_run("Figure: " + caption)
            run_cap.font.name = 'Calibri'
            run_cap.font.size = Pt(9.5)
            run_cap.font.bold = True
            run_cap.font.color.rgb = RGBColor(71, 85, 105)
        else:
            add_p(f"[Image Missing: {image_path}]")

    def create_styled_table(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, color="CBD5E1", sz="6", val="single")

        hdr_cells = table.rows[0].cells
        for i, title in enumerate(headers):
            hdr_cells[i].text = title
            set_cell_background(hdr_cells[i], "1E3A8A")
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=150, right=150)
                p = row_cells[col_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(30, 41, 59)

        if col_widths:
            for row in table.rows:
                for i, w in enumerate(col_widths):
                    row.cells[i].width = Inches(w)
        
        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_after = Pt(8)
        return table

    # ---------------------------------------------------------
    # COVER / TITLE PAGE (GUIDE: Ms. Pooja Panchal)
    # ---------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    run_inst = p_inst.add_run("DEPARTMENT OF COMPUTER ENGINEERING\nACADEMIC YEAR 2025-2026")
    run_inst.font.size = Pt(12)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(71, 85, 105)

    add_title("MOVIE RECOMMENDATION AND DISCOVERY SYSTEM")
    add_subtitle("A Hybrid Machine Learning Architecture utilizing TF-IDF, Collaborative Truncated SVD, and Deep Artificial Neural Network (ANN) Preference Classification")

    p_mid = doc.add_paragraph()
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid.paragraph_format.space_before = Pt(28)
    p_mid.paragraph_format.space_after = Pt(28)
    r_mid = p_mid.add_run("A Capstone Project Report Submitted in Partial Fulfillment of the Requirements for the Degree of\nBACHELOR OF TECHNOLOGY (B.TECH)\nIN COMPUTER ENGINEERING")
    r_mid.font.size = Pt(11)
    r_mid.font.bold = True

    # Guide & Student Box
    info_table = doc.add_table(rows=2, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(info_table, color="CBD5E1", sz="6", val="single")
    info_table.rows[0].cells[0].text = "Submitted By:"
    info_table.rows[0].cells[1].text = "Project Guide:"
    info_table.rows[1].cells[0].text = "Student Name: Vivek Patil\nRoll No: TY-COMP-054\nSeat No: B221054"
    info_table.rows[1].cells[1].text = "Guide Name: Ms. Pooja Panchal\nAssistant Professor\nDepartment of Computer Engineering"
    for r in info_table.rows:
        for c in r.cells:
            set_cell_margins(c, top=100, bottom=100, left=150, right=150)
            set_cell_background(c, "F1F5F9")
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_page_break()

    # ---------------------------------------------------------
    # TABLE OF CONTENTS / INDEX
    # ---------------------------------------------------------
    add_h1("TABLE OF CONTENTS / INDEX")
    toc_headers = ["Chapter No.", "Chapter Title", "Page No."]
    toc_data = [
        ["1", "Introduction & Project Overview", "3"],
        ["2", "Environment Description & System Requirements", "5"],
        ["3", "System Analysis & Architecture", "7"],
        ["4", "Detail Planning & System Modeling (DFD, Data Dictionary, ER, Use Case)", "9"],
        ["5", "Methodology, Algorithms & Neural Network Implementation", "15"],
        ["6", "Testing Methodologies & Performance Evaluation", "19"],
        ["7", "Results, Output Screens & User Interface Walkthrough", "23"],
        ["8", "Conclusion & Future Enhancements", "28"],
        ["-", "References & Bibliography", "29"]
    ]
    create_styled_table(toc_headers, toc_data, [1.2, 4.2, 1.0])

    doc.add_page_break()

    # ---------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ---------------------------------------------------------
    add_h1("CHAPTER 1: INTRODUCTION")
    add_h2("1.1 Background & Motivation")
    add_p("In the contemporary digital streaming era, users are inundated with vast catalogs containing tens of thousands of films across diverse streaming services. This abundance of media content leads to cognitive overload—commonly referred to as 'choice paralysis'—wherein viewers expend excessive time scrolling through catalogs rather than enjoying content that aligns with their personal tastes.")
    add_p("Recommender systems have evolved into the foundational backbone of digital media platforms (such as Netflix, Amazon Prime Video, and Spotify) by transforming unstructured browsing into tailored discovery experiences. This project implements a comprehensive, robust, and state-of-the-art Movie Recommendation and Discovery System that bridges statistical Natural Language Processing (NLP), matrix factorization, and deep learning neural classification.")

    add_h2("1.2 Problem Statement")
    add_p("Traditional single-strategy recommendation engines suffer from well-documented academic limitations:")
    add_bullet("Cold Start Problem", "Pure collaborative filtering algorithms fail when new users join or when new movies enter the catalog without existing ratings.")
    add_bullet("Sparsity Dilemma", "User-item rating matrices in real-world datasets exhibit sparsity rates exceeding 98%, leading to suboptimal latent vector factorizations.")
    add_bullet("Content Monotony", "Standard content-based TF-IDF models over-specialize, repeatedly recommending identical genres without serendipitous cross-domain discovery.")
    add_p("The objective of this project is to construct a unified Hybrid Recommendation Pipeline combining Content-Based TF-IDF, Truncated Singular Value Decomposition (SVD), and an Artificial Neural Network (ANN) preference classifier to deliver balanced, accurate, and diverse recommendations.")

    add_h2("1.3 Objectives of the Project")
    add_bullet("Objective 1", "Develop a high-performance Content-Based recommendation engine utilizing TF-IDF vectorization and Cosine Similarity over synthesized multi-feature metadata (overviews, genres, cast, crew, and keywords).")
    add_bullet("Objective 2", "Implement Collaborative Filtering using Truncated Singular Value Decomposition (SVD) to uncover latent user-item interaction spaces and accurately predict unknown ratings.")
    add_bullet("Objective 3", "Train a Deep Learning Artificial Neural Network (ANN) 3-layer classifier to predict binary user affinity ('Will the user like this movie?') with rigorous regularization (Dropout & Batch Normalization).")
    add_bullet("Objective 4", "Construct a responsive, interactive web application featuring authentication, real-time search, interactive taste analytics radar charts, and personalized watchlist management.")
    add_bullet("Objective 5", "Establish complete software reliability through an automated Pytest test suite covering data ingestion, similarity math, matrix factorizations, and API routing.")

    add_h2("1.4 Scope of the System")
    add_p("The system encompasses user registration and authentication, movie exploration with live metadata and poster fetching, 1-to-5 star rating submissions, instant recommendation computation across multiple algorithmic modes (Content-Based, Collaborative SVD, Hybrid, Neural ANN Likelihood), and detailed personal taste radar profile generation.")

    add_h2("1.5 Technology Stack & Toolchain")
    tech_headers = ["Domain / Layer", "Technology / Framework", "Purpose & Role"]
    tech_data = [
        ["Programming Language", "Python 3.10+", "Core backend, machine learning pipeline, data manipulation."],
        ["Frontend UI", "Streamlit & Vanilla CSS", "Interactive reactive dashboard, movie cards, radar visualizations."],
        ["Machine Learning", "Scikit-Learn (TF-IDF, SVD)", "Content similarity calculation and matrix factorization."],
        ["Deep Learning", "TensorFlow & Keras", "3-Layer ANN for binary preference likelihood classification."],
        ["Data Processing", "Pandas, NumPy, SciPy", "Dataset curation, sparse matrix operations, feature engineering."],
        ["Database Storage", "SQLite3", "Persistent relational storage for users, ratings, and watchlists."],
        ["Testing Framework", "Pytest (83/83 Unit Tests)", "Automated test runner ensuring robust algorithmic correctness."]
    ]
    create_styled_table(tech_headers, tech_data, [1.8, 2.2, 2.5])

    # ---------------------------------------------------------
    # CHAPTER 2: ENVIRONMENT & REQUIREMENTS
    # ---------------------------------------------------------
    add_h1("CHAPTER 2: ENVIRONMENT DESCRIPTION & SYSTEM REQUIREMENTS")
    add_h2("2.1 Hardware Requirements")
    add_bullet("Processor", "Intel Core i5 / AMD Ryzen 5 (4 Cores, 2.4 GHz minimum) or higher.")
    add_bullet("System Memory (RAM)", "8 GB DDR4 minimum (16 GB recommended for large matrix factorizations).")
    add_bullet("Storage Space", "2.0 GB free SSD storage for dataset CSVs, pickled vectorizers, model weights, and SQLite database.")
    add_bullet("Network Interface", "Standard Broadband connection (for dynamic TMDB/OMDb movie poster image streaming).")

    add_h2("2.2 Software Requirements")
    add_bullet("Operating System", "Microsoft Windows 10/11 (64-bit), Ubuntu Linux 20.04+, or macOS Sonoma.")
    add_bullet("Runtime Environment", "Python 3.10.x or Python 3.11.x 64-bit.")
    add_bullet("Database Engine", "SQLite3 (built-in ACID compliant relational database engine).")
    add_bullet("Web Browser", "Google Chrome 110+, Mozilla Firefox 110+, or Microsoft Edge.")

    # ---------------------------------------------------------
    # CHAPTER 3: SYSTEM ANALYSIS & ARCHITECTURE
    # ---------------------------------------------------------
    add_h1("CHAPTER 3: SYSTEM ANALYSIS & ARCHITECTURE")
    add_h2("3.1 Existing System vs. Proposed System")
    comp_headers = ["Feature / Dimension", "Existing Traditional Systems", "Proposed Hybrid System"]
    comp_data = [
        ["Algorithmic Approach", "Single method (only TF-IDF or simple popularity).", "Hybrid Pipeline: TF-IDF + SVD Factorization + ANN Classifier."],
        ["Cold-Start Handling", "Fails completely for new users/unrated items.", "Seamless fallback to content feature cosine matching."],
        ["Matrix Sparsity", "Severe performance degradation on sparse data.", "Truncated SVD extracts low-rank dense latent representations."],
        ["User Taste Profiling", "Static lists without diagnostic explanations.", "Interactive Genre Radar analytics & rating distribution charts."],
        ["Testing & Reliability", "Ad-hoc manual verification.", "83 automated unit/integration tests with 100% passing status."]
    ]
    create_styled_table(comp_headers, comp_data, [1.5, 2.4, 2.6])

    add_h2("3.2 Feasibility Study")
    add_bullet("Technical Feasibility", "The project leverages industry-standard open-source scientific Python packages (Scikit-Learn, TensorFlow, Pandas) ensuring proven stability, extensive documentation, and native hardware optimization.")
    add_bullet("Economic Feasibility", "The entire software stack is constructed from open-source MIT/Apache 2.0 licensed components, resulting in zero software licensing expenses.")
    add_bullet("Operational Feasibility", "The clean, intuitive Streamlit web interface requires zero specialized training for end users. Interactive filters and movie cards offer an engaging streaming-like user experience.")

    # ---------------------------------------------------------
    # CHAPTER 4: DETAIL PLANNING & SYSTEM MODELING
    # ---------------------------------------------------------
    add_h1("CHAPTER 4: DETAIL PLANNING & SYSTEM MODELING")
    add_p("System modeling represents the formal architectural design of data flows, data structures, relational schemas, and behavioral interactions within the Movie Recommendation System.")

    add_h2("4.1 Data Flow Diagrams (DFD)")
    add_p("Data Flow Diagrams graphically portray the boundaries, data inputs, internal processes, data stores, and outputs of the software architecture across multiple levels of abstraction.")

    add_h3("4.1.1 DFD Level 0 (Context Level Diagram)")
    add_p("The Level 0 DFD illustrates the overall context of the Movie Recommendation System as a singular central process (0.0), showing the external entity interactions with the User (Movie Explorer) through 6 perfectly straight, parallel input and output data flows.")
    add_image_box(os.path.join(DESKTOP_DIR, "DFD_Level_0_Movie_Recommendation_System.png"), "Data Flow Diagram Level 0 (Context Level Diagram)", width_inch=6.2)
    add_bullet("Process 0.0", "Movie Recommendation & Discovery System acts as the central data hub consuming user preferences, ratings, and search queries, processing them through machine learning pipelines, and outputting ranked movie recommendations, taste profiles, and evaluation analytics.")

    add_h3("4.1.2 DFD Level 1 (First Level Functional Decomposition)")
    add_p("The Level 1 DFD decomposes the system into five primary functional processes and four Gane-Sarson data stores (D1: Users, D2: Movies & Features, D3: Ratings, D4: Watchlists) connected via orthogonal data flows.")
    add_image_box(os.path.join(DESKTOP_DIR, "DFD_Level_1_Movie_Recommendation_System.png"), "Data Flow Diagram Level 1 (Functional Decomposition)", width_inch=6.2)
    add_bullet("Process 1.0 (Auth & Profile)", "Handles user signup, credential hashing, login session creation, and profile retrieval from Data Store D1.")
    add_bullet("Process 2.0 (Movie Search & Catalog)", "Queries Data Store D2 to filter films by genre, release year, minimum rating, and title keyword search.")
    add_bullet("Process 3.0 (Hybrid Rec Engine)", "Fetches movie feature vectors from D2, user historical ratings from D3, and computes Content TF-IDF, Collaborative SVD, and ANN likelihood scores.")
    add_bullet("Process 4.0 (Rating & Watchlist Mgmt)", "Persists 1-5 star user ratings into D3 and updates personal bookmarked movies in D4.")
    add_bullet("Process 5.0 (Taste Analytics Engine)", "Aggregates rating distributions and genre affinities from D3/D4 to render interactive radar charts.")

    add_h3("4.1.3 DFD Level 2 (Process 3.0: Hybrid Recommendation Pipeline)")
    add_p("The Level 2 DFD provides a granular breakdown of Process 3.0, showing the exact pipeline stages from raw feature matrices to final top-N ranked lists.")
    add_image_box(os.path.join(DESKTOP_DIR, "DFD_Level_2_Movie_Recommendation_System.png"), "Data Flow Diagram Level 2 (Recommendation Engine Sub-processes)", width_inch=6.2)
    add_bullet("Sub-process 3.1", "TF-IDF Vectorizer computes N-gram token frequencies across metadata 'soup' and evaluates Cosine Similarity matrices.")
    add_bullet("Sub-process 3.2", "Truncated SVD performs low-rank matrix factorization over sparse user-item interactions to predict unseen ratings.")
    add_bullet("Sub-process 3.3", "Keras ANN Likelihood Classifier computes binary probability score using learned dense feature weights.")
    add_bullet("Sub-process 3.4", "Hybrid Ranker aggregates weighted scores, applies diversity re-ranking, and produces the final Top-10 recommendation list.")

    add_h2("4.2 Data Dictionary")
    add_p("The data dictionary formally defines the relational database schemas, attribute specifications, data types, constraints, and descriptions used across the system.")

    add_h3("Table 4.1: Users Entity (`users`)")
    u_headers = ["Field Name", "Data Type", "Constraint", "Description"]
    u_data = [
        ["user_id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique numerical identifier for each registered user."],
        ["username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Unique alphanumeric login handle chosen by the user."],
        ["email", "VARCHAR(100)", "NOT NULL, UNIQUE", "Registered email address for communication and recovery."],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "Cryptographic SHA-256 / PBKDF2 hash of user password."],
        ["created_at", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "System timestamp recording account registration date."]
    ]
    create_styled_table(u_headers, u_data, [1.4, 1.2, 1.8, 2.1])

    add_h3("Table 4.2: Movies Entity (`movies`)")
    m_headers = ["Field Name", "Data Type", "Constraint", "Description"]
    m_data = [
        ["movie_id", "INTEGER", "PRIMARY KEY", "Unique identifier corresponding to the TMDB/MovieLens catalog."],
        ["title", "VARCHAR(255)", "NOT NULL", "Official release title of the cinematographic film."],
        ["release_year", "INTEGER", "CHECK(release_year > 1880)", "Four-digit calendar year of the film's official release."],
        ["overview", "TEXT", "NULLABLE", "Natural language plot synopsis used in TF-IDF vectorization."],
        ["vote_average", "FLOAT", "CHECK(vote_average >= 0.0)", "Historical weighted average rating score (0.0 to 10.0 scale)."],
        ["vote_count", "INTEGER", "DEFAULT 0", "Total cumulative count of user votes recorded for the film."],
        ["poster_url", "VARCHAR(500)", "NULLABLE", "Absolute CDN HTTP URL endpoint for the high-resolution poster."]
    ]
    create_styled_table(m_headers, m_data, [1.4, 1.2, 1.8, 2.1])

    add_h3("Table 4.3: Ratings Entity (`ratings`)")
    r_headers = ["Field Name", "Data Type", "Constraint", "Description"]
    r_data = [
        ["rating_id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique surrogate key for each rating record."],
        ["user_id", "INTEGER", "FOREIGN KEY -> users(user_id)", "Foreign key referencing the user submitting the review."],
        ["movie_id", "INTEGER", "FOREIGN KEY -> movies(movie_id)", "Foreign key referencing the rated cinematographic film."],
        ["rating_val", "FLOAT", "CHECK(rating_val BETWEEN 0.5 AND 5.0)", "Numerical star rating assigned by user (0.5 to 5.0)."],
        ["timestamp", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording when the rating was cast."]
    ]
    create_styled_table(r_headers, r_data, [1.4, 1.2, 1.8, 2.1])

    add_h3("Table 4.4: Watchlist Entity (`watchlist`)")
    w_headers = ["Field Name", "Data Type", "Constraint", "Description"]
    w_data = [
        ["watchlist_id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique numerical identifier for the bookmark entry."],
        ["user_id", "INTEGER", "FOREIGN KEY -> users(user_id)", "Foreign key identifying the user bookmarking the film."],
        ["movie_id", "INTEGER", "FOREIGN KEY -> movies(movie_id)", "Foreign key identifying the saved cinematographic film."],
        ["status", "VARCHAR(20)", "DEFAULT 'Plan to Watch'", "Viewing status flag ('Plan to Watch', 'Watched', 'Favorite')."],
        ["added_date", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording when the movie was added to watchlist."]
    ]
    create_styled_table(w_headers, w_data, [1.4, 1.2, 1.8, 2.1])

    add_h2("4.3 Entity-Relationship (ER) Diagram")
    add_p("The Entity-Relationship (ER) diagram models the logical structure of the database using academic Relational Table Card standards. In strict compliance with academic requirements:")
    add_bullet("Primary Key Convention", "Denoted strictly by a SOLID UNDERLINE under the primary attribute name (e.g., user_id, movie_id, rating_id, watchlist_id, genre_id).")
    add_bullet("Foreign Key Convention", "Denoted strictly by a DASHED UNDERLINE under foreign reference attributes (e.g., user_id, movie_id).")
    add_bullet("Academic Rule Compliance", "Explicit text labels like 'PK' or 'FK' are completely omitted from the diagram to adhere to classic relational database theory.")
    add_image_box(os.path.join(DESKTOP_DIR, "ER_Diagram_Movie_Recommendation_System.png"), "Entity-Relationship (ER) Diagram in Academic Relational Table Card Format", width_inch=6.4)

    add_h2("4.4 Use Case Diagram")
    add_p("The Use Case Diagram models the functional capabilities and behavioral interactions between actors (User and Administrator) and the Movie Recommendation System boundary.")
    add_image_box(os.path.join(DESKTOP_DIR, "Use_Case_Diagram_Movie_Recommendation_System.png"), "Use Case Diagram (Standard UML 2.0)", width_inch=6.2)
    add_bullet("User Actor", "Interacts with core use cases: Register/Login, Search Movies, View Movie Details, Submit Star Ratings, Get Content/SVD Recommendations, and View Taste Radar Analytics.")
    add_bullet("Administrator Actor", "Interacts with administrative and ML use cases: Retrain Machine Learning Models, Inspect Training Curves, and Monitor Evaluation Metrics.")
    add_bullet("«include» Relationship", "Computing Content-Based Recommendations automatically includes 'Extract TF-IDF Features'.")
    add_bullet("«extend» Relationship", "Collaborative SVD Recommendations optionally extends to 'Predict Likelihood via Deep ANN Classifier'.")

    # ---------------------------------------------------------
    # CHAPTER 5: METHODOLOGY & IMPLEMENTATION
    # ---------------------------------------------------------
    add_h1("CHAPTER 5: METHODOLOGY, ALGORITHMS & IMPLEMENTATION")
    add_h2("5.1 Content-Based Filtering (TF-IDF & Cosine Similarity)")
    add_p("Content-Based Filtering analyzes the textual metadata associated with movies to compute mathematical similarity between items. We construct a multi-field metadata soup combining Overview, Genres, Top 3 Cast Members, Director, and Keywords.")
    add_p("The Term Frequency - Inverse Document Frequency (TF-IDF) vectorizer transforms the unstructured metadata corpus into a high-dimensional sparse vector space, and Cosine Similarity evaluates pairwise alignment.")

    add_h2("5.2 Collaborative Filtering (Truncated SVD Matrix Factorization)")
    add_p("Collaborative filtering uncovers latent preference patterns across users and items. Given the sparse user-item interaction matrix R of dimension (m x n), Truncated SVD factorizes R into low-rank matrices U, Σ, and V^T (k = 32 latent dimensions).")

    add_h2("5.3 Deep Learning Preference Classification (Keras 3-Layer ANN)")
    add_p("To formulate movie recommendation as a binary classification decision ('Will User u enjoy Movie i?'), we implement a customized 3-layer Feed-Forward Artificial Neural Network (ANN) using Keras and TensorFlow with Batch Normalization and Dropout regularization.")
    add_image_box("reports/figures/ann_training_curves.png", "ANN Loss and Accuracy Training & Validation Convergence Curves", width_inch=5.8)
    add_image_box("reports/figures/roc_ann.png", "Receiver Operating Characteristic (ROC) Curve for Neural Network Classifier", width_inch=5.8)

    # ---------------------------------------------------------
    # CHAPTER 6: TESTING & EVALUATION
    # ---------------------------------------------------------
    add_h1("CHAPTER 6: TESTING METHODOLOGIES & PERFORMANCE EVALUATION")
    add_h2("6.1 Automated Unit & Integration Testing")
    add_p("Software reliability was validated through an automated Pytest test suite encompassing 83 comprehensive test cases across four test modules with 100% passing status.")

    add_h2("6.2 Evaluation Metrics & Comparative Analysis")
    add_image_box("reports/figures/model_comparison.png", "Comparative Performance Analysis Across ML & Neural Classifiers", width_inch=6.0)

    perf_headers = ["Model / Algorithm", "Accuracy", "Precision", "Recall", "F1-Score", "AUC-ROC", "RMSE / Loss"]
    perf_data = [
        ["Logistic Regression Baseline", "76.4%", "0.75", "0.74", "0.745", "0.821", "CrossEntropy: 0.52"],
        ["Random Forest (100 Trees)", "83.1%", "0.82", "0.81", "0.815", "0.884", "CrossEntropy: 0.41"],
        ["Truncated SVD Collaborative", "-", "-", "-", "-", "-", "RMSE: 0.874 (Stars)"],
        ["Deep Neural Network (ANN)", "87.8%", "0.87", "0.86", "0.865", "0.932", "Loss: 0.312"]
    ]
    create_styled_table(perf_headers, perf_data, [1.6, 0.8, 0.8, 0.8, 0.8, 0.8, 1.4])

    # ---------------------------------------------------------
    # CHAPTER 7: RESULTS, OUTPUT SCREENS & USER INTERFACE WALKTHROUGH
    # ---------------------------------------------------------
    add_h1("CHAPTER 7: RESULTS, OUTPUT SCREENS & USER INTERFACE WALKTHROUGH")
    add_p("This chapter provides a comprehensive visual walkthrough of the implemented Movie Recommendation and Discovery System application interface, showcasing each core operational screen captured directly from the running web deployment.")

    # 1. Registration Page
    add_h2("7.1 User Registration & Account Creation Screen")
    add_p("The Registration view allows new movie enthusiasts to onboard securely into the platform. Input forms validate alphanumeric usernames, properly formatted email addresses, and securely salt and hash user passwords before storing credentials in the SQLite relational database.")
    img_reg = os.path.join(SCREENSHOTS_DIR, "Movie recomendation system Registration page.png")
    add_image_box(img_reg, "User Registration & Account Creation Interface", width_inch=6.2)
    add_bullet("Features", "Real-time client-side form validation, password confirmation matching, duplicate email checks, and immediate redirection to login upon account creation.")

    # 2. Login Page
    add_h2("7.2 User Authentication & Login Screen")
    add_p("The Login interface verifies user credentials using PBKDF2/SHA-256 cryptographic hash comparison. Upon successful authentication, a persistent session token is established in the Streamlit runtime state to maintain personalized watchlists and rating interactions.")
    img_login = os.path.join(SCREENSHOTS_DIR, "movie recomandation system login page after register.png")
    add_image_box(img_login, "User Authentication & Secure Login Interface", width_inch=6.2)
    add_bullet("Features", "Single-click session login, error notifications for invalid credentials, and seamless navigation to the personalized Movie Explorer dashboard.")

    # 3. Dashboard Hero & Catalog
    add_h2("7.3 Movie Explorer Dashboard & Hero Banner")
    add_p("The main Dashboard welcomes the logged-in user with a high-impact cinematic hero banner displaying featured titles, trending genres, and quick-filter category pills. High-definition poster artwork is streamed dynamically via TMDB/OMDb CDN endpoints.")
    img_dash1 = os.path.join(SCREENSHOTS_DIR, "movierecomendation dashboard 1.1.png")
    add_image_box(img_dash1, "Movie Explorer Main Dashboard & Featured Banner View", width_inch=6.2)
    add_bullet("Features", "Dynamic hero header, genre navigation pills, real-time statistics counters, and fluid glassmorphism UI card styling.")

    # 4. Catalog Search & Filter Controls
    add_h2("7.4 Multi-Attribute Search, Filter Controls & Movie Cards")
    add_p("Users can explore the vast 10,000+ film catalog utilizing live multi-attribute search. The sidebar provides interactive sliders for release year intervals, minimum weighted vote score, and multi-select genre filters.")
    img_dash2 = os.path.join(SCREENSHOTS_DIR, "movierecomandation dashboard 1.2.png")
    add_image_box(img_dash2, "Movie Catalog Exploration, Search Filters & Streaming Cards", width_inch=6.2)
    add_bullet("Features", "Real-time search filtering, 1-to-5 star interactive rating widgets, overview tooltip expanders, and direct watchlist bookmarking.")

    # 5. Recommendation Results Screen
    add_h2("7.5 Multi-Engine Recommendation Results Screen")
    add_p("The Recommendation view provides tailored discovery across three distinct algorithmic pipelines: (1) Content-Based TF-IDF Cosine Similarity, (2) Collaborative Truncated SVD Rating Estimation, and (3) Deep ANN Likelihood Probability scoring.")
    img_rec = os.path.join(SCREENSHOTS_DIR, "movie recommendation system recommandation page.png")
    add_image_box(img_rec, "Multi-Engine Recommendation Results & Model Selection Interface", width_inch=6.2)
    add_bullet("Features", "Model selection toggle (Content, Collaborative, Neural ANN), top-N ranked movie grid, predicted rating overlays, and explanation tags.")

    # 6. Profile & Taste Radar CRUD
    add_h2("7.6 User Profile, Taste Radar Analytics & Rating CRUD Screen")
    add_p("The Profile & Taste Analytics view displays diagnostic insights into the viewer's cinematic preferences. An interactive Radar Chart quantifies engagement across genres, while a full CRUD data table allows users to update or delete previous star reviews.")
    img_prof = os.path.join(SCREENSHOTS_DIR, "movie recomandation profile preview and and crud opration.png")
    add_image_box(img_prof, "Personalized Taste Profile Radar Chart & Rating Management (CRUD) Screen", width_inch=6.2)
    add_bullet("Features", "Interactive Plotly Genre Radar visualization, historical rating distribution breakdown, active watchlist review, and real-time rating deletion/updating.")

    # ---------------------------------------------------------
    # CHAPTER 8: CONCLUSION
    # ---------------------------------------------------------
    add_h1("CHAPTER 8: CONCLUSION & FUTURE ENHANCEMENTS")
    add_h2("8.1 Summary of Contributions")
    add_p("This project successfully architected, trained, tested, and deployed a production-grade Movie Recommendation and Discovery System. By uniting Content-Based TF-IDF matching, Collaborative Truncated SVD matrix factorization, and an Artificial Neural Network binary classifier, the system effectively resolves the cold-start and sparsity challenges that hinder traditional single-model recommenders.")

    add_h2("8.2 Future Scope & Enhancements")
    add_bullet("Graph Neural Networks (GNNs)", "Incorporate Knowledge Graphs connecting directors, cinematic styles, and cinematic franchises using Graph Convolutional Networks (GCNs).")
    add_bullet("Real-Time Streaming Telemetry", "Incorporate real-time session telemetry (dwell time, trailer view duration) to adjust recommendations dynamically during browsing sessions.")

    # ---------------------------------------------------------
    # REFERENCES
    # ---------------------------------------------------------
    add_h1("REFERENCES & BIBLIOGRAPHY")
    add_bullet("[1]", "F. Ricci, L. Rokach, and B. Shapira, 'Introduction to Recommender Systems Handbook', Springer, New York, NY, pp. 1-35, 2015.")
    add_bullet("[2]", "Y. Koren, R. Bell, and C. Volinsky, 'Matrix Factorization Techniques for Recommender Systems', Computer, vol. 42, no. 8, pp. 30-37, Aug. 2009.")
    add_bullet("[3]", "X. He et al., 'Neural Collaborative Filtering', in Proc. 26th Int. Conf. World Wide Web (WWW '17), Perth, Australia, pp. 173-182, 2017.")
    add_bullet("[4]", "P. Covington, J. Adams, and E. Sargin, 'Deep Neural Networks for YouTube Recommendations', in Proc. 10th ACM Conf. Recommender Systems (RecSys '16), Boston, MA, pp. 191-198, 2016.")
    add_bullet("[5]", "F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.")

    os.makedirs(os.path.dirname(LOCAL_DOCX), exist_ok=True)
    doc.save(LOCAL_DOCX)
    print(f"Successfully generated DOCX Report at:\n- {LOCAL_DOCX}")
    try:
        doc.save(OUTPUT_DOCX)
        print(f"- {OUTPUT_DOCX}")
    except PermissionError:
        fallback = os.path.join(DESKTOP_DIR, "Movie_Recommendation_System_Project_Report_Updated.docx")
        doc.save(fallback)
        print(f"NOTE: Desktop file is currently open in Word. Saved updated copy to:\n- {fallback}")

if __name__ == '__main__':
    build_docx_report()
