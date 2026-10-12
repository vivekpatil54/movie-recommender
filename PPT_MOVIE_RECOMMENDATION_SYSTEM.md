# 🎬 PPT PRESENTATION SLIDES
# **MOVIE RECOMMENDATION SYSTEM (CineMind)**
### **Third Year (TY) Project Defense / Viva Presentation**

---

## 📽️ **SLIDE 1: Title Slide**
* **Project Title:** CineMind – AI-Powered Movie Recommendation System
* **Domain:** Machine Learning, Deep Learning & Web Development
* **Presented by:** TY BCA / B.Sc Computer Science
* **Technologies:** Python, Scikit-Learn, TensorFlow/Keras, Streamlit, Flask, SQLite

---

## 📽️ **SLIDE 2: Problem Statement & Motivation**
* **Problem:** Over 10,000+ titles across modern streaming platforms cause "Choice Paralysis" and information overload.
* **Limitations of Existing Systems:**
  * Static top-10 charts ignore personal taste.
  * Basic genre filters return unranked, overwhelming lists.
  * Opaque "black-box" systems give zero explanations.
* **Our Solution:** A hybrid recommendation engine that learns user taste and predicts likelihood of enjoyment with high accuracy ($>72\%$).

---

## 📽️ **SLIDE 3: System Objectives**
* Develop an end-to-end intelligent movie discovery platform.
* Implement multiple ML/DL recommendation paradigms:
  1. Content-Based (TF-IDF + Cosine Similarity)
  2. Collaborative Filtering (Truncated SVD Matrix Factorization)
  3. Supervised Classifiers (Random Forest & Logistic Regression)
  4. Deep Learning Re-Ranker (Keras 3-Layer ANN)
* Provide interpretable explanations for every recommendation.
* Deliver real-time analytics and exportable PDF Taste Reports.

---

## 📽️ **SLIDE 4: Architecture & Methodology**
* **Dataset:** Benchmark MovieLens dataset ($100,836$ ratings across $9,724$ movies and $610$ users).
* **Feature Engineering:**
  * User rating frequency, mean rating, standard deviation.
  * Movie average rating, popularity count, genre affinity vectors.
* **Pipeline:**
  $$\text{User Interaction} \rightarrow \text{Candidate Generator} \rightarrow \text{Feature Extractor} \rightarrow \text{ANN / SVD Scoring} \rightarrow \text{Top-}N\text{ Ranked Output}$$

---

## 📽️ **SLIDE 5: Machine Learning & Deep Learning Models**
| Algorithm | Technique | Performance / Metric | Key Role |
| :--- | :--- | :--- | :--- |
| **TF-IDF + Cosine** | Content Similarity | 5,000 Vocabulary | Instant genre & tag matching |
| **Truncated SVD** | Collaborative Latent Factors | RMSE: $0.922$, MAE: $0.715$ | Cross-user taste pattern discovery |
| **Random Forest** | 100 Decision Trees Ensemble | Accuracy: $72.26\%$, ROC: $0.7952$ | Non-linear interaction classification |
| **Keras ANN** | 3-Layer Dense (128-64-32) | Accuracy: $72.29\%$, **ROC: $0.8006$** | **Primary re-ranker (Like probability)** |

---

## 📽️ **SLIDE 6: Key Features & User Panel**
* **Dynamic AI Recommendations:** Real-time top-$N$ generation with model switching and genre filters.
* **Ratings & Watchlist Library:** Interactive 0.5★ to 5.0★ rater with status tracking ("Plan to Watch", "Watching", "Completed").
* **Movie Discovery:** Multi-parameter search by title, genre, and release year range.
* **Personalized Taste Report:** Genre radar breakdown, liked percentage, and downloadable 2-page PDF report.

---

## 📽️ **SLIDE 7: System Design & Database (ER & DFD)**
* **Database Schema (SQLite):**
  * `users` table (PBKDF2 password hashing, security questions)
  * `movies` table (Metadata, pipe-separated genres, tags)
  * `ratings` table (User-movie interaction history)
  * `watchlist` table (Custom user queues)
  * `prediction_logs` table (Inference audit logs)
* **Standard Chen Notation:** Primary keys marked with solid underline; Foreign keys marked with dashed underline.

---

## 📽️ **SLIDE 8: Testing & Validation**
* **Pytest Test Suite:** 83 automated test cases passing with 100% success rate.
  * `test_auth.py` (36 tests) – Password hashing, security recovery, auth rules.
  * `test_crud.py` (14 tests) – Movie, rating, and watchlist transactional integrity.
  * `test_models.py` (9 tests) – Prediction probability bounds, SVD & ANN metrics.
  * `test_ui.py` (18 tests) – UI state transitions & view rendering.
  * `test_llm.py` (6 tests) – Status probing & fallback templates.

---

## 📽️ **SLIDE 9: Conclusion & Live Demonstration**
* Successfully deployed hybrid recommendation engine delivering superior discovery and personalization.
* High predictive accuracy ($0.8006$ ROC-AUC) on benchmark real-world data.
* Clean, responsive Streamlit UI backed by robust Flask REST microservices.
* **Live App Demo Link:** Hosted on Streamlit Community Cloud.

---

