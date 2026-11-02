from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
HTML_OUT = REPORT_DIR / "CGTH_Project_Report_bn.html"


def table(headers: list[str], rows: list[list[str]], cls: str = "") -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def build_html() -> str:
    results = table(
        ["মডেল", "Balanced accuracy (95% CI)", "Accuracy", "Sensitivity", "Specificity", "ROC-AUC", "LR coverage"],
        [
            ["Logistic Regression", "0.730 [0.667, 0.794]", "0.745", "0.821", "0.639", "0.800", "100%"],
            ["Random Forest", "0.761 [0.706, 0.816]", "0.780", "0.881", "0.642", "0.835", "0%"],
            ["Soft Voting (LR+RF)", "0.741 [0.678, 0.804]", "0.760", "0.857", "0.626", "0.820", "—"],
            ["<b>CGTH (প্রস্তাবিত)</b>", "<b>0.757 [0.700, 0.813]</b>", "0.776", "0.878", "0.635", "0.809", "<b>68%</b>"],
        ],
    )
    lit = table(
        ["ধারা", "সাহিত্যে সাধারণ চিত্র", "এই প্রকল্পের প্রতিক্রিয়া"],
        [
            ["ডেটা", "EHR-ভিত্তিক বড় cohort অথবা ছোট single-site questionnaire; provenance ও duplication audit সবসময় থাকে না।", "Raw data অপরিবর্তিত রেখে duplicate, missing cell, timestamp ও label plausibility audit করা হয়েছে।"],
            ["Label", "EPDS/PHQ স্কোর, diagnosis code বা symptom label—ফলাফল একরকম নয়।", "এখানে `Feeling anxious` self-reported item; clinical diagnosis হিসেবে দাবি করা হয়নি।"],
            ["Validation", "Single split বা internal CV বেশি; optimistic point estimate-এর ঝুঁকি থাকে।", "Stratified 5-fold × 10 repeat = 50 paired folds এবং corrected CI ব্যবহার করা হয়েছে।"],
            ["Ensemble", "Voting/stacking সাধারণত সব case-এ একসঙ্গে ব্যবহার হয়।", "Transparent-first gate: confident case LR নেয়, uncertain case RF-তে যায়।"],
            ["Explainability", "SHAP/feature plot দেখানো হয়, কিন্তু কত case simple model decide করেছে তা মাপা হয় না।", "LR coverage এবং transparency–performance curve রিপোর্ট করা হয়েছে।"],
        ],
    )
    age = table(
        ["Age band", "Unique rows", "Balanced accuracy", "Sensitivity", "Specificity", "LR coverage"],
        [
            ["25–30", "49", "0.664", "0.748", "0.581", "0.624"],
            ["30–35", "71", "0.824", "0.967", "0.681", "0.601"],
            ["35–40", "76", "0.760", "0.826", "0.693", "0.774"],
            ["40–45", "73", "0.755", "0.878", "0.633", "0.656"],
            ["45–50", "57", "0.726", "0.927", "0.525", "0.756"],
        ],
    )
    refs = """
    <ol class="refs">
      <li>Zhang et al. (2020), <i>JMIR Medical Informatics</i>, 8(4):e15516.</li>
      <li>Shin, Lee, Adeluwa &amp; Hur (2020), <i>Journal of Clinical Medicine</i>, 9(9):2899.</li>
      <li>Hochman et al. (2021), <i>Depression and Anxiety</i>, 38(4):400–411.</li>
      <li>Amit et al. (2021), <i>BMC Pregnancy and Childbirth</i>, 21:630.</li>
      <li>Saqib, Khan &amp; Butt (2021), <i>JMIR Mental Health</i>, 8(11):e29838.</li>
      <li>Cellini et al. (2022), <i>Journal of Affective Disorders</i>, 309.</li>
      <li>Collins et al. (2024), TRIPOD+AI, <i>BMJ</i>, 385:e078378.</li>
      <li>Huang et al. (2025), <i>Frontiers in Medicine</i>, doi:10.3389/fmed.2025.1565374.</li>
      <li>Xia et al. (2025), <i>Frontiers in Public Health</i>, doi:10.3389/fpubh.2025.1631705.</li>
      <li>Alkhateeb et al. (2026), <i>Journal of Medical Internet Research</i>, 28:e77376.</li>
      <li>Lundberg &amp; Lee (2017), SHAP; Ribeiro et al. (2016), LIME; Nadeau &amp; Bengio (2003), corrected resampling.</li>
    </ol>
    """
    return f"""<!doctype html>
<html lang="bn">
<head>
<meta charset="utf-8">
<style>
@page {{ size: A4; margin: 18mm 17mm 18mm 17mm; @bottom-center {{ content: "CGTH Project Report  |  " counter(page); font-size: 9pt; color: #64748b; }} }}
@font-face {{ font-family: Hind; src: url("file:///Users/abdurrahman/Library/Fonts/HindSiliguri-Regular.ttf"); font-weight: 400; }}
@font-face {{ font-family: Hind; src: url("file:///Users/abdurrahman/Library/Fonts/HindSiliguri-SemiBold.ttf"); font-weight: 600; }}
@font-face {{ font-family: Hind; src: url("file:///Users/abdurrahman/Library/Fonts/HindSiliguri-Bold.ttf"); font-weight: 700; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Hind, sans-serif; color: #1e293b; font-size: 11pt; line-height: 1.55; }}
h1, h2, h3 {{ color: #0f3d56; line-height: 1.25; }}
h1 {{ font-size: 25pt; margin-top: 0; }}
h2 {{ font-size: 17pt; border-bottom: 2px solid #2d8ca8; padding-bottom: 4px; margin-top: 24px; }}
h3 {{ font-size: 13pt; margin-bottom: 3px; }}
p {{ text-align: justify; margin: 7px 0; }}
.cover {{ min-height: 235mm; display: flex; flex-direction: column; justify-content: center; text-align: center; page-break-after: always; }}
.cover h1 {{ font-size: 29pt; }}
.subtitle {{ font-size: 16pt; color: #2d8ca8; }}
.meta {{ margin-top: 30mm; color: #475569; font-size: 12pt; }}
.callout {{ background: #eef7fa; border-left: 5px solid #2d8ca8; padding: 10px 14px; margin: 12px 0; }}
.warning {{ background: #fff7ed; border-left-color: #ea580c; }}
.good {{ background: #f0fdf4; border-left-color: #16a34a; }}
.pagebreak {{ page-break-before: always; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0 15px; font-size: 9pt; }}
th {{ background: #0f3d56; color: white; font-weight: 600; }}
th, td {{ border: 1px solid #cbd5e1; padding: 5px 6px; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f8fafc; }}
ul, ol {{ margin-top: 4px; }}
li {{ margin: 3px 0; }}
pre {{ background: #f1f5f9; border: 1px solid #cbd5e1; padding: 10px; font-family: monospace; font-size: 8.5pt; white-space: pre-wrap; }}
.figure {{ text-align: center; margin: 12px 0; }}
.figure img {{ max-width: 100%; max-height: 105mm; }}
.caption {{ color: #475569; font-size: 9pt; }}
.small {{ font-size: 9pt; color: #475569; }}
.refs {{ font-size: 9pt; }}
.toc li {{ margin: 2px; }}
</style>
</head>
<body>
<section class="cover">
  <div class="subtitle">Complete Research Project Report / পূর্ণাঙ্গ গবেষণা প্রতিবেদন</div>
  <h1>Interpretable Postpartum Anxiety Screening-এর জন্য<br>Confidence-Gated Transparent Hybrid Machine Learning</h1>
  <p class="subtitle">CGTH Project Report — English + বাংলা Mixed Edition (Updated)</p>
  <div class="meta">
    <p><b>Core project idea / মূল ধারণা:</b> Logistic Regression-এর explainability এবং Random Forest-এর predictive strength-কে একটি confidence gate-এর মাধ্যমে combine করা।</p>
    <p>প্রধান notebook: <code>notebooks/01_cgth_hybrid_study.ipynb</code><br>
    রিপোর্টের তারিখ: ২ নভেম্বর ২০২৬</p>
  </div>
</section>

<h2>Executive Summary / সারসংক্ষেপ</h2>
<p>এই প্রকল্পে postpartum survey data ব্যবহার করে একজন respondent-এর self-reported anxiety item অনুমান করার জন্য একটি ব্যাখ্যাযোগ্য hybrid machine-learning পদ্ধতি তৈরি ও মূল্যায়ন করা হয়েছে। প্রস্তাবিত <b>Confidence-Gated Transparent Hybrid (CGTH)</b>-এ Logistic Regression (LR) যখন নিজের prediction সম্পর্কে confident, তখন সে-ই final decision দেয়; probability 0.5-এর কাছাকাছি হলে কেবল সেই uncertain case Random Forest (RF)-এ পাঠানো হয়।</p>
<div class="callout good"><b>মূল ফলাফল:</b> duplicate সরানোর পর ৫০টি paired validation fold-এ CGTH balanced accuracy 0.757 [0.700, 0.813], RF-এর 0.761-এর খুব কাছাকাছি, অথচ ৬৮% decision সরাসরি transparent LR করেছে। তবে stricter, fold-wise threshold selection-এ RF-এর non-inferiority statisticalভাবে প্রতিষ্ঠিত হয়নি (p = 0.06); তাই ফলাফল promising, definitive নয়।</div>
<p>সবচেয়ে গুরুত্বপূর্ণ শিক্ষা হলো model score-এর চেয়ে data quality বেশি decisive: raw dataset-এর ৭৮% row duplicate/replicated pattern, label একটি clinical diagnosis নয়, এবং guilt item বাদ দিলে balanced accuracy প্রায় 0.60-এ নেমে যায়। তাই এই report-এ সাফল্যের সঙ্গে সীমাবদ্ধতা ও বাকি কাজও সমানভাবে বলা হয়েছে।</p>

<h2>Table of Contents / সূচিপত্র</h2>
<ol class="toc">
  <li>প্রকল্পের পটভূমি ও সমস্যা</li><li>উদ্দেশ্য, research questions ও hypotheses</li>
  <li>Literature review ও research gap</li><li>Dataset, audit ও ethics</li>
  <li>Methodology ও architecture</li><li>Evaluation ও statistical design</li>
  <li>ফলাফল ও বিশ্লেষণ</li><li>Explainability, robustness ও fairness</li>
  <li>Contribution, limitation ও clinical meaning</li><li>উপসংহার ও ভবিষ্যৎ roadmap</li>
</ol>

<h2>১. Project Background and Problem / প্রকল্পের পটভূমি ও সমস্যা</h2>
<p>Postpartum period-এ উদ্বেগ ও বিষণ্ণতার উপসর্গ দ্রুত শনাক্ত করা গুরুত্বপূর্ণ। Machine learning questionnaire-এর বহু উত্তর থেকে risk signal ধরতে পারে, কিন্তু mental-health context-এ শুধু accuracy যথেষ্ট নয়। একজন clinician বা researcher-কে জানতে হয় কেন একটি decision এসেছে, কোন feature তার সঙ্গে সম্পর্কিত, এবং কোন ক্ষেত্রে model অনিশ্চিত।</p>
<p>এখানে মৌলিক trade-off হলো: LR সহজে odds ratio দিয়ে ব্যাখ্যা করা যায়, কিন্তু non-linear interaction ধরতে সীমিত; RF interaction ধরতে পারে, কিন্তু individual decision বোঝানো কঠিন। প্রচলিত soft voting সব case-এ দুই model-এর probability blend করে, ফলে কোনো decision-ই পুরোপুরি simple model-এর decision থাকে না। CGTH এই সমস্যায় “transparent first, complex only when needed” নীতি প্রয়োগ করে।</p>

<h2>২. Objectives, Research Questions and Hypotheses / উদ্দেশ্য ও গবেষণা প্রশ্ন</h2>
<ol>
  <li>Dataset-এর duplicate, missing value, timestamp ও label plausibility audit করা।</li>
  <li>LR ও RF দিয়ে CGTH তৈরি করা।</li>
  <li>Leakage-free repeated validation-এ LR, RF, soft voting ও CGTH তুলনা করা।</li>
  <li>কত শতাংশ decision transparent LR করছে—coverage—তা মাপা।</li>
  <li>LR decision odds ratio দিয়ে ব্যাখ্যা করা এবং transparency–performance curve তৈরি করা।</li>
  <li>Duplicate leakage ও dominant guilt item-এর ওপর robustness পরীক্ষা করা।</li>
</ol>
<div class="callout"><b>H1:</b> CGTH RF-এর চেয়ে balanced accuracy-তে 0.03 margin-এর মধ্যে non-inferior হবে।<br>
<b>H2:</b> CGTH LR-এর চেয়ে superior হবে। Primary metric balanced accuracy; ROC-AUC secondary।</div>

<h2>৩. Literature Review and Research Gaps / সাহিত্য পর্যালোচনা ও research gap</h2>
<p>পর্যালোচিত literature-এ তিনটি ধারা দেখা যায়। বড় EHR cohort-এ sample বড় হলেও documented diagnosis এবং symptom screening এক নয়। ছোট questionnaire study-তে AUC বেশি দেখা যায়, কিন্তু single-site data, small-n optimism এবং internal-only validation-এর ঝুঁকি থাকে। Review papers validation inconsistency, variable selection এবং reporting bias-এর কথা বলেছে।</p>
{lit}
<h3>Specific Gaps Addressed by This Project / এই প্রকল্পে address করা gap</h3>
<table>
<thead><tr><th>Gap</th><th>সমস্যা</th><th>এই প্রকল্পে উত্তর</th></tr></thead>
<tbody>
<tr><td>G1</td><td>Public survey data-তে duplicate/replication audit অনিয়মিত।</td><td>১,৫০৩ raw row থেকে unique pattern, missingness ও label anomaly পরিমাপ।</td></tr>
<tr><td>G2</td><td>Single split-এর point estimate optimistic হতে পারে।</td><td>৫০টি paired fold, corrected CI এবং hypothesis test।</td></tr>
<tr><td>G3</td><td>Hybrid সাধারণত সব case-এ blend করে।</td><td>Confident case LR; uncertain case RF।</td></tr>
<tr><td>G4</td><td>Explainability plot আছে, কিন্তু transparent decision coverage নেই।</td><td>৬৮% LR coverage ও delta curve রিপোর্ট।</td></tr>
<tr><td>G5</td><td>Ensemble superiority প্রায়ই ধরে নেওয়া হয়।</td><td>Pre-stated non-inferiority বনাম RF এবং superiority বনাম LR test।</td></tr>
<tr><td>G6</td><td>একটি dominant item headline result চালাতে পারে।</td><td>Guilt item বাদ দিয়ে পূর্ণ experiment পুনরায় চালানো।</td></tr>
</tbody></table>
<p class="small"><b>Novelty সততার সঙ্গে:</b> confidence-based cascade বা selective classification নতুন ধারণা নয়। এই কাজের অবদান হলো postpartum survey setting-এ transparent-first cascade প্রয়োগ, coverage-কে performance-এর পাশে report করা এবং data-quality failure-কে ফলাফলের অংশ করা।</p>

<h2>৪. Dataset, Data Audit and Ethics / ডেটাসেট, audit ও নৈতিকতা</h2>
<p>Source হলো Kaggle-এর <i>PostPartum Depression</i> dataset; uploader: <code>parvezalmuqtadir2348</code>। Raw file-এ ১,৫০৩ row ও ১১ column: timestamp, age band এবং ৯টি categorical survey item। Target হিসেবে <code>Feeling anxious</code>-এর Yes/No নেওয়া হয়েছে। Raw data কখনও overwrite করা হয়নি; preprocessing notebook-এর pipeline-এর ভিতরে হয়েছে।</p>
<table>
<thead><tr><th>Audit item</th><th>ফলাফল</th><th>অর্থ</th></tr></thead>
<tbody>
<tr><td>Raw rows</td><td>1,503</td><td>প্রথমে দেখা sample size; model-এর effective independent sample নয়।</td></tr>
<tr><td>Unique answer patterns</td><td>326</td><td>প্রায় ৭৮% duplicate/replicated row; leakage-এর বড় ঝুঁকি।</td></tr>
<tr><td>Missing cells</td><td>27</td><td>Most-frequent imputation training fold-এর ভিতরে fit করা হয়েছে।</td></tr>
<tr><td>Distinct timestamps</td><td>90</td><td>একই সময়/response pattern replication-এর সম্ভাবনা।</td></tr>
<tr><td>Label</td><td>Self-reported anxiety item</td><td>Validated clinical diagnosis নয়।</td></tr>
</tbody></table>
<div class="callout warning"><b>Ethics ও safe use:</b> dataset-এ mental-health item এবং suicide-related question আছে। এটি individual clinical diagnosis, triage বা treatment recommendation-এর জন্য নয়। Kaggle licence ও provenance redistributing-এর আগে যাচাই করতে হবে; anonymisation এবং secure storage বজায় রাখতে হবে।</div>

<h2>৫. Methodology: From Preprocessing to Final Decision / preprocessing থেকে final decision</h2>
<ol>
  <li>Timestamp drop করা হয়েছে, কারণ এটি clinical predictor নয় এবং collection order-এর proxy হতে পারে।</li>
  <li>Exact duplicate row split-এর আগেই বাদ দেওয়া হয়েছে, যাতে একই response train ও validation-এ না থাকে।</li>
  <li>Missing categorical value-এর most-frequent imputation এবং one-hot encoding কেবল training fold-এ fit করা হয়েছে; validation fold-এ তথ্য leak হয়নি।</li>
  <li>LR ও RF একই fold, একই threshold এবং একই transformed features পেয়েছে।</li>
  <li>LR probability <i>p</i>-এর জন্য delta = 0.2: |p − 0.5| ≥ 0.2 হলে LR final decision; নইলে RF decision।</li>
</ol>
<pre>respondent answers
        │
fold-specific imputation + one-hot encoding
        │
Logistic Regression → probability p
        │
    |p − 0.5| ≥ δ ?
       ┌───────┴────────┐
     হ্যাঁ              না
       │                 │
 final = LR          final = RF
 explainable         uncertain case only</pre>
<h3>Why These Two Models? / কেন এই দুই model?</h3>
<table>
<thead><tr><th>Model</th><th>ভূমিকা</th><th>কেন ব্যবহার</th></tr></thead>
<tbody>
<tr><td>Logistic Regression</td><td>Transparent base</td><td>Odds ratio, low variance, categorical survey data-তে readable association।</td></tr>
<tr><td>Random Forest</td><td>Stronger nonlinear base</td><td>Feature interaction ধরতে পারে; এই data-তে single-model benchmark-এর সেরা ফল।</td></tr>
<tr><td>Soft voting</td><td>Comparator hybrid</td><td>প্রচলিত probability averaging-এর fair baseline।</td></tr>
<tr><td>CGTH</td><td>Proposed method</td><td>Simple model confident হলে complexity না বাড়িয়ে decision; uncertain হলে RF-এর সাহায্য।</td></tr>
</tbody></table>

<h2>৬. Evaluation and Statistical Design / evaluation ও statistical design</h2>
<p>Dataset ছোট হওয়ায় আলাদা 66-row hold-out অত্যন্ত noisy হতে পারে। তাই stratified 5-fold cross-validation 10 বার repeat করে মোট ৫০টি paired fold ব্যবহার করা হয়েছে। সব model একই folds ব্যবহার করায় model differences paired। Primary metric balanced accuracy, কারণ class ratio প্রায় 58/42 এবং শুধু raw accuracy majority class-এর দিকে ঝুঁকতে পারে। Secondary metrics: accuracy, sensitivity, specificity, F1, MCC এবং ROC-AUC।</p>
<p>Nadeau–Bengio corrected standard error দিয়ে 95% confidence interval তৈরি করা হয়েছে; cross-validation training sets overlap করে বলে সাধারণ fold standard error অতিরিক্ত optimistic হতে পারে। H1-এর জন্য one-sided non-inferiority margin 0.03, H2-এর জন্য one-sided superiority test। Non-significant ফলকে “সমান প্রমাণিত” না বলে “significant evidence নেই” বলা হয়েছে।</p>
<p>দুটি validation view রাখা হয়েছে: fixed exploratory δ = 0.2 এবং training fold-এর ভিতর δ নির্বাচন করা stricter analysis। এই separation tuning optimism সম্পর্কে সৎ ধারণা দেয়।</p>

<h2 class="pagebreak">৭. ফলাফল</h2>
<h3>৭.১ Main Model Comparison / প্রধান model comparison</h3>
{results}
<p>CGTH-এর balanced accuracy RF-এর চেয়ে মাত্র 0.005 কম এবং LR coverage 68%। অর্থাৎ decision performance RF-এর কাছাকাছি রেখে অধিকাংশ decision simple model-এর হাতে রাখা সম্ভব হয়েছে—fixed δ analysis-এ এটি প্রকল্পের প্রধান empirical result। তবে CGTH-এর ROC-AUC RF-এর চেয়ে কম (0.809 বনাম 0.835), কারণ দুই model-এর decision probability মিশে ranking quality কমে। CGTH একটি decision policy; তাই balanced accuracy primary হওয়া যুক্তিসঙ্গত।</p>
<h3>৭.২ Hypothesis Tests / hypothesis পরীক্ষা</h3>
<table>
<thead><tr><th>Hypothesis</th><th>Observed difference</th><th>p-value</th><th>Interpretation</th></tr></thead>
<tbody>
<tr><td>H1 fixed δ=0.2: CGTH non-inferior to RF</td><td>−0.0046</td><td>&lt;0.001</td><td>সমর্থিত, কিন্তু δ exploratoryভাবে দেখা হয়েছিল।</td></tr>
<tr><td>H2: CGTH better than LR</td><td>+0.0264</td><td>0.080</td><td>Significant evidence নেই।</td></tr>
<tr><td>Strict H1: δ training fold-এ নির্বাচন</td><td>−0.0112</td><td>0.060</td><td>Non-inferiority প্রতিষ্ঠিত নয়; ফলাফল suggestive।</td></tr>
<tr><td>Strict H2</td><td>+0.0197</td><td>0.127</td><td>Significant evidence নেই।</td></tr>
</tbody></table>
<h3>৭.৩ Why Does the Gate Work? / gate কেন কাজ করে?</h3>
<table>
<thead><tr><th>Condition</th><th>Accuracy</th></tr></thead>
<tbody><tr><td>LR on confident cases</td><td>0.806</td></tr><tr><td>LR on uncertain cases</td><td>0.606</td></tr><tr><td>RF on uncertain cases</td><td>0.709</td></tr></tbody></table>
<p>এই ফল CGTH-এর mechanism support করে: LR confident case-এ ভালো, কিন্তু boundary case-এ RF তুলনামূলকভাবে বেশি useful।</p>
<div class="figure"><img src="file://{(ROOT / 'results' / 'transparency_vs_performance.png').as_posix()}"><div class="caption">চিত্র ১: Delta বাড়লে transparent LR coverage ও balanced accuracy-এর trade-off।</div></div>
<div class="figure"><img src="file://{(ROOT / 'results' / 'model_comparison.png').as_posix()}"><div class="caption">চিত্র ২: প্রধান model-গুলোর comparative ফল।</div></div>

<h2>৮. Robustness, Performance Ceiling and Subgroup Analysis / robustness ও subgroup analysis</h2>
<h3>৮.১ Data-quality Robustness / data-quality robustness</h3>
<table>
<thead><tr><th>Model</th><th>Unique rows</th><th>Duplicates kept</th><th>Guilt item removed</th></tr></thead>
<tbody>
<tr><td>CGTH</td><td>0.757</td><td>0.843</td><td>0.601</td></tr>
<tr><td>LR</td><td>0.730</td><td>0.796</td><td>0.601</td></tr>
<tr><td>RF</td><td>0.761</td><td>0.855</td><td>0.602</td></tr>
<tr><td>Soft voting</td><td>0.741</td><td>0.813</td><td>0.601</td></tr>
</tbody></table>
<p>Duplicates রেখে score 0.84–0.86 হওয়া স্পষ্ট leakage inflation। Guilt item বাদ দিলে সব model প্রায় 0.60—তাই headline performance-কে clinically meaningful general signal ধরে নেওয়া যাবে না।</p>
<h3>৮.২ Performance Ceiling / performance ceiling</h3>
<p>Tuned RF, Extra Trees, SVM, Gradient Boosting, categorical Naive Bayes, tuned LR এবং k-NN-এর balanced accuracy আনুমানিক 0.69–0.76। অর্থাৎ এই data ও label-এ leakage ছাড়া প্রায় 0.76-এর কাছাকাছি একটি ceiling দেখা যায়; শুধু আরও complex model যোগ করলে বড় উন্নতি হওয়ার প্রমাণ নেই।</p>
<h3>৮.৩ Age-band Descriptive Check / age-band বিশ্লেষণ</h3>
{age}
<p>Age-band ফল fairness proof নয়: প্রতিটি band-এ unique row মাত্র 49–76। এটি subgroup monitoring-এর শুরু, final fairness claim নয়।</p>
<h3>৮.৪ Train–Test Gap / train–test gap</h3>
<p>CGTH balanced accuracy train 0.792 বনাম validation/test 0.757; gap 0.036। RF-এর gap 0.035 এবং AUC gap 0.099। এই gap small-n generalisation uncertainty দেখায়, কিন্তু external validation-এর বিকল্প নয়।</p>

<h2>৯. Explainability, Contributions and Practical Benefits / explainability ও ব্যবহারিক benefit</h2>
<ul>
  <li><b>Individual transparency:</b> LR-decided case odds ratio দিয়ে কোন response association decision-এ অবদান রেখেছে তা বোঝানো যায়।</li>
  <li><b>Coverage:</b> 68% decision transparent model করেছে; stricter fold-wise δ-তে coverage 77%, কিন্তু statistical guarantee দুর্বল হয়েছে।</li>
  <li><b>Operational benefit:</b> সব case-এ black-box model না চালিয়ে audit-friendly default রাখা যায়; uncertain case আলাদা queue বা second review-তে পাঠানো যায়।</li>
  <li><b>Research benefit:</b> শুধু best AUC নয়, performance–transparency trade-off মাপা হয়েছে।</li>
</ul>
<p>Odds ratio association, causation নয়। কোনো survey answer postpartum anxiety-এর clinical cause প্রমাণ করে না। SHAP/LIME যোগ করা গেলেও তা এই data-এর label validity বা external generalisation ঠিক করবে না; explanation stability resample-এর ওপর ভবিষ্যতে মাপা উচিত।</p>

<h2>১০. Limitations, Reviewer Criticism and Honest Interpretation / সীমাবদ্ধতা</h2>
<table>
<thead><tr><th>সম্ভাব্য প্রশ্ন</th><th>সৎ উত্তর</th></tr></thead>
<tbody>
<tr><td>এটি কি clinical screening model?</td><td>না। এটি self-reported anxiety item prediction; validated clinical reference standard নেই।</td></tr>
<tr><td>CGTH কি প্রমাণিতভাবে RF-এর সমান?</td><td>Fixed δ-তে H1 সমর্থিত; fold-wise δ selection-এ p=0.06, তাই definitive নয়।</td></tr>
<tr><td>CGTH কি LR-এর চেয়ে better?</td><td>Observed gain +0.026, কিন্তু p=0.08; superiority প্রমাণিত নয়।</td></tr>
<tr><td>Dataset reliable?</td><td>না বলা যাবে না: provenance unclear, 78% duplicates, 90 timestamp, single-item label। Audit এগুলো quantify করেছে।</td></tr>
<tr><td>Novelty কী?</td><td>Cascade ধারণা পুরনো; novelty হলো এই setting-এ transparent-first application ও coverage reporting।</td></tr>
<tr><td>External validation আছে?</td><td>নেই; দ্বিতীয় independent validated dataset প্রয়োজন।</td></tr>
<tr><td>Hyperparameter tuning?</td><td>Main LR/RF settings pre-fixed; broader ceiling analysis-এ inner tuning করা হয়েছে।</td></tr>
</tbody></table>

<h2>১১. Reproducibility and Project Structure / reproducibility ও project structure</h2>
<p>মূল experiment এক notebook-এ ২২টি task হিসেবে রাখা হয়েছে। Raw dataset read-only; outputs <code>results/</code>-এ CSV এবং PNG হিসেবে সংরক্ষিত। Seed 42, δ grid, non-inferiority margin এবং library versions সংরক্ষণ করা হয়েছে। এই separation audit trail তৈরি করে এবং একই result পুনরায় চালানোর সুযোগ বাড়ায়।</p>
<table>
<thead><tr><th>Path</th><th>ভূমিকা</th></tr></thead>
<tbody>
<tr><td><code>data/DATA_CARD.md</code></td><td>Source, size, ethics, known issues।</td></tr>
<tr><td><code>research_plan/01–09</code></td><td>Audit, literature, hypotheses, architecture, methodology, limitations, roadmap।</td></tr>
<tr><td><code>notebooks/01_cgth_hybrid_study.ipynb</code></td><td>পুরো leakage-free analysis pipeline।</td></tr>
<tr><td><code>results/*.csv</code></td><td>Model metrics, tests, robustness, subgroup ও ceiling outputs।</td></tr>
<tr><td><code>results/*.png</code></td><td>Comparison ও transparency figures।</td></tr>
</tbody></table>

<h2>১২. Remaining Work: Priority Roadmap / কী কী করা বাকি</h2>
<ol>
  <li><b>অবিলম্বে:</b> Kaggle provenance/licence যাচাই এবং একই dataset নিয়ে prior 2026 analysis পূর্ণপাঠে যাচাই।</li>
  <li><b>ডেটা:</b> validated EPDS/PHQ বা clinician-verified outcome-সহ independent Bangladesh বা multi-site dataset সংগ্রহ।</li>
  <li><b>Validation:</b> temporal/external validation, pre-registered threshold, sample-size justification এবং calibration curve/Brier score যোগ করা।</li>
  <li><b>Clinical utility:</b> decision-curve analysis, false-negative cost, referral threshold এবং clinician-in-the-loop usability study।</li>
  <li><b>Fairness:</b> age ছাড়াও parity, calibration ও error-rate subgroup analysis; যথেষ্ট subgroup sample ছাড়া claim না করা।</li>
  <li><b>Explainability:</b> bootstrap/resample-এ odds ratio ও explanation stability, uncertainty intervals, এবং user-facing explanation test।</li>
  <li><b>Reporting:</b> TRIPOD+AI checklist, complete feature dictionary, preprocessing code, model card ও data-use statement যোগ করা।</li>
</ol>
<div class="callout good"><b>Publication-ready হওয়ার প্রধান শর্ত:</b> দ্বিতীয় independent dataset-এ validated label দিয়ে result replicate করা। এটি নতুন algorithm যোগ করার চেয়ে অনেক বেশি গুরুত্বপূর্ণ উন্নতি হবে।</div>

<h2>১৩. Conclusion / উপসংহার</h2>
<p>CGTH একটি বাস্তবসম্মত, audit-friendly hybrid design: simple model confident হলে explanation বজায় থাকে, uncertain case-এ stronger RF ব্যবহার হয়। এই project-এ 68% transparent coverage সহ RF-এর কাছাকাছি balanced accuracy পাওয়া গেছে। কিন্তু এই সাফল্যকে clinical performance বলা যাবে না, কারণ data duplication, unclear provenance, self-reported single-item label এবং small effective sample বড় সীমাবদ্ধতা।</p>
<p>সুতরাং প্রকল্পটির সবচেয়ে শক্তিশালী উন্নতি হলো শুধু নতুন model নয়—সঠিক audit, leakage-free validation, corrected uncertainty, honest hypothesis reporting এবং transparency–performance trade-off। পরবর্তী ধাপে external validated data ও clinical utility evaluation যোগ হলে CGTH ধারণাটি গবেষণা থেকে দায়িত্বশীল screening-support prototype-এর দিকে এগোতে পারবে।</p>

<h2>References and Methodology Sources / তথ্যসূত্র</h2>
{refs}
<p class="small">নোট: Literature review-এর যেসব entry-র metadata research plan-এ অসম্পূর্ণ হিসেবে চিহ্নিত, সেগুলো final thesis bibliography-তে DOI/journal page দেখে পুনরায় যাচাই করতে হবে।</p>

</body></html>"""


if __name__ == "__main__":
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(build_html(), encoding="utf-8")
    print(f"Wrote {HTML_OUT} ({HTML_OUT.stat().st_size} bytes)")
