// static/js/charts/formatter.js
/**
 * Formatador de gráficos para padronização visual
 */
const ChartFormatter = {
    /**
     * Padroniza todos os gráficos carregados
     */
    standardizeAllCharts: function() {
        console.log("Padronizando todos os gráficos");
        
        if (!Highcharts.charts || Highcharts.charts.length === 0) {
            console.warn("Nenhum gráfico encontrado para padronização");
            return;
        }
        
        Highcharts.charts.forEach(chart => {
            if (!chart) return;
            
            this.formatChart(chart);
        });
    },
    
    /**
     * Formata um gráfico específico
     */
    formatChart: function(chart) {
        const chartId = chart.renderTo.id;
        const chartType = chart.options.chart.type;
        console.log(`Formatando gráfico ${chartId} do tipo ${chartType}`);
        
        try {
            // Aplicar os diferentes formatadores
            this.formatTitles(chart);
            this.formatAxis(chart, chartType);
            this.formatLegend(chart, chartType);
            this.ensureLegendVisibility(chart);
            this.addRestoreButton(chart);
            
            // Redesenhar o gráfico
            chart.redraw();
        } catch (error) {
            console.error(`Erro ao formatar gráfico ${chartId}:`, error);
        }
    },
    
    /**
     * Formata títulos do gráfico
     */
    formatTitles: function(chart) {
        if (chart.title) {
            chart.title.update({
                align: 'center',
                margin: 20,
                style: {
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: '#0d6efd'
                }
            }, false);
        }
    },
    
    /**
     * Formata eixos do gráfico de acordo com o tipo
     */
    formatAxis: function(chart, chartType) {
        // Configuração de eixos para gráficos de barra horizontal
        if (chartType === 'bar') {
            // Ajustar eixo Y (categorias)
            if (chart.yAxis && chart.yAxis[0]) {
                chart.yAxis[0].update({
                    type: 'category',
                    labels: {
                        style: {
                            fontSize: '12px',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            overflow: 'hidden',
                            width: '150px'
                        }
                    }
                }, false);
            }
            
            // Ajustar eixo X (valores)
            if (chart.xAxis && chart.xAxis[0]) {
                chart.xAxis[0].update({
                    min: 0,
                    title: {
                        text: 'Contagem',
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold'
                        }
                    }
                }, false);
            }
        } 
        // Configuração para gráficos de coluna vertical
        else if (chartType === 'column') {
            // Ajustar eixo X (categorias)
            if (chart.xAxis && chart.xAxis[0]) {
                const categories = chart.xAxis[0].categories || [];
                const shouldRotateLabels = categories.length > 5;
                
                chart.xAxis[0].update({
                    labels: {
                        rotation: shouldRotateLabels ? -45 : 0,
                        style: {
                            fontSize: '12px'
                        }
                    }
                }, false);
            }
            
            // Ajustar eixo Y (valores)
            if (chart.yAxis && chart.yAxis[0]) {
                chart.yAxis[0].update({
                    title: {
                        text: 'Contagem',
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold'
                        }
                    }
                }, false);
            }
        }
    },
    
    /**
     * Formata legenda de acordo com o tipo de gráfico
     */
    formatLegend: function(chart, chartType) {
        if (!chart.legend) return;
        
        // Configurações comuns para legendas
        const legendConfig = {
            enabled: true,
            itemStyle: {
                fontSize: '12px',
                fontWeight: 'normal',
                color: '#495057'
            },
            itemHoverStyle: {
                color: '#0d6efd'
            }
        };
        
        // Configurações específicas por tipo
        if (chartType === 'bar') {
            // Legenda vertical para gráficos de barra horizontal
            Object.assign(legendConfig, {
                align: 'left',
                verticalAlign: 'middle',
                layout: 'vertical',
                x: -160,
                y: 0,
                width: 140,
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                shadow: true
            });
        } else if (chartType === 'pie') {
            // Legenda para gráficos de pizza
            Object.assign(legendConfig, {
                align: 'center',
                verticalAlign: 'bottom',
                layout: 'horizontal'
            });
        } else {
            // Legenda padrão para outros tipos
            Object.assign(legendConfig, {
                align: 'center',
                verticalAlign: 'bottom',
                layout: 'horizontal'
            });
        }
        
        // Atualizar legenda
        chart.legend.update(legendConfig, false);
    },
    
    /**
     * Garante que a legenda esteja sempre visível
     */
    ensureLegendVisibility: function(chart) {
        if (!chart.legend) return;
        
        // Função para verificar visibilidade
        const checkLegendVisibility = () => {
            const legendGroup = chart.legend.group;
            if (legendGroup) {
                legendGroup.attr({
                    visibility: 'visible',
                    opacity: 1
                });
            }
            
            // Aplicar visibilidade via DOM
            const chartContainer = document.getElementById(chart.renderTo.id);
            if (chartContainer) {
                const legendElements = chartContainer.querySelectorAll('.highcharts-legend');
                legendElements.forEach(el => {
                    el.style.visibility = 'visible';
                    el.style.opacity = '1';
                    el.style.display = 'block';
                });
            }
        };
        
        // Verificar imediatamente e após um curto atraso
        checkLegendVisibility();
        setTimeout(checkLegendVisibility, 200);
    },
    
    /**
     * Adiciona botão de restauração ao gráfico
     */
    addRestoreButton: function(chart) {
        const chartContainer = document.getElementById(chart.renderTo.id);
        if (!chartContainer || chartContainer._hasResetButton) return;
        
        // Criar botão
        const resetButton = document.createElement('button');
        resetButton.innerHTML = '<i class="fas fa-undo-alt"></i>';
        resetButton.className = 'btn btn-sm btn-outline-primary reset-chart-button';
        resetButton.title = 'Restaurar gráfico';
        resetButton.style.position = 'absolute';
        resetButton.style.right = '10px';
        resetButton.style.top = '10px';
        resetButton.style.zIndex = '200';
        resetButton.style.opacity = '0';
        resetButton.style.transition = 'opacity 0.3s';
        
        // Mostrar/ocultar botão com hover
        chartContainer.addEventListener('mouseenter', () => {
            resetButton.style.opacity = '1';
        });
        chartContainer.addEventListener('mouseleave', () => {
            resetButton.style.opacity = '0';
        });
        
        // Restaurar visualização
        resetButton.addEventListener('click', () => {
            chart.series.forEach(series => {
                series.points.forEach(point => {
                    point.setVisible(true, false);
                });
            });
            chart.redraw();
        });
        
        chartContainer.appendChild(resetButton);
        chartContainer._hasResetButton = true;
    },
    
    /**
     * Inicializa o formatador
     */
    init: function() {
        // Registrar listeners de eventos
        document.addEventListener('charts-loaded', () => {
            // Usar timeout para garantir que todos os gráficos estejam prontos
            setTimeout(() => this.standardizeAllCharts(), 100);
        });
        
        // Ajustar quando a janela for redimensionada
        window.addEventListener('resize', this.debounce(() => {
            this.standardizeAllCharts();
        }, 250));
        
        console.log("ChartFormatter inicializado");
    },
    
    /**
     * Utilitário para debounce de eventos
     */
    debounce: function(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
};

// Inicializar quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    ChartFormatter.init();
});