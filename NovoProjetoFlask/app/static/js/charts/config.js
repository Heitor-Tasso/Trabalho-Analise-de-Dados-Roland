// static/js/charts/config.js
/**
 * Configuração central para todos os gráficos Highcharts
 */
const HighchartsConfig = {
    // Configuração base para todos os gráficos
    baseConfig: {
        lang: {
            thousandsSep: '.',
            decimalPoint: ',',
            months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            shortMonths: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            weekdays: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
            exportButtonTitle: "Exportar",
            printButtonTitle: "Imprimir",
            downloadPNG: 'Baixar imagem PNG',
            downloadJPEG: 'Baixar imagem JPEG',
            downloadPDF: 'Baixar documento PDF',
            downloadSVG: 'Baixar imagem SVG',
            downloadCSV: 'Baixar CSV',
            downloadXLS: 'Baixar XLS',
            viewFullscreen: 'Ver em tela cheia'
        },
        credits: {
            enabled: false
        },
        exporting: {
            buttons: {
                contextButton: {
                    menuItems: [
                        'viewFullscreen',
                        'separator',
                        'downloadPNG',
                        'downloadJPEG',
                        'downloadPDF',
                        'downloadSVG',
                        'separator',
                        'downloadCSV',
                        'downloadXLS'
                    ]
                }
            }
        },
        chart: {
            style: {
                fontFamily: "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
            },
            spacing: [10, 10, 15, 10], // [top, right, bottom, left]
            backgroundColor: '#ffffff',
            borderRadius: 0
        },
        title: {
            style: {
                fontSize: '16px',
                fontWeight: 'bold',
                color: '#0d6efd'
            },
            align: 'center'
        },
        xAxis: {
            title: {
                style: {
                    fontSize: '13px',
                    fontWeight: 'bold',
                    color: '#495057'
                }
            },
            labels: {
                style: {
                    fontSize: '12px',
                    color: '#6c757d'
                }
            },
            lineColor: '#dee2e6',
            tickColor: '#dee2e6'
        },
        yAxis: {
            title: {
                style: {
                    fontSize: '13px',
                    fontWeight: 'bold',
                    color: '#495057'
                }
            },
            labels: {
                style: {
                    fontSize: '12px',
                    color: '#6c757d'
                }
            },
            lineColor: '#dee2e6',
            tickColor: '#dee2e6',
            gridLineColor: '#f5f5f5'
        },
        legend: {
            itemStyle: {
                fontSize: '12px',
                fontWeight: 'normal',
                color: '#495057'
            }
        },
        tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderWidth: 1,
            borderRadius: 8,
            shadow: true,
            style: {
                fontSize: '12px',
                color: '#212529'
            }
        }
    },
    
    // Cores padrão
    defaultColors: [
        '#0d6efd', '#6c757d', '#198754', '#dc3545', '#ffc107', 
        '#0dcaf0', '#6610f2', '#fd7e14', '#20c997', '#d63384'
    ],
    
    // Cores para modo daltônico
    colorBlindColors: [
        '#0072B2', '#E69F00', '#56B4E9', '#009E73', 
        '#F0E442', '#D55E00', '#CC79A7', '#999999'
    ],
    
    // Configurações específicas por tipo de gráfico
    barChartConfig: {
        chart: {
            marginLeft: 180
        },
        yAxis: {
            type: 'category',
            title: {
                text: null
            }
        },
        xAxis: {
            min: 0,
            title: {
                text: 'Contagem'
            }
        },
        legend: {
            align: 'left',
            verticalAlign: 'middle',
            layout: 'vertical',
            x: -160,
            y: 0
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                },
                colorByPoint: true
            }
        }
    },
    
    // Inicialização
    init: function() {
        if (typeof Highcharts !== 'undefined') {
            Highcharts.setOptions(this.baseConfig);
            console.log("Highcharts: Configuração global aplicada");
        } else {
            console.warn("Highcharts não está disponível");
        }
    },
    
    // Aplicar modo daltônico
    setColorBlindMode: function(enabled) {
        if (typeof Highcharts === 'undefined') return;
        
        // Cores a serem usadas
        const colors = enabled ? this.colorBlindColors : this.defaultColors;
        
        // Atualizar configuração global
        Highcharts.setOptions({
            colors: colors
        });
        
        // Atualizar todos os gráficos existentes
        if (Highcharts.charts) {
            Highcharts.charts.forEach(chart => {
                if (chart) {
                    chart.update({
                        colors: colors
                    });
                }
            });
        }
        
        console.log(`Modo daltônico ${enabled ? 'ativado' : 'desativado'}`);
    }
};

// Aplicar configuração ao carregar
document.addEventListener('DOMContentLoaded', function() {
    HighchartsConfig.init();
});
