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
            console.log('Loading reports for user:', userData.user_id);
            
            // Use relative URL to avoid CORS issues
            const response = await fetch(`/api/reports/${userData.user_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            console.log('Reports response status:', response.status);

            if (response.ok) {
                this.reports = await response.json();
                console.log('Reports loaded:', this.reports);
                this.renderReports();
            } else {
                console.error('Failed to load reports:', response.status);
                // Handle as empty list if there are no reports
                this.reports = [];
                this.renderReports();
            }
        } catch (error) {
            console.error('Error loading reports:', error);
            this.reports = [];
            this.renderReports();
        }
    }

    renderReports() {
    const reportsGrid = document.getElementById('reports-grid');
    
    // If there are no reports and no pets registered, create sample data for demonstration
    if (this.reports.length === 0) {
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        // Only show sample data if the user is logged in
        if (userData.user_id) {
            this.reports = this.generateSampleReports();
        }
    }
    
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

                ${report.conditions && Array.isArray(report.conditions) && report.conditions.length > 0 ? `
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

    generateSampleReports() {
        // Generate sample reports for demonstration
        return [
            {
                id: 'sample-1',
                report_type: 'health_summary',
                created_at: new Date().toISOString(),
                pet_name: 'Whiskers',
                pet_species: 'Cat',
                pet_breed: 'Persian',
                pet_weight: 5.2,
                pet_height: 25,
                health_metric: 7.5,
                conditions: ['Overweight']
            },
            {
                id: 'sample-2',
                report_type: 'health_summary',
                created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
                pet_name: 'Buddy',
                pet_species: 'Dog',
                pet_breed: 'Golden Retriever',
                pet_weight: 28.5,
                pet_height: 60,
                health_metric: 6.2,
                conditions: []
            }
        ];
    }

    // Generate HTML report inspired by Whiskers_health_report_2025-07-25.html
    generateReportHTML(report) {
        console.log('Generating HTML for report:', report);
        
        try {
            // Process report data from the backend
            const processedData = this.processReportData(report);
            console.log('Processed data:', processedData);
            
            // Helper for recommendations
            const recommendationsHTML = processedData.recommendations.map(rec => `
                <div class="recommendation-item">${rec}</div>
            `).join('');

            // Helper for metrics
            const metrics = processedData.metrics;
        const metricCards = `
            <div class="card">
                <h3>📊 Basic Information</h3>
                <div class="metric-label">Breed</div>
                <div class="metric-value">${report.pet_breed || 'Unknown'}</div>
                <div class="metric-label">Species</div>
                <div class="metric-value">${report.pet_species || 'Unknown'}</div>
                <div class="metric-label">Weight</div>
                <div class="metric-value">${report.pet_weight ? report.pet_weight + ' kg' : 'Not recorded'}</div>
                <div class="metric-label">Height</div>
                <div class="metric-value">${report.pet_height ? report.pet_height + ' cm' : 'Not recorded'}</div>
            </div>
            <div class="card">
                <h3>⚖️ Weight & Condition</h3>
                <div class="metric-label">Current Weight</div>
                <div class="metric-value">${report.pet_weight ? report.pet_weight + ' kg' : 'Not recorded'}</div>
                <div class="metric-label">Body Condition Score</div>
                <div class="metric-value">${report.health_metric || 'Not assessed'}</div>
                <div class="metric-label">BMI Status</div>
                <div class="status-badge ${metrics.bmi_status_class}">${metrics.bmi_status}</div>
            </div>
            <div class="card">
                <h3>🏥 Health Status</h3>
                <div class="metric-label">Overall Status</div>
                <div class="status-badge ${metrics.health_status_class}">${metrics.health_status}</div>
                <div class="metric-label">Medical Conditions</div>
                <div class="metric-value">${report.conditions ? 
                    (Array.isArray(report.conditions) ? report.conditions.length : 
                     report.conditions.split(',').filter(c => c.trim()).length) : 0}</div>
                <div class="metric-label">Report Type</div>
                <div class="metric-value">${(report.report_type || 'Health Summary').replace('_', ' ').toUpperCase()}</div>
            </div>
            <div class="card">
                <h3>📋 Report Summary</h3>
                <div class="metric-label">Medical Conditions</div>
                <div class="metric-value">${report.conditions ? 
                    (Array.isArray(report.conditions) ? report.conditions.join(', ') || 'None' : 
                     report.conditions || 'None') : 'None'}</div>
                <div class="metric-label">Generated</div>
                <div style="color: #10b981;">${new Date(report.created_at).toLocaleDateString()}</div>
            </div>
        `;

        // Helper for insights
        const insightsHTML = processedData.insights.map(i => `<li>${i}</li>`).join('');

        // Timeline (basic for now)
        const timelineHTML = `
            <div class="timeline-item low">
                <div class="timeline-icon">📋</div>
                <div class="timeline-content">
                    <h4>Health Report Generated</h4>
                    <div class="timeline-date">${new Date(report.created_at).toLocaleDateString()}</div>
                    <div class="timeline-description">Comprehensive health assessment completed for ${report.pet_name}</div>
                </div>
            </div>
        `;

        // Recommendations section
        const recommendationsSection = `
            <div class="recommendations">
                <h3>💡 Health Recommendations</h3>
                ${recommendationsHTML}
            </div>
        `;

        // Main HTML
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Report - ${report.pet_name}</title>
    <style>
        ${this.getReportCSS()}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="header">
            <h1>${report.pet_species === 'Cat' ? '🐱' : report.pet_species === 'Dog' ? '🐶' : '🐾'} ${report.pet_name}</h1>
            <div class="subtitle">Comprehensive Health Report</div>
            <div class="report-meta">
                <strong>Report Generated:</strong> ${new Date(report.created_at).toLocaleDateString()}<br>
                <strong>Pet Species:</strong> ${report.pet_species}<br>
                <strong>Pet Breed:</strong> ${report.pet_breed}
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
                    <h4>Report Date</h4>
                    <p>${new Date(report.created_at).toLocaleDateString()}</p>
                    <p>Pet: ${report.pet_name}</p>
                </div>
            </div>
            <div style="border-top: 1px solid #475569; padding-top: 20px; margin-top: 20px;">
                <p>&copy; 2025 PetCare Monitor - Professional Pet Health Management System</p>
            </div>
        </div>
    </div>
</body>
</html>
        `;
        } catch (error) {
            console.error('Error generating report HTML:', error);
            return `<html><body><h1>Error generating report</h1><p>${error.message}</p></body></html>`;
        }
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

    processReportData(report) {
        // Calculate BMI and health status based on weight and height
        const bmi = this.calculateBMI(report.pet_weight, report.pet_height);
        const bmiStatus = this.getBMIStatus(bmi, report.pet_species);
        
        // Generate recommendations based on available data
        const recommendations = this.generateRecommendations(report, bmi);
        
        // Generate insights based on the data
        const insights = this.generateInsights(report, bmi);
        
        return {
            metrics: {
                bmi: bmi,
                bmi_status: bmiStatus.status,
                bmi_status_class: bmiStatus.class,
                health_status: this.getOverallHealthStatus(report),
                health_status_class: this.getHealthStatusClass(report)
            },
            recommendations: recommendations,
            insights: insights
        };
    }

    calculateBMI(weight, height) {
        if (!weight || !height) return null;
        // BMI = weight(kg) / (height(m))^2
        const heightInMeters = height / 100;
        return (weight / (heightInMeters * heightInMeters)).toFixed(1);
    }

    getBMIStatus(bmi, species) {
        if (!bmi) return { status: 'Not calculated', class: 'status-fair' };
        
        const bmiValue = parseFloat(bmi);
        
        // Rangos aproximados para mascotas (pueden variar según especie y raza)
        if (species === 'Cat') {
            if (bmiValue < 3.5) return { status: 'Underweight', class: 'status-poor' };
            if (bmiValue <= 5.0) return { status: 'Ideal', class: 'status-excellent' };
            if (bmiValue <= 6.5) return { status: 'Overweight', class: 'status-fair' };
            return { status: 'Obese', class: 'status-poor' };
        } else {
            // Para perros y otras mascotas
            if (bmiValue < 4.0) return { status: 'Underweight', class: 'status-poor' };
            if (bmiValue <= 6.0) return { status: 'Ideal', class: 'status-excellent' };
            if (bmiValue <= 8.0) return { status: 'Overweight', class: 'status-fair' };
            return { status: 'Obese', class: 'status-poor' };
        }
    }

    getOverallHealthStatus(report) {
        // Handle conditions as either array or string
        let conditionsCount = 0;
        if (report.conditions) {
            if (Array.isArray(report.conditions)) {
                conditionsCount = report.conditions.length;
            } else if (typeof report.conditions === 'string') {
                conditionsCount = report.conditions.split(',').filter(c => c.trim()).length;
            }
        }
        
        const hasConditions = conditionsCount > 0;
        const bmi = this.calculateBMI(report.pet_weight, report.pet_height);
        const bmiStatus = this.getBMIStatus(bmi, report.pet_species);
        
        if (hasConditions && bmiStatus.class === 'status-poor') {
            return 'Needs Attention';
        } else if (hasConditions || bmiStatus.class === 'status-fair') {
            return 'Fair';
        } else if (bmiStatus.class === 'status-excellent') {
            return 'Excellent';
        } else {
            return 'Good';
        }
    }

    getHealthStatusClass(report) {
        const status = this.getOverallHealthStatus(report);
        switch(status) {
            case 'Excellent': return 'status-excellent';
            case 'Good': return 'status-good';
            case 'Fair': return 'status-fair';
            case 'Needs Attention': return 'status-poor';
            default: return 'status-fair';
        }
    }

    generateRecommendations(report, bmi) {
        const recommendations = [];
        const bmiStatus = this.getBMIStatus(bmi, report.pet_species);
        
        // Recomendaciones basadas en BMI
        if (bmiStatus.status === 'Overweight' || bmiStatus.status === 'Obese') {
            recommendations.push('⚠️ Pet is overweight - Implement weight management program');
            recommendations.push('🏃 Increase exercise and playtime activities');
            recommendations.push('🍽️ Reduce food portions and switch to weight management food');
        } else if (bmiStatus.status === 'Underweight') {
            recommendations.push('📈 Pet is underweight - Consult veterinarian for feeding plan');
            recommendations.push('🍽️ Consider increasing food portions with high-quality nutrition');
        }
        
        // Recomendaciones basadas en condiciones médicas
        let conditionsCount = 0;
        if (report.conditions) {
            if (Array.isArray(report.conditions)) {
                conditionsCount = report.conditions.length;
            } else if (typeof report.conditions === 'string') {
                conditionsCount = report.conditions.split(',').filter(c => c.trim()).length;
            }
        }
        
        if (conditionsCount > 0) {
            recommendations.push('🏥 Monitor existing medical conditions closely');
            recommendations.push('💊 Follow prescribed medication schedule');
        }
        
        // Recomendaciones generales
        recommendations.push('🗓️ Schedule regular veterinary checkups');
        recommendations.push('💉 Keep vaccination schedule up to date');
        recommendations.push('🎾 Maintain regular exercise routine');
        
        return recommendations;
    }

    generateInsights(report, bmi) {
        const insights = [];
        const bmiStatus = this.getBMIStatus(bmi, report.pet_species);
        
        if (bmi) {
            insights.push(`💡 Current BMI is ${bmi} - Status: ${bmiStatus.status}`);
        }
        
        // Handle conditions as either array or string
        let conditionsCount = 0;
        let conditionsArray = [];
        if (report.conditions) {
            if (Array.isArray(report.conditions)) {
                conditionsArray = report.conditions;
                conditionsCount = report.conditions.length;
            } else if (typeof report.conditions === 'string') {
                conditionsArray = report.conditions.split(',').map(c => c.trim()).filter(c => c);
                conditionsCount = conditionsArray.length;
            }
        }
        
        if (conditionsCount > 0) {
            insights.push(`🏥 Has ${conditionsCount} documented medical condition(s): ${conditionsArray.join(', ')}`);
        } else {
            insights.push('✅ No current medical conditions documented');
        }
        
        if (report.health_metric) {
            insights.push(`📊 Body condition metric: ${report.health_metric}`);
        }
        
        // Insight temporal
        const reportDate = new Date(report.created_at);
        const now = new Date();
        const daysSince = Math.floor((now - reportDate) / (1000 * 60 * 60 * 24));
        
        if (daysSince === 0) {
            insights.push('🆕 Report generated today - Most current health data');
        } else if (daysSince < 30) {
            insights.push(`📅 Report is ${daysSince} days old - Recent health data`);
        } else {
            insights.push(`⏰ Report is ${daysSince} days old - Consider generating updated report`);
        }
        
        return insights;
    }

    viewReport(reportId) {
        // Ensure we can match both string and numeric IDs
        const report = this.reports.find(r => r.id == reportId || r.id === reportId);
        if (!report) {
            console.error('Report not found for ID:', reportId, 'Available reports:', this.reports);
            this.showNotification('Report not found.', 'error');
            return;
        }
        
        console.log('Viewing report for:', report.pet_name, 'with ID:', reportId);
        
        // Crear y mostrar el modal del reporte con HTML estilizado
        const modal = document.createElement('div');
        modal.className = 'modal report-modal active';
        modal.innerHTML = `
            <div class="modal-content">
                <button class="close-btn">&times;</button>
                <iframe srcdoc='${this.generateReportHTML(report).replace(/'/g, "&#39;")}' style="
                    width: 100%;
                    height: 90vh;
                    border: none;
                    overflow: auto;
                    background: white;
                "></iframe>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Manejadores para cerrar el modal
        const closeBtn = modal.querySelector('.close-btn');
        closeBtn.addEventListener('click', () => { 
            modal.remove(); 
        });
        
        modal.addEventListener('click', (e) => { 
            if (e.target === modal) { 
                modal.remove(); 
            } 
        });
        
        // Cerrar con ESC
        const handleKeydown = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', handleKeydown);
            }
        };
        document.addEventListener('keydown', handleKeydown);
        
        this.showNotification(`Viewing report for ${report.pet_name}`, 'info');
    }

    async downloadReport(reportId) {
        // Generar y descargar el archivo HTML del reporte
        // Ensure we can match both string and numeric IDs
        const report = this.reports.find(r => r.id == reportId || r.id === reportId);
        if (!report) {
            console.error('Report not found for download with ID:', reportId, 'Available reports:', this.reports);
            this.showNotification('Report not found.', 'error');
            return;
        }
        
        console.log('Downloading report for:', report.pet_name, 'with ID:', reportId);
        
        const html = this.generateReportHTML(report);
        const blob = new Blob([html], { type: 'text/html' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Generar nombre de archivo descriptivo
        const petName = (report.pet_name || 'Pet').replace(/[^a-zA-Z0-9]/g, '_');
        const reportDate = new Date(report.created_at).toISOString().split('T')[0];
        a.download = `${petName}_health_report_${reportDate}.html`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Mostrar mensaje de éxito
        this.showNotification('Report downloaded successfully!', 'success');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#2563eb'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 10000;
            font-size: 14px;
            max-width: 300px;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize reports component
window.reportsComponent = new Reports();