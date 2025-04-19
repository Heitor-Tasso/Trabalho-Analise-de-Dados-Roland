// Main JavaScript for FATEC Socioeconomic Analysis App

document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // File input validation
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const filePath = this.value;
            const allowedExtensions = /(\.xlsx|\.xls)$/i;
            
            if (!allowedExtensions.exec(filePath)) {
                alert('Por favor, selecione um arquivo Excel válido (.xlsx ou .xls)');
                this.value = '';
                return false;
            }
            
            // Show file name
            const fileName = this.files[0].name;
            const fileSize = Math.round(this.files[0].size / 1024); // KB
            
            // Display file info if we have a file info element
            const fileInfo = document.getElementById('file-info');
            if (fileInfo) {
                fileInfo.innerHTML = `
                    <div class="alert alert-info mt-2">
                        <i class="fas fa-file-excel me-2"></i>
                        <strong>${fileName}</strong> (${fileSize} KB)
                    </div>
                `;
            }
        });
    }

    // Confirmation for data clearing
    const clearDataForm = document.querySelector('form[action*="clear_data"]');
    if (clearDataForm) {
        clearDataForm.addEventListener('submit', function(e) {
            if (!confirm('Tem certeza que deseja limpar todos os dados processados? Esta ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            // Create a new bootstrap alert and close it
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize Highcharts theme
    initHighchartsTheme();
    
    // Apply colorblind mode if previously enabled
    if (isColorBlindModeEnabled()) {
        toggleColorBlindMode(true);
    }
    
    // Handle print media events
    window.addEventListener('beforeprint', preparePrint);
    window.addEventListener('afterprint', cleanupAfterPrint);
});

/**
 * Initialize Highcharts theme
 */
function initHighchartsTheme() {
    // Skip if Highcharts is not loaded
    if (typeof Highcharts === 'undefined') return;

    // Apply FATEC theme to all charts
    Highcharts.theme = {
        colors: ['#0d6efd', '#6c757d', '#198754', '#dc3545', '#ffc107', 
                '#0dcaf0', '#6610f2', '#fd7e14', '#20c997', '#d63384'],
        chart: {
            backgroundColor: '#ffffff',
            borderRadius: 8,
            style: {
                fontFamily: "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
            },
            spacing: [10, 10, 15, 10] // [top, right, bottom, left]
        },
        title: {
            style: {
                color: '#0d6efd',
                fontWeight: 'bold',
                fontSize: '16px'
            },
            margin: 20
        },
        subtitle: {
            style: {
                color: '#6c757d',
                fontSize: '13px'
            }
        },
        legend: {
            itemStyle: {
                fontWeight: 'normal',
                fontSize: '12px',
                color: '#495057'
            },
            itemHoverStyle: {
                color: '#0d6efd'
            }
        },
        xAxis: {
            labels: {
                style: {
                    color: '#6c757d',
                    fontSize: '12px'
                }
            },
            title: {
                style: {
                    color: '#495057',
                    fontSize: '13px',
                    fontWeight: 'bold'
                }
            },
            gridLineColor: '#e9ecef',
            lineColor: '#dee2e6',
            tickColor: '#dee2e6'
        },
        yAxis: {
            labels: {
                style: {
                    color: '#6c757d',
                    fontSize: '12px'
                }
            },
            title: {
                style: {
                    color: '#495057',
                    fontSize: '13px',
                    fontWeight: 'bold'
                }
            },
            gridLineColor: '#f5f5f5',
            lineColor: '#dee2e6',
            tickColor: '#dee2e6'
        },
        tooltip: {
            backgroundColor: 'rgba(247, 247, 247, 0.95)',
            borderWidth: 1,
            borderColor: '#e9ecef',
            shadow: true,
            style: {
                fontSize: '12px',
                color: '#212529'
            }
        },
        plotOptions: {
            series: {
                animation: {
                    duration: 1000
                }
            },
            bar: {
                borderRadius: 3,
                pointPadding: 0.15,
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    style: {
                        textOutline: 'none'
                    }
                }
            },
            column: {
                borderRadius: 3,
                pointPadding: 0.15,
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    style: {
                        textOutline: 'none'
                    }
                }
            },
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f}%',
                    style: {
                        textOutline: 'none'
                    }
                }
            }
        },
        credits: {
            enabled: false
        }
    };

    // Apply the theme
    Highcharts.setOptions(Highcharts.theme);
    console.log("Highcharts theme initialized");
}

/**
 * Export all charts as a zip archive
 */
window.exportAllCharts = function() {
    // Check if required libraries are loaded
    if (typeof JSZip === 'undefined' || typeof saveAs === 'undefined') {
        alert('Bibliotecas de exportação não estão disponíveis. Por favor, tente exportar os gráficos individualmente.');
        return;
    }

    // Show loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center bg-white bg-opacity-75';
    loadingIndicator.style.zIndex = '9999';
    loadingIndicator.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Preparando todos os gráficos para exportação...</p>
        </div>
    `;
    document.body.appendChild(loadingIndicator);

    // Create a new zip file
    const zip = new JSZip();
    const promises = [];
    const chartElements = document.querySelectorAll('[id^="chart-"]');
    
    // Process each chart
    chartElements.forEach((element, index) => {
        const chart = Highcharts.charts.find(c => c && c.renderTo.id === element.id);
        if (chart) {
            const deferred = $.Deferred();
            promises.push(deferred.promise());
            
            // Get chart name from id
            const chartName = element.id.replace('chart-', '');
            
            // Export chart as PNG
            try {
                // Get data URL for chart
                const imageData = chart.toDataURL('image/png');
                const base64Data = imageData.split(',')[1];
                
                // Add to zip
                zip.file(`${chartName}.png`, base64Data, { base64: true });
                deferred.resolve();
            } catch (error) {
                console.error(`Error exporting chart ${chartName}:`, error);
                deferred.resolve(); // Resolve anyway to continue with other charts
            }
        }
    });
    
    // When all charts are processed
    $.when.apply($, promises).done(function() {
        // Generate the zip file
        zip.generateAsync({ type: 'blob' }).then(function(content) {
            // Download the zip
            saveAs(content, 'fatec-socioeconomico-graficos.zip');
            
            // Remove loading indicator
            document.body.removeChild(loadingIndicator);
        }).catch(function(error) {
            console.error('Error generating zip:', error);
            alert('Ocorreu um erro ao gerar o arquivo ZIP.');
            document.body.removeChild(loadingIndicator);
        });
    });
};

/**
 * Print all charts
 */
window.printAllCharts = function() {
    preparePrint();
    window.print();
};

/**
 * Prepare page for printing
 */
function preparePrint() {
    // Add print title
    const originalTitle = document.title;
    document.title = 'FATEC - Análise Socioeconômica - ' + new Date().toLocaleDateString();
    document._originalTitle = originalTitle;
    
    // Add print styles
    const style = document.createElement('style');
    style.id = 'print-styles';
    style.innerHTML = `
        @media print {
            body * {
                visibility: hidden;
            }
            .chart-card, .chart-card * {
                visibility: visible;
            }
            .chart-card {
                break-inside: avoid;
                page-break-inside: avoid;
                position: relative;
                left: 0;
                top: 0;
                width: 100%;
                margin: 30px 0;
                border: none;
                box-shadow: none;
            }
            header, footer, .nav-sections, .card-header, form, button {
                display: none !important;
            }
            .container {
                width: 100% !important;
                max-width: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            h2 {
                font-size: 18px !important;
                margin-top: 15px !important;
            }
            .highcharts-subtitle, .highcharts-data-labels text {
                font-size: 11px !important;
            }
            .highcharts-data-labels text, .highcharts-axis-labels text {
                font-size: 9px !important;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Resize charts for better printing
    Highcharts.charts.forEach(chart => {
        if (chart) {
            chart._originalWidth = chart.chartWidth;
            chart._originalHeight = chart.chartHeight;
            chart.setSize(800, 450, false);
        }
    });
}

/**
 * Clean up after printing
 */
function cleanupAfterPrint() {
    // Restore title
    if (document._originalTitle) {
        document.title = document._originalTitle;
        delete document._originalTitle;
    }
    
    // Remove print styles
    const printStyles = document.getElementById('print-styles');
    if (printStyles) {
        document.head.removeChild(printStyles);
    }
    
    // Restore chart sizes
    // Highcharts.charts.forEach(chart => {
    //     if (chart && chart._originalWidth && chart._originalHeight) {
    //         chart.setSize(chart._originalWidth, chart._originalHeight, false);
    //         delete chart._originalWidth;
    //         delete chart._originalHeight;
    //     }
    // });
}

/**
 * Toggle colorblind mode
 */
window.toggleColorBlindMode = function(enable) {
    // Color-blind friendly palette
    const colorBlindPalette = [
        '#0072B2', '#E69F00', '#56B4E9', '#009E73', 
        '#F0E442', '#D55E00', '#CC79A7', '#999999'
    ];
    
    // Standard palette
    const standardPalette = [
        '#0d6efd', '#6c757d', '#198754', '#dc3545', 
        '#ffc107', '#0dcaf0', '#6610f2', '#fd7e14'
    ];
    
    // Toggle body class for CSS rules
    if (enable) {
        document.body.classList.add('colorblind-mode');
    } else {
        document.body.classList.remove('colorblind-mode');
    }
    
    // Set color palette based on mode
    const colors = enable ? colorBlindPalette : standardPalette;
    
    // Update all charts
    Highcharts.charts.forEach(chart => {
        if (chart) {
            chart.update({
                colors: colors
            });
        }
    });
    
    // Store preference
    localStorage.setItem('colorBlindMode', enable ? 'true' : 'false');
    
    // Update UI
    const toggleButton = document.getElementById('toggleColorBlind');
    if (toggleButton) {
        toggleButton.innerHTML = enable ? 
            '<i class="fas fa-eye-slash"></i> Modo Normal' : 
            '<i class="fas fa-eye"></i> Modo Daltônico';
    }
};

/**
 * Check if color-blind mode is enabled
 */
window.isColorBlindModeEnabled = function() {
    return localStorage.getItem('colorBlindMode') === 'true';
};

/**
 * Utility function to format numbers with thousands separator
 */
function formatNumber(number) {
    return new Intl.NumberFormat('pt-BR').format(number);
}

// Adição de funcionalidades interativas para legendas
// Adicionar ao final do arquivo main.js

/**
 * Melhora a interatividade das legendas dos gráficos Highcharts
 * Adiciona efeitos de hover e tooltips informativos
 */
function enhanceLegendInteractivity() {
    // Executar após pequeno delay para garantir que os gráficos estão renderizados
    setTimeout(() => {
        // Iterar sobre todos os gráficos Highcharts
        Highcharts.charts.forEach(chart => {
            if (!chart) return;
            
            const chartId = chart.renderTo.id;
            const chartEl = document.getElementById(chartId);
            
            if (!chartEl) return;
            
            // console.log(chartEl);
            // getChartHeight()
            // Encontrar os elementos de legenda dentro do SVG
            const legendItems = chartEl.querySelectorAll('.highcharts-legend-item');
            
            // Adicionar tooltips informativos e efeitos visuais aos itens da legenda
            legendItems.forEach(item => {
                // Adicionar título para mostrar tooltip nativo do navegador como fallback
                const textEl = item.querySelector('text');
                if (textEl) {
                    const categoryName = textEl.textContent;
                    textEl.setAttribute('title', `Categoria: ${categoryName}`);
                    
                    // Adicionar evento de mouseover para destacar a barra/coluna correspondente
                    item.addEventListener('mouseover', function() {
                        // Encontrar o ponto correspondente na série
                        const pointIndex = Array.from(legendItems).indexOf(item);
                        if (chart.series[0] && chart.series[0].points && chart.series[0].points[pointIndex]) {
                            const point = chart.series[0].points[pointIndex];
                            
                            // Destacar o ponto
                            point.setState('hover');
                            
                            // Adicionar classe CSS para estilização
                            textEl.classList.add('highcharts-legend-item-active');
                        }
                    });
                    
                    // Adicionar evento de mouseout para remover o destaque
                    item.addEventListener('mouseout', function() {
                        // Remover destaque de todos os pontos
                        if (chart.series[0]) {
                            chart.series[0].points.forEach(p => p.setState(''));
                        }
                        
                        // Remover classe CSS
                        textEl.classList.remove('highcharts-legend-item-active');
                    });
                }
            });
            
            // Para o gráfico de distribuição por gênero, adicionar informações mais detalhadas
            if (chartId === 'chart-genero') {
                const legendTitle = chartEl.querySelector('.highcharts-legend-title text');
                if (legendTitle) {
                    legendTitle.setAttribute('title', 'Distribuição dos estudantes por gênero');
                }
            }
            
            // Para o gráfico de distribuição por curso, adicionar informações mais detalhadas
            if (chartId === 'chart-curso') {
                const legendTitle = chartEl.querySelector('.highcharts-legend-title text');
                if (legendTitle) {
                    legendTitle.setAttribute('title', 'Distribuição dos estudantes por curso');
                }
            }
        });
        
        console.log("Interatividade das legendas aprimorada");
    }, 1000);
}

// Adicionar ao evento DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Código existente...
    
    // Adicionar listener para o evento de carregamento de gráficos
    document.addEventListener('charts-loaded', function() {
        // Chamar função após as outras padronizações
        setTimeout(enhanceLegendInteractivity, 300);
    });
});

// Função para depuração e correção dinâmica de legendas
// Adicionar ao arquivo main.js
// Remover:
// - A função debugAndFixLegends()
// - O código que adiciona o botão de depuração

// Remover o observer duplicado e substitui-lo por uma versão mais simples:



// Log application start
console.log("FATEC Socioeconomic Analysis App initialized");