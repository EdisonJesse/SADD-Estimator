# ACCORD SADD Estimator

The **ACCORD SADD Estimator** is a premium, self-contained single-page web application designed for humanitarian responders, information managers, and planning teams. It calculates estimated disaggregations of sex, age cohorts, and functional difficulty/disability levels for any municipality in the Philippines, based on the **Philippine Statistics Authority (PSA) 2020 Census of Population and Housing (CPH)**.

This tool helps organizations meet humanitarian accountability standards by providing instant, localized **Sex, Age, and Disability Disaggregated Data (SADD)** during disaster response and anticipatory action planning.

---

## 🌟 Features

* **Complete Geographic Coverage**: Aligned and mapped with the official geographic taxonomy of 1,658 Philippine municipalities.
* **Separated Sex Disaggregations**: Displays separate charts and tables for male and female breakdowns to prevent merged-data assumptions.
* **Functional Difficulty Tracking**: Displays estimates for the 6 standard domains (Seeing, Hearing, Walking, Remembering, Self Caring, Communicating) across all severity levels (Mild, Moderate, Severe, Any).
* **Mathematical Rounding Consistency**: Uses the **Largest Remainder Method (Hamilton Method)** to distribute cohort calculations, guaranteeing that rounded sub-category counts sum up exactly to the user-entered total population.
* **100% Offline Compatible**: The application is self-contained. All municipal ratios are embedded inside the file, requiring no database connections or external APIs to run.
* **Modern Premium UI**: Built with a responsive, glassmorphic layout featuring custom dark/light modes and dynamic grouped charts.
* **Clean Data Export**: Instantly download calculated breakdowns as a structured, spreadsheet-ready CSV file.

---

## 🛠️ Tech Stack

* **Frontend**: HTML5, Vanilla CSS3 (Custom design system), JavaScript (ES6+)
* **Libraries**: [Chart.js](https://www.chartjs.org/) (Grouped bar charts and donuts)
* **Typography**: Google Fonts (Inter & Outfit)

---

## 📊 Data & Fallback Methodology

The estimator leverages:
1. **PSA 2020 CPH Household Population by Age Group and Sex**
2. **PSA 2020 CPH Household Population 5 Years Old and Over with Functional Difficulty**

### Missing Data Handling:
For municipalities completely missing from the raw PSA difficulty datasets (e.g., *Peñablanca, Cagayan* and *Sasmuan, Pampanga*), the tool dynamically calculates and applies the weighted provincial average of all other municipalities in that province to ensure data integrity and prevent blank or zero values.

---

## 🚀 Deployment

### Option A: GitHub Pages (Recommended)
Because the app is a single static file (`estimator_app.html`), you can host it for free on GitHub Pages:
1. Go to your repository **Settings** > **Pages**.
2. Under **Build and deployment**, set the source to **Deploy from a branch** (usually `main` or `root`).
3. Click **Save**. Your estimator will be live at `https://[your-username].github.io/[repo-name]/estimator_app.html`.
4. Paste this URL into your SharePoint page's **Embed** Web Part.

### Option B: SharePoint (Local ASPX Page)
If your organization requires hosting directly on SharePoint:
1. Rename the file extension from `estimator_app.html` to `estimator_app.aspx`.
2. Upload the file to your site's **Site Assets** library.
3. Reference the file path inside a standard `<iframe>` in SharePoint's **Embed** Web Part:
   ```html
   <iframe src="https://[domain].sharepoint.com/sites/[site]/SiteAssets/estimator_app.aspx" width="100%" height="900px" style="border:none;"></iframe>
