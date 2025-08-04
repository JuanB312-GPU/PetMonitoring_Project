// Reports Component
class Reports {
    constructor() {
        this.reports = [];
        this.init();
    }

    init() {
        this.loadReports();
    }

    async loadReports() {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) return;

            const userData = JSON.parse(localStorage.getItem('userData'));
            // Fetch reports from the API
            const response =  await fetch(`http://127.0.0.1:8000/api/reports/${userData.user_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                this.reports = await response.json();
                this.renderReports();
            }
        } catch (error) {
            console.error('Error loading reports:', error);
        }
    }

    renderReports() {
    const reportsGrid = document.getElementById('reports-grid');
    if (this.reports.length === 0) {
        reportsGrid.innerHTML = `
            <div class="empty-state">
                <h3>No Reports Generated</h3>
                <p>Generate health reports from the My Pets section to see them here.</p>
            </div>
        `;
        return;
    }

    reportsGrid.innerHTML = this.reports.map(report => `
        <div class="report-card">
            <div class="report-header">
                <h3>${report.pet_name} - ${report.report_type.replace('_', ' ').toUpperCase()}</h3>
                <span class="report-date">${new Date(report.created_at).toLocaleDateString()}</span>
            </div>
            <div class="report-body">
                <p><strong>Species:</strong> ${report.pet_species}</p>
                <p><strong>Breed:</strong> ${report.pet_breed}</p>
                <p><strong>Weight:</strong> ${report.pet_weight} kg</p>
                <p><strong>Height:</strong> ${report.pet_height} cm</p>
                <p><strong>Health Metric:</strong> ${report.health_metric}</p>

                ${report.conditions && report.conditions.length > 0 ? `
                    <div class="pet-conditions">
                        <h4>Medical Conditions</h4>
                        <div class="conditions-list">
                            ${report.conditions.map(condition => `
                                <span class="condition-tag">${condition.replace('_', ' ').toUpperCase()}</span>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
            <div class="report-actions">
                <button class="btn btn-primary" onclick="window.reportsComponent.viewReport('${report.id}')">View Details</button>
                <button class="btn btn-secondary" onclick="window.reportsComponent.downloadReport('${report.id}')">Download</button>
            </div>
        </div>
    `).join('');
    }

    // Generate HTML report inspired by Whiskers_health_report_2025-07-25.html
    generateReportHTML(report) {
        // Helper for recommendations
        const recommendationsHTML = report.data.recommendations ? report.data.recommendations.map(rec => `
            <div class="recommendation-item">${rec}</div>
        `).join('') : '';

        // Helper for metrics
        const metrics = report.data.metrics || {};
        const metricCards = `
            <div class="card">
                <h3>📊 Basic Information</h3>
                <div class="metric-label">Breed</div>
                <div class="metric-value">${report.pet_breed || '-'}</div>
                <div class="metric-label">Age</div>
                <div class="metric-value">${metrics.age || '-'}</div>
                <div class="metric-label">Human Age Equivalent</div>
                <div class="metric-value">${metrics.human_age || '-'}</div>
            </div>
            <div class="card">
                <h3>⚖️ Weight & Condition</h3>
                <div class="metric-label">Current Weight</div>
                <div class="metric-value">${metrics.weight || '-'}</div>
                <div class="metric-label">Body Condition Score</div>
                <div class="metric-value">${metrics.bcs || '-'}</div>
                <div class="metric-label">Ideal Range</div>
                <div style="color: #64748b;">${metrics.ideal_weight_range || '-'}</div>
            </div>
            <div class="card">
                <h3>🏥 Health Status</h3>
                <div class="metric-label">Overall Status</div>
                <div class="status-badge status-fair">${metrics.status || '-'}</div>
                <div class="metric-label">Weight Trend</div>
                <div class="metric-value">${metrics.weight_trend || '-'}</div>
            </div>
            <div class="card">
                <h3>📋 Records Summary</h3>
                <div class="metric-label">Health Records</div>
                <div class="metric-value">${metrics.health_records || '0'}</div>
                <div class="metric-label">Activity Records</div>
                <div class="metric-value">${metrics.activity_records || '0'}</div>
                <div class="metric-label">Period Weight Change</div>
                <div style="color: #10b981;">${metrics.period_weight_change || '+0 kg'}</div>
            </div>
        `;

        // Helper for insights
        const insightsHTML = report.data.insights ? report.data.insights.map(i => `<li>${i}</li>`).join('') : '<li>No routine checkups recorded in this period</li>';

        // Timeline (if available)
        const timelineHTML = report.data.timeline ? report.data.timeline.map(item => `
            <div class="timeline-item ${item.severity || ''}">
                <div class="timeline-icon">${item.icon || ''}</div>
                <div class="timeline-content">
                    <h4>${item.title || ''}</h4>
                    <div class="timeline-date">${item.date || ''}</div>
                    <div class="timeline-description">${item.description || ''}</div>
                </div>
            </div>
        `).join('') : '';

        // Recommendations
        const recommendationsSection = recommendationsHTML ? `
            <div class="recommendations">
                <h3>💡 Health Recommendations</h3>
                ${recommendationsHTML}
            </div>
        ` : '';

        // Main HTML
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Report - ${report.pet_name}</title>
    <style>
        /* ...existing Whiskers_health_report_2025-07-25.html CSS... */
        ${this.getReportCSS()}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="header">
            <h1>${report.pet_species === 'cat' ? '🐱' : report.pet_species === 'dog' ? '🐶' : '🐾'} ${report.pet_name}</h1>
            <div class="subtitle">Comprehensive Health Report</div>
            <div class="report-meta">
                <strong>Report Period:</strong> ${metrics.period_start || '-'} - ${metrics.period_end || '-'}<br>
                <strong>Generated:</strong> ${new Date(report.created_at).toLocaleDateString()}<br>
                <strong>Total Events:</strong> ${metrics.total_events || '0'}
            </div>
        </div>
        <div class="content">
            <button class="print-btn" onclick="window.print()">🖨️ Print Report</button>
            <div class="overview-grid">
                ${metricCards}
            </div>
            <div class="insights">
                <h3>🔍 Key Insights</h3>
                <ul>
                    ${insightsHTML}
                </ul>
            </div>
            <div class="timeline">
                <h3>📅 Health Timeline</h3>
                ${timelineHTML}
            </div>
            ${recommendationsSection}
        </div>
        <div class="footer">
            <div class="footer-content">
                <div>
                    <h4>Report Details</h4>
                    <p>Generated by PetCare Monitor</p>
                    <p>Professional Pet Health Management</p>
                </div>
                <div>
                    <h4>Contact Information</h4>
                    <p>For questions about this report</p>
                    <p>Contact your veterinarian</p>
                </div>
                <div>
                    <h4>Data Period</h4>
                    <p>${metrics.period_start || '-'}</p>
                    <p>to ${metrics.period_end || '-'}</p>
                </div>
            </div>
            <div style="border-top: 1px solid #475569; padding-top: 20px; margin-top: 20px;">
                <p>&copy; 2024 PetCare Monitor - Professional Pet Health Management System</p>
            </div>
        </div>
    </div>
</body>
</html>
        `;
    }

    // Extract CSS from the Whiskers model (for brevity, you can paste the CSS here or load from a file)
    getReportCSS() {
        return `
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .report-container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 40px; text-align: center; position: relative; overflow: hidden; }
        .header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="30" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="70" r="1.5" fill="rgba(255,255,255,0.1)"/></svg>'); opacity: 0.3; }
        .header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 10px; position: relative; z-index: 1; }
        .header .subtitle { font-size: 1.2rem; opacity: 0.9; position: relative; z-index: 1; }
        .header .report-meta { margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; backdrop-filter: blur(10px); position: relative; z-index: 1; }
        .content { padding: 40px; }
        .overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-bottom: 40px; }
        .card { background: #f8fafc; border-radius: 15px; padding: 25px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
        .card h3 { color: #4f46e5; font-size: 1.3rem; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .metric-value { font-size: 2rem; font-weight: 700; color: #1e293b; margin: 10px 0; }
        .metric-label { color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .status-badge { display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .status-excellent { background: #dcfce7; color: #166534; }
        .status-good { background: #dbeafe; color: #1d4ed8; }
        .status-fair { background: #fef3c7; color: #d97706; }
        .status-poor { background: #fee2e2; color: #dc2626; }
        .timeline { margin: 40px 0; }
        .timeline-item { display: flex; margin-bottom: 20px; padding: 20px; background: white; border-radius: 12px; border-left: 4px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .timeline-item.critical { border-left-color: #dc2626; }
        .timeline-item.high { border-left-color: #ea580c; }
        .timeline-item.medium { border-left-color: #0ea5e9; }
        .timeline-item.low { border-left-color: #10b981; }
        .timeline-icon { font-size: 1.5rem; margin-right: 15px; min-width: 40px; }
        .timeline-content h4 { color: #1e293b; margin-bottom: 5px; }
        .timeline-date { color: #64748b; font-size: 0.9rem; margin-bottom: 8px; }
        .timeline-description { color: #475569; }
        .insights { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 15px; padding: 25px; margin: 30px 0; border: 1px solid #0ea5e9; }
        .insights h3 { color: #0c4a6e; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .insights ul { list-style: none; }
        .insights li { padding: 8px 0; padding-left: 25px; position: relative; }
        .insights li::before { content: '💡'; position: absolute; left: 0; }
        .weight-chart { background: white; border-radius: 15px; padding: 25px; margin: 30px 0; border: 1px solid #e2e8f0; }
        .chart-container { height: 300px; display: flex; align-items: end; justify-content: space-around; background: #f8fafc; border-radius: 10px; padding: 20px; margin-top: 20px; }
        .chart-bar { background: linear-gradient(to top, #4f46e5, #7c3aed); border-radius: 4px 4px 0 0; min-width: 40px; position: relative; color: white; font-size: 0.8rem; display: flex; align-items: end; justify-content: center; padding-bottom: 5px; }
        .recommendations { background: linear-gradient(135deg, #fef7cd 0%, #fde68a 100%); border-radius: 15px; padding: 25px; margin: 30px 0; border: 1px solid #f59e0b; }
        .recommendations h3 { color: #92400e; margin-bottom: 15px; }
        .recommendation-item { background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #f59e0b; }
        .footer { background: #1e293b; color: white; padding: 30px 40px; text-align: center; }
        .footer-content { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .footer h4 { color: #94a3b8; margin-bottom: 10px; }
        .print-btn { background: #4f46e5; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 1rem; margin: 20px; transition: background 0.2s ease; }
        .print-btn:hover { background: #3730a3; }
        @media print { body { background: white; padding: 0; } .report-container { box-shadow: none; } .print-btn { display: none; } }
        @media (max-width: 768px) { .content { padding: 20px; } .header { padding: 20px; } .overview-grid { grid-template-columns: 1fr; } }
        `;
    }

    viewReport(reportId) {
        const report = this.reports.find(r => r.id === reportId);
        // Fallback if not found
        if (!report) {
            alert('Report not found.');
            return;
        }
        // Create and show report modal with styled HTML
        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 1000px; padding:0; background:none; box-shadow:none;">
                <span class="close" style="position:absolute;top:10px;right:20px;font-size:2rem;cursor:pointer;z-index:10;">&times;</span>
                <iframe srcdoc='${this.generateReportHTML(report).replace(/'/g, "&#39;")}' style="width:100%;height:80vh;border:none;border-radius:20px;overflow:auto;background:white;"></iframe>
            </div>
        `;
        document.body.appendChild(modal);
        // Close modal handlers
        const closeBtn = modal.querySelector('.close');
        closeBtn.addEventListener('click', () => { modal.remove(); });
        modal.addEventListener('click', (e) => { if (e.target === modal) { modal.remove(); } });
    }

    async downloadReport(reportId) {
        // Instead of fetching a PDF, generate and download the HTML file
        const report = this.reports.find(r => r.id === reportId);
        if (!report) return;
        const html = this.generateReportHTML(report);
        const blob = new Blob([html], { type: 'text/html' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `health-report-${report.pet_name || reportId}.html`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
}

// Initialize reports component
window.reportsComponent = new Reports();