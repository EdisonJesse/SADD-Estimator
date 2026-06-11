import json
import os

psa_dir = r"c:\AI Projects\Sarangani Earthquake\PSA"
json_path = os.path.join(psa_dir, "municipality_ratios.json")
html_path = os.path.join(psa_dir, "estimator_app.html")

print("Loading ratios JSON data...")
with open(json_path, 'r') as f:
    ratios_data = json.load(f)

print(f"Loaded {len(ratios_data)} municipalities.")

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
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            padding: 1.75rem;
            box-shadow: var(--card-shadow);
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
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
            height: 250px;
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
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-glass);
        }

        td {
            padding: 0.75rem 1rem;
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
    </style>
</head>
<body>
    <header>
        <div class="logo-container">
            <div class="logo-icon">AC</div>
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

    <div class="container">
        <!-- Control Card -->
        <div class="card">
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

            <button class="btn" onclick="calculateEstimates()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Calculate Estimates
            </button>
            <button class="btn btn-secondary" onclick="resetForm()">Reset</button>
        </div>

        <!-- Output Results Area -->
        <div class="results-container">
            <!-- Placeholder before selection -->
            <div id="placeholder" class="placeholder-card">
                <div class="placeholder-icon">📊</div>
                <h3>Estimator Dashboard</h3>
                <p>Select a Province and Municipality, then input the affected population to view estimated disaggregation.</p>
            </div>

            <!-- Dashboard Content (hidden initially) -->
            <div id="dashboard" style="display: none;" class="results-container">
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
                        <span class="kpi-label">Est. Disability Cases (Moderate/Severe)</span>
                        <span class="kpi-value" id="kpiDisability">542</span>
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
                        <div class="chart-box" style="height: 250px;">
                            <canvas id="disabilityChart"></canvas>
                        </div>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Difficulty Domain</th>
                                        <th>Male %</th>
                                        <th>Male Est.</th>
                                        <th>Female %</th>
                                        <th>Female Est.</th>
                                        <th>Total %</th>
                                        <th>Total Est.</th>
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
                <button class="btn" style="width: fit-content; align-self: flex-end;" onclick="exportCSV()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    Export Full Disaggregation Report (CSV)
                </button>
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

        // Track last calculation to align UI display with CSV exports exactly
        let lastCalculation = {
            pop: 0,
            maleCount: 0,
            femaleCount: 0,
            ageCounts: {
                male: {},
                female: {},
                total: {}
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
            
            provinces.forEach(prov => {
                const opt = document.createElement('option');
                opt.value = prov;
                opt.textContent = prov;
                provinceSelect.appendChild(opt);
            });
            
            // Set default to Sarangani and Alabel if present
            if (provinces.includes('Sarangani')) {
                provinceSelect.value = 'Sarangani';
                onProvinceChange();
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
                document.getElementById('placeholder').style.display = 'flex';
                document.getElementById('dashboard').style.display = 'none';
                return;
            }
            
            selectedMunicipality = MUNICIPALITY_DATA.find(item => item.Province === prov && item.Municipality === mun);
        }

        // Calculate and Render Dashboard
        function calculateEstimates() {
            if (!selectedMunicipality) {
                alert("Please select a valid Province and Municipality.");
                return;
            }
            
            const countInput = document.getElementById('populationInput');
            let pop = parseInt(countInput.value);
            if (isNaN(pop) || pop <= 0) {
                pop = 10000;
                countInput.value = 10000;
            }
            
            // Show Dashboard, Hide Placeholder
            document.getElementById('placeholder').style.display = 'none';
            document.getElementById('dashboard').style.display = 'flex';
            
            // Update KPIs
            document.getElementById('kpiLocation').textContent = `${selectedMunicipality.Municipality}, ${selectedMunicipality.Province}`;
            document.getElementById('kpiAffected').textContent = pop.toLocaleString();
            
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
            const ageKeys = Object.keys(selectedMunicipality)
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
                
            const ageTableBody = document.getElementById('ageTableBody');
            ageTableBody.innerHTML = '';
            
            const ageLabels = [];
            const maleAgeCounts = [];
            const femaleAgeCounts = [];
            
            const maleRatiosArr = ageKeys.map(k => {
                const clean_age = k.replace('Age_', '').replace('_Ratio', '');
                return selectedMunicipality[`Male_Age_${clean_age}_Ratio`] || 0.0;
            });
            const femaleRatiosArr = ageKeys.map(k => {
                const clean_age = k.replace('Age_', '').replace('_Ratio', '');
                return selectedMunicipality[`Female_Age_${clean_age}_Ratio`] || 0.0;
            });
            
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
            
            ageKeys.forEach((k, idx) => {
                let label = k.replace('Age_Age_', '').replace('_Ratio', '').replace('Age_', '');
                label = label.replace('to', '-').replace('yearsoldandover', ' years and over').replace('yearsandover', ' years and over');
                label = label.charAt(0).toUpperCase() + label.slice(1);
                label = label.replace(/(\d+)-(\d+)/, '$1 - $2');
                
                const clean_age = k.replace('Age_', '').replace('_Ratio', '');
                const mRatio = selectedMunicipality[`Male_Age_${clean_age}_Ratio`] || 0.0;
                const fRatio = selectedMunicipality[`Female_Age_${clean_age}_Ratio`] || 0.0;
                const tRatio = selectedMunicipality[k] || 0.0;
                
                const mCount = maleCountsArr[idx];
                const fCount = femaleCountsArr[idx];
                const tCount = mCount + fCount; // Exact sum of male and female counts
                
                // Track count for export consistency
                lastCalculation.ageCounts.male[k] = mCount;
                lastCalculation.ageCounts.female[k] = fCount;
                lastCalculation.ageCounts.total[k] = tCount;
                
                ageLabels.push(label);
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
            
            // Sum Moderate and Severe for the KPI
            // Approximate total disability cases as the maximum domain difficulty count in Moderate/Severe, 
            // since domains can overlap on individuals.
            let maxModSev = 0;
            domains.forEach(d => {
                const modRatio = selectedMunicipality[`Disability_${d}_Moderate_Ratio`] || 0;
                const sevRatio = selectedMunicipality[`Disability_${d}_Severe_Ratio`] || 0;
                const count = Math.round(pop * modRatio) + Math.round(pop * sevRatio);
                if (count > maxModSev) maxModSev = count;
            });
            document.getElementById('kpiDisability').textContent = maxModSev.toLocaleString();

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
                    <td>${(mRatio * 100).toFixed(3)}%</td>
                    <td style="font-weight: 600; color: #2563eb;">${mCount.toLocaleString()}</td>
                    <td>${(fRatio * 100).toFixed(3)}%</td>
                    <td style="font-weight: 600; color: #c084fc;">${fCount.toLocaleString()}</td>
                    <td>${(tRatio * 100).toFixed(3)}%</td>
                    <td style="font-weight: 700; color:${colors[idx]}; background-color: rgba(255,255,255,0.02);">${tCount.toLocaleString()}</td>
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
            Object.keys(selectedMunicipality)
                .filter(k => k.startsWith('Age_') && k.endsWith('_Ratio'))
                .sort((a, b) => {
                    const clean_a = a.replace('Age_Age_', '').replace('_Ratio', '').replace('Age_', '');
                    const clean_b = b.replace('Age_Age_', '').replace('_Ratio', '').replace('Age_', '');
                    if (clean_a.startsWith('80')) return 1;
                    if (clean_b.startsWith('80')) return -1;
                    const val_a = parseInt(clean_a.split('to')[0].split('-')[0]);
                    const val_b = parseInt(clean_b.split('to')[0].split('-')[0]);
                    return val_a - val_b;
                })
                .forEach(k => {
                    const clean_age = k.replace('Age_', '').replace('_Ratio', '');
                    const label = clean_age.replace('to', ' - ').replace('yearsoldandover', ' years and over').replace('yearsandover', ' years and over');
                    
                    const mRatio = selectedMunicipality[`Male_Age_${clean_age}_Ratio`] || 0.0;
                    const fRatio = selectedMunicipality[`Female_Age_${clean_age}_Ratio`] || 0.0;
                    const tRatio = selectedMunicipality[k] || 0.0;
                    
                    const mCount = lastCalculation.ageCounts.male[k];
                    const fCount = lastCalculation.ageCounts.female[k];
                    const tCount = lastCalculation.ageCounts.total[k];
                    
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
            link.setAttribute("href", url);
            link.setAttribute("download", `ACCORD_SADD_Estimate_${selectedMunicipality.Municipality}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
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
