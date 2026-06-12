import json
import os

psa_dir = r"c:\AI Projects\Sarangani Earthquake\PSA"
json_path = os.path.join(psa_dir, "municipality_ratios.json")
html_path = os.path.join(psa_dir, "estimator_app.html")

print("Loading ratios JSON data...")
with open(json_path, 'r') as f:
    ratios_data = json.load(f)

print(f"Loaded {len(ratios_data)} municipalities.")

# Load Base64 logo
logo_txt_path = os.path.join(psa_dir, "logo_base64.txt")
with open(logo_txt_path, 'r') as f:
    logo_base64 = f.read().strip()

# We will generate the single-file HTML app
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACCORD SADD Estimator</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- CDNs -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        :root {
            --bg-primary: #0b0f19;
            --bg-secondary: #161c2d;
            --bg-glass: rgba(22, 28, 45, 0.6);
            --border-glass: rgba(255, 255, 255, 0.08);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent: #2563eb;
            --accent-glow: rgba(37, 99, 235, 0.4);
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .light-theme {
            --bg-primary: #f3f4f6;
            --bg-secondary: #ffffff;
            --bg-glass: rgba(255, 255, 255, 0.7);
            --border-glass: rgba(0, 0, 0, 0.08);
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --accent: #1d4ed8;
            --accent-glow: rgba(29, 78, 216, 0.2);
            --accent-success: #059669;
            --accent-warning: #d97706;
            --accent-danger: #dc2626;
            --card-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Glassmorphism Navigation */
        header {
            background: var(--bg-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-glass);
            padding: 1.25rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: #ffffff;
            font-size: 1.25rem;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
            font-family: 'Outfit', sans-serif;
        }

        .logo-text h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .logo-text p {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .theme-toggle {
            background: var(--bg-secondary);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            font-weight: 500;
            box-shadow: var(--card-shadow);
        }

        .theme-toggle:hover {
            border-color: var(--accent);
        }

        /* Layout */
        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 320px minmax(0, 1fr);
            gap: 2rem;
            flex-grow: 1;
            width: 100%;
        }

        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
            }
        }

        /* Glassmorphism Card Style */
        .card {
            background: var(--bg-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass);
            border-radius: 1rem;
            padding: 1.25rem 1.5rem;
            box-shadow: var(--card-shadow);
            display: flex;
            flex-direction: column;
            gap: 1rem;
            height: fit-content;
            min-width: 0; /* Prevents flex children from stretching container */
        }

        h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border-glass);
            padding-bottom: 0.75rem;
            color: var(--text-primary);
        }

        /* Form Controls */
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--text-secondary);
        }

        select, input {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.95rem;
            width: 100%;
            outline: none;
        }

        select:focus, input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .btn {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: #ffffff;
            border: none;
            padding: 0.875rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: var(--bg-secondary);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
            box-shadow: none;
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--text-secondary);
            box-shadow: none;
        }

        /* Results Area */
        .results-container {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .placeholder-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 5rem 2rem;
            color: var(--text-secondary);
            border: 2px dashed var(--border-glass);
            border-radius: 1rem;
        }

        .placeholder-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        /* Summary KPIs */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
        }

        .kpi-card {
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 0.75rem;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            position: relative;
            overflow: hidden;
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }

        .kpi-card.blue::before { background-color: #3b82f6; }
        .kpi-card.purple::before { background-color: #8b5cf6; }
        .kpi-card.green::before { background-color: #10b981; }

        .kpi-value {
            font-family: 'Outfit', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
        }

        .kpi-label {
            font-size: 0.8rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Dashboard Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr);
            gap: 2rem;
        }

        @media (max-width: 900px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .full-width {
            grid-column: span 2;
        }

        @media (max-width: 900px) {
            .full-width {
                grid-column: span 1;
            }
        }

        /* Chart container */
        .chart-box {
            position: relative;
            height: 180px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Tables */
        .table-container {
            overflow-x: auto;
            border-radius: 0.5rem;
            border: 1px solid var(--border-glass);
            background-color: rgba(0, 0, 0, 0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }

        th {
            background-color: rgba(255, 255, 255, 0.02);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid var(--border-glass);
        }

        td {
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid var(--border-glass);
            color: var(--text-primary);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.01);
        }

        /* Tabs/Segmented Control */
        .tabs {
            display: flex;
            background: var(--bg-secondary);
            padding: 0.25rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-glass);
            width: fit-content;
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            font-weight: 600;
            border-radius: 0.375rem;
            cursor: pointer;
        }

        .tab-btn.active {
            background: var(--accent);
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--border-glass);
            color: var(--text-secondary);
            font-size: 0.8rem;
            background-color: var(--bg-glass);
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
        }

        /* Container Layout Toggles */
        .container.full-width-layout {
            grid-template-columns: 1fr;
        }

        /* Main Tabs Navigation */
        .main-tabs {
            display: flex;
            background: var(--bg-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-glass);
            padding: 0.5rem 2rem;
            position: sticky;
            top: 70px;
            z-index: 99;
            gap: 1rem;
            overflow-x: auto;
        }

        .main-tab-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.75rem 1.25rem;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .main-tab-btn:hover {
            color: var(--text-primary);
        }

        .main-tab-btn.active {
            color: var(--accent);
            border-bottom-color: var(--accent);
        }

        /* Scrollable Checkbox Container */
        .checkbox-container {
            border: 1px solid var(--border-glass);
            border-radius: 0.5rem;
            background: var(--bg-secondary);
            padding: 0.75rem;
            max-height: 200px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            cursor: pointer;
            color: var(--text-primary);
        }

        .checkbox-item input {
            width: auto;
            margin: 0;
            cursor: pointer;
        }

        .checkbox-actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.25rem;
        }

        .btn-small {
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            border-radius: 0.25rem;
        }

        /* Info Content Views */
        .info-content {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            max-width: 950px;
            margin: 0 auto;
            padding: 1.5rem 0;
            width: 100%;
        }

        .info-section {
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 1rem;
            padding: 1.5rem 2rem;
            box-shadow: var(--card-shadow);
        }

        .info-section h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            color: var(--accent);
            margin-bottom: 0.75rem;
            font-weight: 600;
        }

        .info-section p {
            font-size: 0.95rem;
            line-height: 1.6;
            color: var(--text-primary);
            margin-bottom: 1rem;
        }

        .info-section p:last-child {
            margin-bottom: 0;
        }

        .info-section ul {
            margin-left: 1.5rem;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .info-section li {
            margin-bottom: 0.5rem;
        }
        
        .info-section code {
            background: rgba(255, 255, 255, 0.07);
            padding: 0.1rem 0.4rem;
            border-radius: 0.25rem;
            font-family: monospace;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <header>
        <div class="logo-container">
            <img src='""" + logo_base64 + """' alt="ACCORD Logo" style="height: 2.5rem; border-radius: 0.25rem; background: white; padding: 2px;">
            <div class="logo-text">
                <h1>ACCORD</h1>
                <p>SADD Estimator</p>
            </div>
        </div>
        <button class="theme-toggle" id="themeToggleBtn" onclick="toggleTheme()">
            <svg id="themeIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
            <span id="themeToggleText">Light Mode</span>
        </button>
    </header>

    <div class="main-tabs">
        <button class="main-tab-btn active" id="tabBtnSingle" onclick="showMainTab('single')">Single Municipality</button>
        <button class="main-tab-btn" id="tabBtnMulti" onclick="showMainTab('multi')">Multiple Selection</button>
        <button class="main-tab-btn" id="tabBtnMethod" onclick="showMainTab('methodology')">Computation Method</button>
        <button class="main-tab-btn" id="tabBtnPrivacy" onclick="showMainTab('privacy')">Privacy & Disclaimer</button>
    </div>

    <div class="container" id="mainContainer">
        <!-- Control Card (Single Mode) -->
        <div class="card" id="cardSingleSidebar">
            <h2>Select Parameters</h2>
            
            <div class="form-group">
                <label for="provinceSelect">Province</label>
                <select id="provinceSelect" onchange="onProvinceChange()">
                    <option value="">-- Select Province --</option>
                </select>
            </div>

            <div class="form-group">
                <label for="municipalitySelect">Municipality</label>
                <select id="municipalitySelect" disabled onchange="onMunicipalityChange()">
                    <option value="">-- Select Municipality --</option>
                </select>
            </div>

            <div class="form-group">
                <label for="populationInput">Affected Population Count</label>
                <input type="number" id="populationInput" min="1" placeholder="Enter total count" value="10000" oninput="calculateEstimates()">
            </div>

            <div class="form-group">
                <label for="ageDisaggregationSelect">Age Disaggregation</label>
                <select id="ageDisaggregationSelect" onchange="onAgeDisaggregationChange(this.value)">
                    <option value="standard">Standard (5-Year Brackets)</option>
                    <option value="alternative">Alternative (0 to 4, 5 to 17, 18 to 59, 60+)</option>
                </select>
            </div>

            <button class="btn" onclick="calculateEstimates()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Calculate Estimates
            </button>
            <button class="btn btn-secondary" onclick="resetForm()">Reset</button>
        </div>

        <!-- Control Card (Multi Mode) -->
        <div class="card" id="cardMultiSidebar" style="display: none;">
            <h2>Select Parameters</h2>
            
            <div class="form-group">
                <label for="provinceSelectMulti">Province</label>
                <select id="provinceSelectMulti" onchange="onProvinceMultiChange()">
                    <option value="">-- Select Province --</option>
                </select>
            </div>

            <div class="form-group">
                <label>Municipalities</label>
                <div class="checkbox-actions">
                    <button class="btn btn-secondary btn-small" onclick="selectAllMuns(true)">Select All</button>
                    <button class="btn btn-secondary btn-small" onclick="selectAllMuns(false)">Clear All</button>
                </div>
                <div class="checkbox-container" id="checkboxContainerMulti" style="margin-top: 0.5rem;">
                    <span style="font-size: 0.85rem; color: var(--text-secondary);">Select a province first...</span>
                </div>
            </div>

            <div class="form-group">
                <label for="populationInputMulti">Total Affected Population</label>
                <input type="number" id="populationInputMulti" min="1" placeholder="Enter total count" value="10000" oninput="calculateEstimates()">
            </div>

            <div class="form-group">
                <label for="ageDisaggregationSelectMulti">Age Disaggregation</label>
                <select id="ageDisaggregationSelectMulti" onchange="onAgeDisaggregationChange(this.value)">
                    <option value="standard">Standard (5-Year Brackets)</option>
                    <option value="alternative">Alternative (0 to 4, 5 to 17, 18 to 59, 60+)</option>
                </select>
            </div>

            <button class="btn" onclick="calculateEstimates()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Calculate Estimates
            </button>
            <button class="btn btn-secondary" onclick="resetFormMulti()">Reset</button>
        </div>

        <!-- Output Results Area -->
        <div class="results-container" id="resultsContainer">
            <!-- Placeholder before selection -->
            <div id="placeholder" class="placeholder-card">
                <div class="placeholder-icon">📊</div>
                <h3>Estimator Dashboard</h3>
                <p>Select a Province and Municipality, then input the affected population to view estimated disaggregation.</p>
            </div>

            <!-- Dashboard Content (hidden initially) -->
            <div id="dashboard" style="display: none;" class="results-container">
                <!-- Branded Report Header (included in image export) -->
                <div class="dashboard-report-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--accent); padding-bottom: 0.75rem; margin-bottom: 1rem; width: 100%;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <img src='""" + logo_base64 + """' alt="ACCORD Logo" style="height: 3rem; border-radius: 0.25rem; background: white; padding: 2px;">
                        <div>
                            <h2 style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 700; border-bottom: none; padding-bottom: 0; margin: 0; color: var(--text-primary);">SADD Estimator Report</h2>
                            <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0;">Sex, Age, and Disability Projections</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p id="reportLocationLabel" style="font-size: 1.05rem; font-weight: 600; color: var(--accent); margin: 0;">Alabel, Sarangani</p>
                        <p id="reportDateLabel" style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">Generated on: June 12, 2026</p>
                    </div>
                </div>

                <!-- KPI cards -->
                <div class="kpi-grid">
                    <div class="kpi-card blue">
                        <span class="kpi-label">Selected Location</span>
                        <span class="kpi-value" id="kpiLocation" style="font-size: 1.25rem; margin-top: 0.5rem;">Alabel, Sarangani</span>
                    </div>
                    <div class="kpi-card purple">
                        <span class="kpi-label">Affected Population</span>
                        <span class="kpi-value" id="kpiAffected">10,000</span>
                    </div>
                    <div class="kpi-card green">
                        <span class="kpi-label">Est. Population with Functional Difficulty</span>
                        <span class="kpi-value" id="kpiDisability">564</span>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <!-- Sex Breakdown Card -->
                    <div class="card">
                        <h2>Sex Disaggregation</h2>
                        <div class="chart-box">
                            <canvas id="sexChart"></canvas>
                        </div>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Sex</th>
                                        <th>Ratio</th>
                                        <th>Estimated Count</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Male</td>
                                        <td id="maleRatio">51.2%</td>
                                        <td id="maleCount" style="font-weight: 600;">5,120</td>
                                    </tr>
                                    <tr>
                                        <td>Female</td>
                                        <td id="femaleRatio">48.8%</td>
                                        <td id="femaleCount" style="font-weight: 600;">4,880</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Functional Difficulty Card -->
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-glass); padding-bottom: 0.5rem;">
                            <h2>Functional Difficulty</h2>
                            <div class="tabs">
                                <button class="tab-btn active" id="btnAll" onclick="changeSeverityTab('All')">Any</button>
                                <button class="tab-btn" id="btnMild" onclick="changeSeverityTab('Mild')">Mild</button>
                                <button class="tab-btn" id="btnModerate" onclick="changeSeverityTab('Moderate')">Mod</button>
                                <button class="tab-btn" id="btnSevere" onclick="changeSeverityTab('Severe')">Sev</button>
                            </div>
                        </div>
                        <div class="chart-box" style="height: 180px;">
                            <canvas id="disabilityChart"></canvas>
                        </div>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Difficulty Domain</th>
                                        <th>Male Est. (%)</th>
                                        <th>Female Est. (%)</th>
                                        <th>Total Est. (%)</th>
                                    </tr>
                                </thead>
                                <tbody id="disabilityTableBody">
                                    <!-- Dynamic Rows -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Age Disaggregation Card -->
                    <div class="card full-width">
                        <h2>Age Cohort Disaggregation</h2>
                        <div class="chart-box" style="height: 280px; margin-bottom: 1rem;">
                            <canvas id="ageChart"></canvas>
                        </div>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Age Cohort</th>
                                        <th>Male %</th>
                                        <th>Male Est.</th>
                                        <th>Female %</th>
                                        <th>Female Est.</th>
                                        <th>Total %</th>
                                        <th>Total Est.</th>
                                    </tr>
                                </thead>
                                <tbody id="ageTableBody">
                                    <!-- Dynamic Rows -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Export Action -->
                <div style="display: flex; gap: 1rem; align-self: flex-end; width: fit-content; margin-top: 1rem;">
                    <button class="btn btn-secondary" onclick="exportDashboardImage()">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                        </svg>
                        Export Dashboard as Image (PNG)
                    </button>
                    <button class="btn" onclick="exportCSV()">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                        Export Full Disaggregation Report (CSV)
                    </button>
                </div>
            </div>

            <!-- Computation Method Tab (hidden initially) -->
            <div id="methodologyTab" style="display: none;" class="info-content">
                <div class="info-section">
                    <h3>Computation Methodology</h3>
                    <p>The ACCORD Sex, Age, and Disability Disaggregation (SADD) Estimator uses a mathematically rigorous, offline-compatible model to project census ratios onto user-entered affected populations.</p>
                </div>
                
                <div class="info-section">
                    <h3>Sex and Age Disaggregation</h3>
                    <p>Ratios are extracted from the PSA 2020 Census of Population and Housing. Gender and age cohorts are computed independently to maintain demographic integrity:</p>
                    <ul>
                        <li><strong>Sex Breakdown</strong>: Projected counts are derived using the municipal ratios:
                            <br><code>Male Count = round(Population * Male_Ratio)</code>
                            <br><code>Female Count = Population - Male Count</code>
                        </li>
                        <li><strong>Age Cohort Distribution</strong>: Distributed independently for Male and Female cohorts using the <strong>Largest Remainder Method (Hamilton Method)</strong>. This avoids mathematical rounding errors and guarantees that the sum of the age cohorts matches the total male and female counts exactly.</li>
                    </ul>
                </div>

                <div class="info-section">
                    <h3>Functional Difficulty Estimation (WGQ)</h3>
                    <p>Prevalence calculations for functional difficulties follow the official <strong>Washington Group Questions (WGQ)</strong> taxonomy across 6 domains (Seeing, Hearing, Walking, Remembering, Self-Caring, and Communicating) and 4 severity levels (Mild, Moderate, Severe, and All/Any):</p>
                    <ul>
                        <li><strong>Aged 5 and Over Denominator</strong>: Since functional difficulty census surveys are only conducted for individuals aged 5 and over, the ratios in the database use the population aged 5+ (excluding the 0-4 cohort) as the denominator, as per international reporting standards.</li>
                        <li><strong>Overall Prevalence Estimation</strong>: In the census data, individual-level microdata is aggregated into domain counts. Because individuals can experience difficulties in more than one domain simultaneously (e.g. both vision and walking limitations), summing the domains together would cause significant double-counting. 
                        <br>To estimate the number of unique individuals experiencing functional difficulty, the dashboard applies the <strong>Maximum Domain Count</strong> rule under the <em>All</em> severity level:
                        <br><code>Est. Population with Functional Difficulty = max(Domain_Count_All)</code>
                        This represents the most accurate, conservative threshold estimate of individuals experiencing at least one functional difficulty.</li>
                    </ul>
                </div>

                <div class="info-section">
                    <h3>Aggregation for Multiple Municipalities</h3>
                    <p>When multiple municipalities are selected, the user-entered population is distributed proportionally among them based on their respective official 2020 census populations:</p>
                    <ul>
                        <li><strong>Proportional Allocation</strong>: 
                            <br><code>Allocated Pop (Mun i) = Total Entered Pop * (Census Pop (Mun i) / Sum of Census Pops)</code>
                        </li>
                        <li><strong>Weighted Ratios</strong>: The synthetic municipality's ratios are computed as the weighted averages of the selected municipalities' ratios, weighted by their total, male, female, or 5+ populations respectively. This ensures that the aggregated estimates are mathematically equivalent to computing individual counts and summing them.</li>
                    </ul>
                </div>
            </div>

            <!-- Privacy & Disclaimer Tab (hidden initially) -->
            <div id="privacyTab" style="display: none;" class="info-content">
                <div class="info-section">
                    <h3>GDPR Compliance & Data Privacy Notice</h3>
                    <p>We take data privacy and compliance seriously. This notice explains how the SADD Estimator handles data under the General Data Protection Regulation (GDPR) and the Philippine Data Privacy Act of 2012 (RA 10173):</p>
                    <ul>
                        <li><strong>100% Client-Side Processing</strong>: The application runs entirely within your local browser. All calculations, data inputs, and exports are performed in-memory on your device.</li>
                        <li><strong>Zero External Data Transmission</strong>: No data entered into this application (such as affected population counts or location selections) is sent to external servers, database hosts, or third-party APIs. The application works completely offline.</li>
                        <li><strong>No Cookies or Tracking</strong>: We do not use cookies, tracking pixels, local storage trackers, or analytics scripts (like Google Analytics). Your usage is completely private and untracked.</li>
                        <li><strong>No Personal Data (PII) Collected</strong>: Since the app does not collect, store, or transmit names, contact details, or specific identifiers, it is fully compliant with GDPR data minimization principles.</li>
                    </ul>
                </div>

                <div class="info-section">
                    <h3>Data Disclaimer & Limitations</h3>
                    <ul>
                        <li><strong>Estimation Proxy</strong>: The dashboard provides estimated numbers based on historical census distributions (PSA Census 2020). Actual numbers in active disaster areas may vary due to local migration, post-2020 demographic shifts, and specific hazard exposure.</li>
                        <li><strong>Self-Reported Limitations</strong>: The Washington Group Questions measure self-reported difficulties in basic activity domains. They reflect functional limitations rather than clinical medical diagnoses.</li>
                        <li><strong>Operational Decisions</strong>: These figures are intended as a tool for initial rapid needs assessments and response planning. They do not replace formal beneficiary registration or direct field verification.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>ACCORD &copy; 2026. Data sourced from PSA 2020 Census of Population and Housing.</p>
    </footer>

    <script>
        // Embed the computed ratios directly
        const MUNICIPALITY_DATA = """ + json.dumps(ratios_data) + """;

        let currentSeverity = 'All'; // Active tab
        let selectedMunicipality = null;
        let sexChartObj = null;
        let ageChartObj = null;
        let disabilityChartObj = null;

        let activeMode = 'single'; // 'single' or 'multi'
        let singleSelectedMun = null;
        let multiSyntheticMun = null;
        let ageDisaggregationMode = 'standard'; // 'standard' or 'alternative'

        function onAgeDisaggregationChange(val) {
            ageDisaggregationMode = val;
            document.getElementById('ageDisaggregationSelect').value = val;
            document.getElementById('ageDisaggregationSelectMulti').value = val;
            calculateEstimates();
        }

        // Track last calculation to align UI display with CSV exports exactly
        let lastCalculation = {
            pop: 0,
            maleCount: 0,
            femaleCount: 0,
            ageKeys: [],
            ageLabels: [],
            ageRatios: {
                male: [],
                female: [],
                total: []
            },
            ageCounts: {
                male: [],
                female: [],
                total: []
            }
        };

        // Largest Remainder Method (Hamilton Method) to distribute population counts exactly summing to pop
        function distributePopulation(pop, ratios) {
            if (pop <= 0) return ratios.map(() => 0);
            let sumRatios = ratios.reduce((a, b) => a + b, 0);
            let normalizedRatios = sumRatios > 0 ? ratios.map(r => r / sumRatios) : ratios;
            
            let exacts = normalizedRatios.map(r => pop * r);
            let counts = exacts.map(Math.round);
            let sum = counts.reduce((a, b) => a + b, 0);
            let diff = pop - sum;
            if (diff === 0) return counts;
            
            let errors = exacts.map((e, idx) => ({
                idx: idx,
                val: counts[idx],
                diff: e - counts[idx]
            }));
            
            if (diff > 0) {
                errors.sort((a, b) => b.diff - a.diff);
                for (let i = 0; i < diff; i++) {
                    counts[errors[i].idx]++;
                }
            } else {
                errors.sort((a, b) => a.diff - b.diff);
                for (let i = 0; i < Math.abs(diff); i++) {
                    counts[errors[i].idx]--;
                }
            }
            return counts;
        }

        // Populate Province options
        function initializeApp() {
            const provinces = [...new Set(MUNICIPALITY_DATA.map(item => item.Province))].sort();
            const provinceSelect = document.getElementById('provinceSelect');
            
            const provinceSelectMulti = document.getElementById('provinceSelectMulti');
            provinces.forEach(prov => {
                const opt1 = document.createElement('option');
                opt1.value = prov;
                opt1.textContent = prov;
                provinceSelect.appendChild(opt1);
                
                const opt2 = document.createElement('option');
                opt2.value = prov;
                opt2.textContent = prov;
                provinceSelectMulti.appendChild(opt2);
            });
            
            // Set default to Sarangani and Alabel if present
            if (provinces.includes('Sarangani')) {
                provinceSelect.value = 'Sarangani';
                onProvinceChange();
                
                provinceSelectMulti.value = 'Sarangani';
                onProvinceMultiChange();
                
                const munSelect = document.getElementById('municipalitySelect');
                if ([...munSelect.options].some(opt => opt.value === 'Alabel')) {
                    munSelect.value = 'Alabel';
                    onMunicipalityChange();
                    calculateEstimates();
                }
            }
        }

        // Handle Province dropdown change
        function onProvinceChange() {
            const prov = document.getElementById('provinceSelect').value;
            const munSelect = document.getElementById('municipalitySelect');
            
            // Clear existing options
            munSelect.innerHTML = '<option value="">-- Select Municipality --</option>';
            selectedMunicipality = null;
            singleSelectedMun = null;
            
            if (!prov) {
                munSelect.disabled = true;
                document.getElementById('placeholder').style.display = 'flex';
                document.getElementById('dashboard').style.display = 'none';
                return;
            }
            
            // Get filtered municipalities
            const muns = MUNICIPALITY_DATA
                .filter(item => item.Province === prov)
                .map(item => item.Municipality)
                .sort();
                
            muns.forEach(mun => {
                const opt = document.createElement('option');
                opt.value = mun;
                opt.textContent = mun;
                munSelect.appendChild(opt);
            });
            
            munSelect.disabled = false;
        }

        // Handle Municipality dropdown change
        function onMunicipalityChange() {
            const prov = document.getElementById('provinceSelect').value;
            const mun = document.getElementById('municipalitySelect').value;
            
            if (!prov || !mun) {
                selectedMunicipality = null;
                singleSelectedMun = null;
                document.getElementById('placeholder').style.display = 'flex';
                document.getElementById('dashboard').style.display = 'none';
                return;
            }
            
            selectedMunicipality = MUNICIPALITY_DATA.find(item => item.Province === prov && item.Municipality === mun);
            singleSelectedMun = selectedMunicipality;
        }

        // Handle Province change in Multi mode
        function onProvinceMultiChange() {
            const prov = document.getElementById('provinceSelectMulti').value;
            const container = document.getElementById('checkboxContainerMulti');
            
            selectedMunicipality = null;
            multiSyntheticMun = null;
            
            if (!prov) {
                container.innerHTML = '<span style="font-size: 0.85rem; color: var(--text-secondary);">Select a province first...</span>';
                document.getElementById('placeholder').style.display = 'flex';
                document.getElementById('dashboard').style.display = 'none';
                return;
            }
            
            // Get municipalities
            const muns = MUNICIPALITY_DATA
                .filter(item => item.Province === prov)
                .map(item => item.Municipality)
                .sort();
                
            container.innerHTML = '';
            muns.forEach(mun => {
                const label = document.createElement('label');
                label.className = 'checkbox-item';
                
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.value = mun;
                input.onchange = calculateEstimates;
                
                label.appendChild(input);
                label.appendChild(document.createTextNode(mun));
                container.appendChild(label);
            });
            
            document.getElementById('placeholder').style.display = 'flex';
            document.getElementById('dashboard').style.display = 'none';
        }

        function selectAllMuns(isChecked) {
            const checkboxes = document.querySelectorAll('#checkboxContainerMulti input[type="checkbox"]');
            checkboxes.forEach(cb => {
                cb.checked = isChecked;
            });
            calculateEstimates();
        }

        function resetFormMulti() {
            document.getElementById('provinceSelectMulti').value = '';
            onProvinceMultiChange();
            document.getElementById('populationInputMulti').value = '10000';
        }

        // Build a synthetic weighted average municipality for multi-selection aggregation
        function buildSyntheticMunicipality(province, checkedCheckboxes) {
            const selectedMunNames = Array.from(checkedCheckboxes).map(cb => cb.value);
            const selectedItems = MUNICIPALITY_DATA.filter(item => item.Province === province && selectedMunNames.includes(item.Municipality));
            
            if (selectedItems.length === 0) return null;
            
            const totalCensusPop = selectedItems.reduce((sum, item) => sum + item.Total_Population, 0);
            const totalMalePop = selectedItems.reduce((sum, item) => sum + item.Male_Population, 0);
            const totalFemalePop = selectedItems.reduce((sum, item) => sum + item.Female_Population, 0);
            
            const itemDenoms = selectedItems.map(item => {
                const age_0_4_ratio = item['Age_0-4_Ratio'] || 0;
                const male_age_0_4_ratio = item['Male_Age_0-4_Ratio'] || 0;
                const female_age_0_4_ratio = item['Female_Age_0-4_Ratio'] || 0;
                
                return {
                    both: item.Total_Population * (1 - age_0_4_ratio),
                    male: item.Male_Population * (1 - male_age_0_4_ratio),
                    female: item.Female_Population * (1 - female_age_0_4_ratio)
                };
            });
            
            const totalDenomBoth = itemDenoms.reduce((sum, d) => sum + d.both, 0);
            const totalDenomMale = itemDenoms.reduce((sum, d) => sum + d.male, 0);
            const totalDenomFemale = itemDenoms.reduce((sum, d) => sum + d.female, 0);
            
            let munLabel = "";
            if (selectedMunNames.length <= 3) {
                munLabel = selectedMunNames.join(', ');
            } else {
                munLabel = `${selectedMunNames.length} Municipalities (${selectedMunNames.slice(0, 2).join(', ')} + ${selectedMunNames.length - 2} more)`;
            }
            
            const synthetic = {
                Province: province,
                Municipality: munLabel,
                Total_Population: totalCensusPop,
                Male_Population: totalMalePop,
                Female_Population: totalFemalePop,
                Male_Ratio: totalMalePop / totalCensusPop,
                Female_Ratio: totalFemalePop / totalCensusPop
            };
            
            const sampleItem = selectedItems[0];
            const ratioKeys = Object.keys(sampleItem);
            
            ratioKeys.forEach(k => {
                if (k === 'Male_Ratio' || k === 'Female_Ratio' || k === 'Total_Population' || k === 'Male_Population' || k === 'Female_Population') return;
                
                if (k.startsWith('Age_') && k.endsWith('_Ratio')) {
                    let weightedSum = 0;
                    selectedItems.forEach(item => {
                        weightedSum += (item[k] || 0) * item.Total_Population;
                    });
                    synthetic[k] = weightedSum / totalCensusPop;
                } 
                else if (k.startsWith('Male_Age_') && k.endsWith('_Ratio')) {
                    let weightedSum = 0;
                    selectedItems.forEach(item => {
                        weightedSum += (item[k] || 0) * item.Male_Population;
                    });
                    synthetic[k] = totalMalePop > 0 ? weightedSum / totalMalePop : 0;
                }
                else if (k.startsWith('Female_Age_') && k.endsWith('_Ratio')) {
                    let weightedSum = 0;
                    selectedItems.forEach(item => {
                        weightedSum += (item[k] || 0) * item.Female_Population;
                    });
                    synthetic[k] = totalFemalePop > 0 ? weightedSum / totalFemalePop : 0;
                }
                else if (k.startsWith('Disability_') && k.endsWith('_Ratio')) {
                    let weightedSum = 0;
                    selectedItems.forEach((item, idx) => {
                        weightedSum += (item[k] || 0) * itemDenoms[idx].both;
                    });
                    synthetic[k] = totalDenomBoth > 0 ? weightedSum / totalDenomBoth : 0;
                }
                else if (k.startsWith('Male_Disability_') && k.endsWith('_Ratio')) {
                    let weightedSum = 0;
                    selectedItems.forEach((item, idx) => {
                        weightedSum += (item[k] || 0) * itemDenoms[idx].male;
                    });
                    synthetic[k] = totalDenomMale > 0 ? weightedSum / totalDenomMale : 0;
                }
                else if (k.startsWith('Female_Disability_') && k.endsWith('_Ratio')) {
                    let weightedSum = 0;
                    selectedItems.forEach((item, idx) => {
                        weightedSum += (item[k] || 0) * itemDenoms[idx].female;
                    });
                    synthetic[k] = totalDenomFemale > 0 ? weightedSum / totalDenomFemale : 0;
                }
            });
            
            return synthetic;
        }

        // Toggle Main Tabs
        function showMainTab(tabId) {
            document.querySelectorAll('.main-tab-btn').forEach(btn => btn.classList.remove('active'));
            
            if (tabId === 'single') document.getElementById('tabBtnSingle').classList.add('active');
            if (tabId === 'multi') document.getElementById('tabBtnMulti').classList.add('active');
            if (tabId === 'methodology') document.getElementById('tabBtnMethod').classList.add('active');
            if (tabId === 'privacy') document.getElementById('tabBtnPrivacy').classList.add('active');
            
            const container = document.getElementById('mainContainer');
            const sidebarSingle = document.getElementById('cardSingleSidebar');
            const sidebarMulti = document.getElementById('cardMultiSidebar');
            const placeholder = document.getElementById('placeholder');
            const dashboard = document.getElementById('dashboard');
            const methodologyTab = document.getElementById('methodologyTab');
            const privacyTab = document.getElementById('privacyTab');
            
            sidebarSingle.style.display = 'none';
            sidebarMulti.style.display = 'none';
            placeholder.style.display = 'none';
            dashboard.style.display = 'none';
            methodologyTab.style.display = 'none';
            privacyTab.style.display = 'none';
            container.classList.remove('full-width-layout');
            
            if (tabId === 'single') {
                activeMode = 'single';
                sidebarSingle.style.display = 'flex';
                selectedMunicipality = singleSelectedMun;
                
                if (selectedMunicipality) {
                    placeholder.style.display = 'none';
                    dashboard.style.display = 'flex';
                    calculateEstimates();
                } else {
                    placeholder.style.display = 'flex';
                    dashboard.style.display = 'none';
                }
            } 
            else if (tabId === 'multi') {
                activeMode = 'multi';
                sidebarMulti.style.display = 'flex';
                selectedMunicipality = multiSyntheticMun;
                
                if (selectedMunicipality) {
                    placeholder.style.display = 'none';
                    dashboard.style.display = 'flex';
                    calculateEstimates();
                } else {
                    placeholder.style.display = 'flex';
                    dashboard.style.display = 'none';
                }
            } 
            else if (tabId === 'methodology') {
                container.classList.add('full-width-layout');
                methodologyTab.style.display = 'flex';
            } 
            else if (tabId === 'privacy') {
                container.classList.add('full-width-layout');
                privacyTab.style.display = 'flex';
            }
        }

        // Calculate and Render Dashboard
        function calculateEstimates() {
            let pop = 10000;
            if (activeMode === 'single') {
                if (!selectedMunicipality) {
                    alert("Please select a valid Province and Municipality.");
                    return;
                }
                const countInput = document.getElementById('populationInput');
                pop = parseInt(countInput.value);
                if (isNaN(pop) || pop <= 0) {
                    pop = 10000;
                    countInput.value = 10000;
                }
                singleSelectedMun = selectedMunicipality;
            } else {
                const provSelect = document.getElementById('provinceSelectMulti');
                const prov = provSelect.value;
                if (!prov) {
                    alert("Please select a Province.");
                    return;
                }
                const checkboxes = document.querySelectorAll('#checkboxContainerMulti input[type="checkbox"]:checked');
                if (checkboxes.length === 0) {
                    document.getElementById('placeholder').style.display = 'flex';
                    document.getElementById('dashboard').style.display = 'none';
                    selectedMunicipality = null;
                    multiSyntheticMun = null;
                    return;
                }
                
                const countInput = document.getElementById('populationInputMulti');
                pop = parseInt(countInput.value);
                if (isNaN(pop) || pop <= 0) {
                    pop = 10000;
                    countInput.value = 10000;
                }
                
                selectedMunicipality = buildSyntheticMunicipality(prov, checkboxes);
                multiSyntheticMun = selectedMunicipality;
            }
            
            // Show Dashboard, Hide Placeholder
            document.getElementById('placeholder').style.display = 'none';
            document.getElementById('dashboard').style.display = 'flex';
            
            // Update KPIs
            const locText = `${selectedMunicipality.Municipality}, ${selectedMunicipality.Province}`;
            if (activeMode === 'single') {
                document.getElementById('kpiLocation').textContent = locText;
                document.getElementById('kpiLocation').style.fontSize = "1.25rem";
            } else {
                document.getElementById('kpiLocation').textContent = locText;
                if (selectedMunicipality.Municipality.length > 20) {
                    document.getElementById('kpiLocation').style.fontSize = "1.05rem";
                } else {
                    document.getElementById('kpiLocation').style.fontSize = "1.25rem";
                }
            }
            document.getElementById('kpiAffected').textContent = pop.toLocaleString();
            
            // Update Export Report Header Details
            document.getElementById('reportLocationLabel').textContent = locText;
            document.getElementById('reportDateLabel').textContent = "Generated on: " + new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
            
            // 1. Sex disaggregation calculations (Ensuring exact sum to pop)
            const maleRatio = selectedMunicipality.Male_Ratio;
            const femaleRatio = selectedMunicipality.Female_Ratio;
            const maleCount = Math.round(pop * maleRatio);
            const femaleCount = pop - maleCount;
            
            lastCalculation = {
                pop: pop,
                maleCount: maleCount,
                femaleCount: femaleCount,
                male_5_plus: 0,
                female_5_plus: 0,
                total_5_plus: 0,
                ageCounts: {
                    male: {},
                    female: {},
                    total: {}
                }
            };
            
            document.getElementById('maleRatio').textContent = (maleRatio * 100).toFixed(2) + "%";
            document.getElementById('maleCount').textContent = maleCount.toLocaleString();
            document.getElementById('femaleRatio').textContent = (femaleRatio * 100).toFixed(2) + "%";
            document.getElementById('femaleCount').textContent = femaleCount.toLocaleString();
            
            renderSexChart(maleCount, femaleCount);
            
            // 2. Age disaggregation calculations (separating Male and Female)
            let ageLabels = [];
            let maleRatiosArr = [];
            let femaleRatiosArr = [];
            let totalRatiosArr = [];
            let ageKeys = [];

            if (ageDisaggregationMode === 'alternative') {
                const getRatios = (sex) => {
                    const prefix = sex === 'Total' ? 'Age_' : `${sex}_Age_`;
                    return {
                        r_0_4: selectedMunicipality[`${prefix}0-4_Ratio`] || 0,
                        r_5_9: selectedMunicipality[`${prefix}5-9_Ratio`] || 0,
                        r_10_14: selectedMunicipality[`${prefix}10-14_Ratio`] || 0,
                        r_15_19: selectedMunicipality[`${prefix}15-19_Ratio`] || 0,
                        r_20_24: selectedMunicipality[`${prefix}20-24_Ratio`] || 0,
                        r_25_29: selectedMunicipality[`${prefix}25-29_Ratio`] || 0,
                        r_30_34: selectedMunicipality[`${prefix}30-34_Ratio`] || 0,
                        r_35_39: selectedMunicipality[`${prefix}35-39_Ratio`] || 0,
                        r_40_44: selectedMunicipality[`${prefix}40-44_Ratio`] || 0,
                        r_45_49: selectedMunicipality[`${prefix}45-49_Ratio`] || 0,
                        r_50_54: selectedMunicipality[`${prefix}50-54_Ratio`] || 0,
                        r_55_59: selectedMunicipality[`${prefix}55-59_Ratio`] || 0,
                        r_60_64: selectedMunicipality[`${prefix}60-64_Ratio`] || 0,
                        r_65_69: selectedMunicipality[`${prefix}65-69_Ratio`] || 0,
                        r_70_74: selectedMunicipality[`${prefix}70-74_Ratio`] || 0,
                        r_75_79: selectedMunicipality[`${prefix}75-79_Ratio`] || 0,
                        r_80plus: selectedMunicipality[`${prefix}80yearsandover_Ratio`] || 0
                    };
                };

                const m = getRatios('Male');
                const f = getRatios('Female');
                const t = getRatios('Total');

                maleRatiosArr = [
                    m.r_0_4,
                    m.r_5_9 + m.r_10_14 + 0.6 * m.r_15_19,
                    0.4 * m.r_15_19 + m.r_20_24 + m.r_25_29 + m.r_30_34 + m.r_35_39 + m.r_40_44 + m.r_45_49 + m.r_50_54 + m.r_55_59,
                    m.r_60_64 + m.r_65_69 + m.r_70_74 + m.r_75_79 + m.r_80plus
                ];

                femaleRatiosArr = [
                    f.r_0_4,
                    f.r_5_9 + f.r_10_14 + 0.6 * f.r_15_19,
                    0.4 * f.r_15_19 + f.r_20_24 + f.r_25_29 + f.r_30_34 + f.r_35_39 + f.r_40_44 + f.r_45_49 + f.r_50_54 + f.r_55_59,
                    f.r_60_64 + f.r_65_69 + f.r_70_74 + f.r_75_79 + f.r_80plus
                ];

                totalRatiosArr = [
                    t.r_0_4,
                    t.r_5_9 + t.r_10_14 + 0.6 * t.r_15_19,
                    0.4 * t.r_15_19 + t.r_20_24 + t.r_25_29 + t.r_30_34 + t.r_35_39 + t.r_40_44 + t.r_45_49 + t.r_50_54 + t.r_55_59,
                    t.r_60_64 + t.r_65_69 + t.r_70_74 + t.r_75_79 + t.r_80plus
                ];

                ageLabels = ['0 to 4', '5 to 17', '18 to 59', '60+'];
                ageKeys = ['0_to_4', '5_to_17', '18_to_59', '60_plus'];
            } else {
                ageKeys = Object.keys(selectedMunicipality)
                    .filter(k => k.startsWith('Age_') && k.endsWith('_Ratio'))
                    .sort((a, b) => {
                        const clean_a = a.replace('Age_Age_', '').replace('_Ratio', '').replace('Age_', '');
                        const clean_b = b.replace('Age_Age_', '').replace('_Ratio', '').replace('Age_', '');
                        if (clean_a.startsWith('80')) return 1;
                        if (clean_b.startsWith('80')) return -1;
                        const val_a = parseInt(clean_a.split('to')[0].split('-')[0]);
                        const val_b = parseInt(clean_b.split('to')[0].split('-')[0]);
                        return val_a - val_b;
                    });

                maleRatiosArr = ageKeys.map(k => {
                    const clean_age = k.replace('Age_', '').replace('_Ratio', '');
                    return selectedMunicipality[`Male_Age_${clean_age}_Ratio`] || 0.0;
                });
                femaleRatiosArr = ageKeys.map(k => {
                    const clean_age = k.replace('Age_', '').replace('_Ratio', '');
                    return selectedMunicipality[`Female_Age_${clean_age}_Ratio`] || 0.0;
                });
                totalRatiosArr = ageKeys.map(k => {
                    return selectedMunicipality[k] || 0.0;
                });

                ageKeys.forEach(k => {
                    let label = k.replace('Age_Age_', '').replace('_Ratio', '').replace('Age_', '');
                    label = label.replace('yearsoldandover', ' years and over').replace('yearsandover', ' years and over');
                    label = label.replace('-', ' to '); // Avoid dates in Excel
                    label = label.charAt(0).toUpperCase() + label.slice(1);
                    ageLabels.push(label);
                });
            }

            const ageTableBody = document.getElementById('ageTableBody');
            ageTableBody.innerHTML = '';

            const maleAgeCounts = [];
            const femaleAgeCounts = [];

            // Distribute male and female population counts separately
            const maleCountsArr = distributePopulation(maleCount, maleRatiosArr);
            const femaleCountsArr = distributePopulation(femaleCount, femaleRatiosArr);

            // Calculate 5+ population counts (excluding 0-4 group)
            const male_5_plus = maleCount - maleCountsArr[0];
            const female_5_plus = femaleCount - femaleCountsArr[0];
            const total_5_plus = pop - (maleCountsArr[0] + femaleCountsArr[0]);

            lastCalculation.male_5_plus = male_5_plus;
            lastCalculation.female_5_plus = female_5_plus;
            lastCalculation.total_5_plus = total_5_plus;

            // Save for export dynamically
            lastCalculation.ageKeys = ageKeys;
            lastCalculation.ageLabels = ageLabels;
            lastCalculation.ageRatios = {
                male: maleRatiosArr,
                female: femaleRatiosArr,
                total: totalRatiosArr
            };
            lastCalculation.ageCounts = {
                male: maleCountsArr,
                female: femaleCountsArr,
                total: maleCountsArr.map((m, i) => m + femaleCountsArr[i])
            };

            ageLabels.forEach((label, idx) => {
                const mRatio = maleRatiosArr[idx];
                const fRatio = femaleRatiosArr[idx];
                const tRatio = totalRatiosArr[idx];

                const mCount = maleCountsArr[idx];
                const fCount = femaleCountsArr[idx];
                const tCount = mCount + fCount;

                maleAgeCounts.push(mCount);
                femaleAgeCounts.push(fCount);

                // Add row to table
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-weight: 500;">${label}</td>
                    <td>${(mRatio * 100).toFixed(2)}%</td>
                    <td style="font-weight: 600; color: #2563eb;">${mCount.toLocaleString()}</td>
                    <td>${(fRatio * 100).toFixed(2)}%</td>
                    <td style="font-weight: 600; color: #c084fc;">${fCount.toLocaleString()}</td>
                    <td>${(tRatio * 100).toFixed(2)}%</td>
                    <td style="font-weight: 700; background-color: rgba(255,255,255,0.02);">${tCount.toLocaleString()}</td>
                `;
                ageTableBody.appendChild(tr);
            });
            
            renderAgeChart(ageLabels, maleAgeCounts, femaleAgeCounts);
            
            // 3. Disability/Difficulty calculations
            updateDisabilitySection(pop, maleCount, femaleCount);
        }

        // Render Sex Pie Chart
        function renderSexChart(male, female) {
            const ctx = document.getElementById('sexChart').getContext('2d');
            const isDark = !document.body.classList.contains('light-theme');
            
            if (sexChartObj) {
                sexChartObj.destroy();
            }
            
            sexChartObj = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Male', 'Female'],
                    datasets: [{
                        data: [male, female],
                        backgroundColor: ['#2563eb', '#c084fc'],
                        borderColor: isDark ? '#161c2d' : '#ffffff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: isDark ? '#f3f4f6' : '#111827'
                            }
                        }
                    },
                    cutout: '65%'
                }
            });
        }

        // Render Age Bar Chart
        function renderAgeChart(labels, maleData, femaleData) {
            const ctx = document.getElementById('ageChart').getContext('2d');
            const isDark = !document.body.classList.contains('light-theme');
            
            if (ageChartObj) {
                ageChartObj.destroy();
            }
            
            ageChartObj = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Male',
                            data: maleData,
                            backgroundColor: '#2563eb',
                            borderColor: isDark ? '#161c2d' : '#ffffff',
                            borderWidth: 1.5,
                            borderRadius: 4
                        },
                        {
                            label: 'Female',
                            data: femaleData,
                            backgroundColor: '#c084fc',
                            borderColor: isDark ? '#161c2d' : '#ffffff',
                            borderWidth: 1.5,
                            borderRadius: 4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: isDark ? '#f3f4f6' : '#111827'
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: isDark ? '#9ca3af' : '#4b5563',
                                font: {
                                    size: 10
                                }
                            }
                        },
                        y: {
                            grid: {
                                color: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)'
                            },
                            ticks: {
                                color: isDark ? '#9ca3af' : '#4b5563'
                            }
                        }
                    }
                }
            });
        }

        // Change disability severity tab
        function changeSeverityTab(severity) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            if (severity === 'All') document.getElementById('btnAll').classList.add('active');
            if (severity === 'Mild') document.getElementById('btnMild').classList.add('active');
            if (severity === 'Moderate') document.getElementById('btnModerate').classList.add('active');
            if (severity === 'Severe') document.getElementById('btnSevere').classList.add('active');
            
            currentSeverity = severity;
            
            if (selectedMunicipality) {
                const pop = lastCalculation.pop || 10000;
                const maleCount = lastCalculation.maleCount || 5000;
                const femaleCount = lastCalculation.femaleCount || 5000;
                updateDisabilitySection(pop, maleCount, femaleCount);
            }
        }

        // Update Functional Difficulty Section (based on active severity tab)
        function updateDisabilitySection(pop, maleCount, femaleCount) {
            if (!selectedMunicipality) return;
            
            const domains = ['Seeing', 'Hearing', 'Walking', 'Remembering', 'Self_Caring', 'Communicating'];
            const labels = ['Seeing', 'Hearing', 'Walking', 'Remembering', 'Self Caring', 'Communicating'];
            
            const tableBody = document.getElementById('disabilityTableBody');
            tableBody.innerHTML = '';
            
            const maleCounts = [];
            const femaleCounts = [];
            const totalCounts = [];
            
            const colors = ['#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#ec4899', '#38bdf8'];
            
            // Estimate total population with functional difficulty as the maximum domain difficulty count in All, 
            // since domains can overlap on individuals.
            let maxDifficulty = 0;
            domains.forEach(d => {
                const allRatio = selectedMunicipality[`Disability_${d}_All_Ratio`] || 0;
                const count = Math.round(pop * allRatio);
                if (count > maxDifficulty) maxDifficulty = count;
            });
            document.getElementById('kpiDisability').textContent = maxDifficulty.toLocaleString();

            domains.forEach((d, idx) => {
                const mRatio = selectedMunicipality[`Male_Disability_${d}_${currentSeverity}_Ratio`] || 0;
                const fRatio = selectedMunicipality[`Female_Disability_${d}_${currentSeverity}_Ratio`] || 0;
                const tRatio = selectedMunicipality[`Disability_${d}_${currentSeverity}_Ratio`] || 0;
                
                const mCount = Math.round(maleCount * mRatio);
                const fCount = Math.round(femaleCount * fRatio);
                const tCount = Math.round(pop * tRatio);
                
                maleCounts.push(mCount);
                femaleCounts.push(fCount);
                totalCounts.push(tCount);
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-weight: 500;">${labels[idx]}</td>
                    <td style="color: #2563eb;"><span style="font-weight: 600;">${mCount.toLocaleString()}</span> <span style="font-size: 0.75rem; opacity: 0.85;">(${(mRatio * 100).toFixed(2)}%)</span></td>
                    <td style="color: #c084fc;"><span style="font-weight: 600;">${fCount.toLocaleString()}</span> <span style="font-size: 0.75rem; opacity: 0.85;">(${(fRatio * 100).toFixed(2)}%)</span></td>
                    <td style="color:${colors[idx]}; background-color: rgba(255,255,255,0.02);"><span style="font-weight: 700;">${tCount.toLocaleString()}</span> <span style="font-size: 0.75rem; opacity: 0.85;">(${(tRatio * 100).toFixed(2)}%)</span></td>
                `;
                tableBody.appendChild(tr);
            });
            
            renderDisabilityChart(labels, maleCounts, femaleCounts);
        }

        // Render Disability Bar Chart
        function renderDisabilityChart(labels, maleData, femaleData) {
            const ctx = document.getElementById('disabilityChart').getContext('2d');
            const isDark = !document.body.classList.contains('light-theme');
            
            if (disabilityChartObj) {
                disabilityChartObj.destroy();
            }
            
            disabilityChartObj = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Male',
                            data: maleData,
                            backgroundColor: '#2563eb',
                            borderRadius: 4
                        },
                        {
                            label: 'Female',
                            data: femaleData,
                            backgroundColor: '#c084fc',
                            borderRadius: 4
                        }
                    ]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: isDark ? '#f3f4f6' : '#111827'
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)'
                            },
                            ticks: {
                                color: isDark ? '#9ca3af' : '#4b5563'
                            }
                        },
                        y: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: isDark ? '#9ca3af' : '#4b5563'
                            }
                        }
                    }
                }
            });
        }

        // Toggle Dark/Light Theme
        function toggleTheme() {
            const body = document.body;
            body.classList.toggle('light-theme');
            
            const isLight = body.classList.contains('light-theme');
            document.getElementById('themeToggleText').textContent = isLight ? "Dark Mode" : "Light Mode";
            
            // Redraw charts with correct color styles
            if (selectedMunicipality) {
                calculateEstimates();
            }
        }

        // Reset inputs
        function resetForm() {
            document.getElementById('provinceSelect').value = '';
            onProvinceChange();
            document.getElementById('populationInput').value = '10000';
        }

        // Export data to CSV
        function exportCSV() {
            if (!selectedMunicipality) return;
            
            const pop = lastCalculation.pop || 10000;
            const maleCount = lastCalculation.maleCount;
            const femaleCount = lastCalculation.femaleCount;
            
            let csv = "ACCORD SADD Estimator - Disaggregation Estimate Report\\n";
            csv += `Location,${selectedMunicipality.Municipality} (${selectedMunicipality.Province} Province)\\n`;
            csv += `Input Affected Population,${pop}\\n\\n`;
            
            csv += "CATEGORY,SUBCATEGORY,MALE RATIO,MALE EST,FEMALE RATIO,FEMALE EST,TOTAL RATIO,TOTAL EST\\n";
            
            // Sex Breakdown
            csv += `Sex,Breakdown,${selectedMunicipality.Male_Ratio},${maleCount},${selectedMunicipality.Female_Ratio},${femaleCount},1.0,${pop}\\n\\n`;
            
            // Age groups
            csv += "Age Groups\\n";
            lastCalculation.ageLabels.forEach((label, idx) => {
                const mRatio = lastCalculation.ageRatios.male[idx];
                const mCount = lastCalculation.ageCounts.male[idx];
                const fRatio = lastCalculation.ageRatios.female[idx];
                const fCount = lastCalculation.ageCounts.female[idx];
                const tRatio = lastCalculation.ageRatios.total[idx];
                const tCount = lastCalculation.ageCounts.total[idx];
                
                csv += `Age Group,${label},${mRatio},${mCount},${fRatio},${fCount},${tRatio},${tCount}\\n`;
            });
            csv += "\\n";
            
            // Disability
            csv += "Disability / Functional Difficulty (Aged 5 and over)\\n";
            const domains = ['Seeing', 'Hearing', 'Walking', 'Remembering', 'Self_Caring', 'Communicating'];
            const severities = ['Mild', 'Moderate', 'Severe', 'All'];
            
            domains.forEach(d => {
                severities.forEach(s => {
                    const mKey = `Male_Disability_${d}_${s}_Ratio`;
                    const fKey = `Female_Disability_${d}_${s}_Ratio`;
                    const tKey = `Disability_${d}_${s}_Ratio`;
                    
                    const mRatio = selectedMunicipality[mKey] || 0;
                    const fRatio = selectedMunicipality[fKey] || 0;
                    const tRatio = selectedMunicipality[tKey] || 0;
                    
                    const mCount = Math.round(maleCount * mRatio);
                    const fCount = Math.round(femaleCount * fRatio);
                    const tCount = Math.round(pop * tRatio);
                    
                    csv += `Disability (${d} - Severity: ${s}),Male / Female / Total,${mRatio},${mCount},${fRatio},${fCount},${tRatio},${tCount}\\n`;
                });
            });
            
            // Download file
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            const fileNameMun = selectedMunicipality.Municipality.replace(/[\s,()]+/g, "_");
            link.setAttribute("href", url);
            link.setAttribute("download", `ACCORD_SADD_Estimate_${fileNameMun}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function exportDashboardImage() {
            if (!selectedMunicipality) return;
            
            const dashboardElement = document.getElementById('dashboard');
            const fileNameMun = selectedMunicipality.Municipality.replace(/[\s,()]+/g, "_");
            
            // Temporary hide export buttons during image generation so they don't appear in the PNG
            const exportBtns = dashboardElement.querySelector('div[style*="align-self: flex-end"]');
            if (exportBtns) exportBtns.style.visibility = 'hidden';
            
            html2canvas(dashboardElement, {
                backgroundColor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                scale: 2, // Double resolution for clean, crisp text and charts
                logging: false,
                useCORS: true
            }).then(canvas => {
                if (exportBtns) exportBtns.style.visibility = 'visible';
                
                const link = document.createElement('a');
                link.download = `ACCORD_SADD_Dashboard_${fileNameMun}.png`;
                link.href = canvas.toDataURL('image/png');
                link.click();
            }).catch(err => {
                if (exportBtns) exportBtns.style.visibility = 'visible';
                console.error("Error generating image:", err);
                alert("Failed to export dashboard as image.");
            });
        }

        // Initialize on load
        window.onload = initializeApp;
    </script>
</body>
</html>
"""

print("Writing estimator_app.html...")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Interactive HTML application generated successfully at: {html_path}")

aspx_path = os.path.join(psa_dir, "estimator_app.aspx")
print("Writing estimator_app.aspx...")
with open(aspx_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"SharePoint ASPX application generated successfully at: {aspx_path}")
