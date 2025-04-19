/**
 * chart-standardizer.js
 * Funções para padronizar elementos dos gráficos Highcharts
 */
/**
 * Função unificada para configurar legendas com comportamento correto
 */
function setupChartLegends() {
    console.log("Configurando legendas dos gráficos...");
    
    Highcharts.charts.forEach(chart => {
        if (!chart) return;
        
        const chartId = chart.renderTo.id;
        const chartType = chart.options.chart.type;
        const isHorizontalBar = chartType === 'bar';
        const isPieChart = chartType === 'pie';
        
        // Para gráficos que não são de pizza, configurar legendas individuais para cada barra
        if (!isPieChart) {
            // Aumentar margem esquerda para evitar sobreposição
            chart.update({
                chart: {
                    marginLeft: 180  // Mais espaço à esquerda
                }
            }, false);
            
            // Obter categorias e pontos
            let categories = [];
            if (isHorizontalBar && chart.yAxis && chart.yAxis[0]) {
                categories = chart.yAxis[0].categories || [];
            } else if (chart.xAxis && chart.xAxis[0]) {
                categories = chart.xAxis[0].categories || [];
            }
            
            // Se temos categorias, criar pontos individuais com legendas
            if (categories.length > 0 && chart.series && chart.series[0]) {
                // Preparar dados para incluir nome em cada ponto
                const points = chart.series[0].points || [];
                
                // Configurar legendas específicas para cada ponto
                chart.update({
                    legend: {
                        enabled: true,
                        align: 'left',
                        verticalAlign: 'middle',
                        layout: 'vertical',
                        x: -160,  // Posicionar mais à esquerda
                        y: 0,
                        width: 140,
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        borderWidth: 1,
                        shadow: true,
                        title: {
                            text: getLegendTitle(chartId),
                            style: {
                                fontWeight: 'bold',
                                color: '#0d6efd'
                            }
                        }
                    },
                    plotOptions: {
                        series: {
                            showInLegend: false,  // Desabilitar legenda da série
                            events: {
                                legendItemClick: function(e) {
                                    // Evitar comportamento padrão
                                    e.preventDefault();
                                    return false;
                                }
                            }
                        },
                        bar: {
                            dataLabels: {
                                enabled: true
                            },
                            colorByPoint: true
                        },
                        column: {
                            dataLabels: {
                                enabled: true
                            },
                            colorByPoint: true
                        }
                    }
                }, false);
                
                // Atualizar pontos individualmente
                points.forEach((point, i) => {
                    if (i < categories.length) {
                        point.update({
                            name: categories[i],
                            showInLegend: true,  // Mostrar ponto na legenda
                            legendIndex: i,      // Ordem na legenda
                            events: {
                                legendItemClick: function() {
                                    // Alternar visibilidade apenas deste ponto
                                    const visible = this.visible !== false;
                                    this.setVisible(!visible);
                                    return false;  // Evitar comportamento padrão
                                }
                            }
                        }, false);
                    }
                });
            }
        } else {
            // Configuração para gráficos de pizza
            chart.update({
                legend: {
                    enabled: true,
                    align: 'left',
                    verticalAlign: 'middle',
                    layout: 'vertical',
                    x: -160,
                    y: 0,
                    title: {
                        text: 'Categorias'
                    }
                },
                plotOptions: {
                    pie: {
                        showInLegend: true
                    }
                }
            }, false);
        }
        
        // Redesenhar o gráfico
        chart.redraw();
    });
}

function getLegendTitle(chartId) {
    // Função auxiliar para determinar título da legenda
    switch(chartId) {
        case 'chart-genero': return 'Gênero';
        case 'chart-curso': return 'Cursos';
        case 'chart-periodo': return 'Períodos';
        case 'chart-estado_civil': return 'Estado Civil';
        case 'chart-renda': return 'Faixas de Renda';
        default: return chartId.includes('cidade') ? 'Cidades' : 'Categorias';
    }
}


// Modificação na função standardizeChartElements para preservar a configuração de gráficos de barra horizontais

function standardizeChartElements() {
    console.log("Padronizando elementos dos gráficos...");
    
    Highcharts.charts.forEach(chart => {
        if (!chart) return;
        
        console.log(`Processando gráfico: ${chart.renderTo.id}`);
        
        // Identificar tipo de gráfico
        const chartType = chart.options.chart.type;
        const isHorizontalBar = chartType === 'bar';
        const isPieChart = chartType === 'pie';
        
        // Ajustar título principal
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
        
        // Para gráficos de barra horizontal, temos uma abordagem específica
        // para evitar sobrescrever as configurações necessárias
        if (isHorizontalBar) {
            // Aumentar margem esquerda para garantir espaço para labels
            // chart.update({
            //     chart: {
            //         marginLeft: 150  // Espaço para labels no eixo Y
            //     }
            // }, false);
            
            // Garantir que o eixo Y seja do tipo categoria
            if (chart.yAxis && chart.yAxis[0]) {
                chart.yAxis[0].update({
                    type: 'category',  // Forçar tipo categoria
                    labels: {
                        style: {
                            fontSize: '12px'
                        }
                    }
                }, false);
            }
            
            // Garantir que o eixo X comece em zero
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
            
            // Não aplicar mais alterações para barras horizontais
            // para evitar conflitos com a configuração específica
        } 
        // Para outros tipos de gráficos, manter o comportamento normal
        else if (!isPieChart) {
            // Ajustar eixo X
            if (chart.xAxis && chart.xAxis[0]) {
                const xAxis = chart.xAxis[0];
                
                // Verificar número de categorias para determinar rotação
                const categoriesCount = xAxis.categories ? xAxis.categories.length : 0;
                const shouldRotateLabels = categoriesCount > 5;
                
                // Ajustar labels do eixo X
                xAxis.update({
                    labels: {
                        style: {
                            fontSize: '12px',
                            color: '#6c757d'
                        },
                        rotation: shouldRotateLabels ? -45 : 0,
                        y: shouldRotateLabels ? 5 : 0
                    },
                    lineColor: '#dee2e6',
                    tickColor: '#dee2e6'
                }, false);
                
                // Garantir que título do eixo X esteja presente e formatado
                xAxis.update({
                    title: {
                        text: xAxis.options.title && xAxis.options.title.text ? xAxis.options.title.text : '',
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold',
                            color: '#495057'
                        },
                        margin: 10
                    }
                }, false);
            }
            
            // Ajustar eixo Y
            if (chart.yAxis && chart.yAxis[0]) {
                const yAxis = chart.yAxis[0];
                
                // Ajustar labels do eixo Y
                yAxis.update({
                    labels: {
                        style: {
                            fontSize: '12px',
                            color: '#6c757d'
                        },
                        x: -5
                    },
                    lineColor: '#dee2e6',
                    tickColor: '#dee2e6',
                    gridLineColor: '#f5f5f5'
                }, false);
                
                // Garantir que título do eixo Y esteja presente e formatado
                yAxis.update({
                    title: {
                        text: yAxis.options.title && yAxis.options.title.text ? yAxis.options.title.text : 'Contagem',
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold',
                            color: '#495057'
                        },
                        margin: 15
                    }
                }, false);
            }
        }
        
        // Ajustar legenda para todos os tipos de gráficos
        if (chart.legend) {
            const hasSeries = chart.series.length > 1 || isPieChart;
            
            chart.legend.update({
                enabled: hasSeries,
                align: 'center',
                verticalAlign: 'bottom',
                layout: 'horizontal',
                itemStyle: {
                    fontSize: '12px',
                    fontWeight: 'normal',
                    color: '#495057'
                },
                itemHoverStyle: {
                    color: '#0d6efd'
                },
                margin: 20,
                padding: 8,
                borderRadius: 5,
                backgroundColor: isPieChart ? 'rgba(255, 255, 255, 0.9)' : undefined
            }, false);
        }
        
        // Ajustar tooltips
        chart.tooltip.update({
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderWidth: 1,
            borderRadius: 8,
            borderColor: '#dee2e6',
            shadow: true,
            style: {
                fontSize: '12px',
                color: '#212529'
            }
        }, false);
        
        // Aplicar mudanças
        chart.redraw();
        console.log(`Gráfico padronizado: ${chart.renderTo.id}`);
    });
}

/**
 * Verifica e corrige sobreposição de labels nos eixos
 */
function fixLabelOverlap() {
    Highcharts.charts.forEach(chart => {
        if (!chart) return;
        
        const chartType = chart.options.chart.type;
        const isHorizontalBar = chartType === 'bar';
        const isPieChart = chartType === 'pie';
        
        // Não aplicar ajustes em gráficos de pizza
        if (isPieChart) return;
        
        // Verificar eixo X para gráficos que não são barras horizontais
        if (!isHorizontalBar && chart.xAxis && chart.xAxis[0] && chart.xAxis[0].categories) {
            const xAxis = chart.xAxis[0];
            const categoriesCount = xAxis.categories.length;
            
            // Se houver muitas categorias, ajustar a exibição
            if (categoriesCount > 10) {
                xAxis.update({
                    labels: {
                        rotation: -45,
                        step: Math.ceil(categoriesCount / 20) // Mostrar apenas alguns labels
                    }
                }, false);
            }
        }
        
        // Tratamento especial para gráficos de barra horizontal
        if (isHorizontalBar && chart.yAxis && chart.yAxis[0] && chart.yAxis[0].categories) {
            const yAxis = chart.yAxis[0];
            const categoriesCount = yAxis.categories.length;
            
            // Para barras horizontais com muitas categorias
            if (categoriesCount > 15) {
                // Aumentar altura do gráfico proporcionalmente
                const newHeight = 400 + (categoriesCount - 15) * 20;
                chart.update({
                    chart: {
                        height: Math.min(800, newHeight)  // Limitar a altura máxima
                    }
                }, false);
                
                // Ajustar o espaçamento entre as barras
                chart.update({
                    plotOptions: {
                        bar: {
                            pointPadding: 0.1,
                            groupPadding: 0.05
                        }
                    }
                }, false);
            }
            
            // Ajustar estilo das labels para melhorar legibilidade
            yAxis.update({
                labels: {
                    style: {
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        width: '100px'  // Limitar largura do texto
                    }
                }
            }, false);
        }
        
        chart.redraw();
    });
}

/**
 * Inicializa os ajustes de padronização após o carregamento dos gráficos
 */
function initChartStandardization() {
    console.log("Inicializando padronização de gráficos...");
    
    // Executar padronização imediatamente se os gráficos já estiverem carregados
    if (Highcharts.charts && Highcharts.charts.length > 0) {
        standardizeChartElements();
        // adjustSpecificCharts();
        fixLabelOverlap();
    }
    
    // Adicionar listener para evento de carregamento de gráficos
    document.addEventListener('charts-loaded', function() {
        setTimeout(function() {
            standardizeChartElements();
            // adjustSpecificCharts();
            fixLabelOverlap();
        }, 100);
    });
    
    // Ajustar quando a janela for redimensionada
    window.addEventListener('resize', function() {
        // Usar debounce para evitar múltiplas chamadas
        clearTimeout(window.resizeTimer);
        window.resizeTimer = setTimeout(function() {
            fixLabelOverlap();
        }, 250);
    });
}

// Função para aprimorar as legendas dos gráficos
// Adicionar ao arquivo chart-standardizer.js


// Correção para garantir que as legendas permaneçam visíveis
// Adicionar ao arquivo chart-standardizer.js

/**
 * Função para garantir que as legendas não desapareçam após o carregamento
 */
function fixPersistentLegends() {
    console.log("Aplicando correção para legendas persistentes...");
    
    // Iterar sobre todos os gráficos do Highcharts
    Highcharts.charts.forEach(chart => {
        if (!chart) return;
        
        const chartId = chart.renderTo.id;
        console.log(`Corrigindo legendas para o gráfico: ${chartId}`);
        
        // Se existe uma legenda
        if (chart.legend && chart.options.legend && chart.options.legend.enabled) {
            // Primeiro, garantir que a legenda esteja habilitada na configuração
            chart.update({
                legend: {
                    enabled: true,  // Garantir que está habilitada
                    floating: false, // Não permitir que "flutue" (o que pode causar desaparecimento)
                    // Definir posição fixa
                    align: 'left',
                    verticalAlign: 'middle',
                    layout: 'vertical',
                    x: 10,
                    y: 0,
                    // Garantir que tenha um fundo sólido
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    borderWidth: 1,
                    borderColor: '#E0E0E0',
                    shadow: true,
                    // Estilo que garante visibilidade
                    itemStyle: {
                        color: '#333333',
                        fontWeight: 'normal',
                        fontSize: '12px'
                    },
                    // Impedir que o usuário a desabilite
                    itemHoverStyle: {
                        color: '#000000'
                    },
                    navigation: {
                        activeColor: '#3E576F',
                        animation: false // Desativar animações que podem causar problemas
                    },
                    // Desabilitar eventos que podem afetar a visibilidade
                    events: {
                        hide: function(e) {
                            // Prevenir esconder a legenda
                            e.preventDefault();
                            return false;
                        }
                    }
                },
                plotOptions: {
                    series: {
                        events: {
                            legendItemClick: function(e) {
                                // Prevenir ações de clique que possam afetar a legenda
                                e.preventDefault();
                                return false;
                            }
                        },
                        showInLegend: true // Garantir que as séries apareçam na legenda
                    }
                }
            }, false); // false para não redesenhar ainda
            
            // Forçar a atualização e renderização da legenda
            chart.legend.update({}, false);
            
            // Atualizar a série principal para garantir que apareça na legenda
            if (chart.series && chart.series[0]) {
                chart.series[0].update({
                    showInLegend: true
                }, false);
            }
            
            // Redesenhar o gráfico com todas as atualizações
            chart.redraw();
            
            // Usar setTimeout para garantir que a legenda permaneça após carregamento completo
            setTimeout(function() {
                // Verificar se a legenda ainda está visível
                if (chart.legend && !chart.legend.display) {
                    console.log(`Forçando exibição da legenda para ${chartId}`);
                    
                    // Forçar exibição da legenda
                    chart.legend.render();
                    chart.legend.display = true;
                    
                    // Garantir que o grupo SVG da legenda esteja visível
                    const legendGroup = chart.legend.group;
                    if (legendGroup) {
                        legendGroup.attr({
                            visibility: 'visible',
                            opacity: 1
                        });
                    }
                }
            }, 500); // Verificar após 500ms
            
            // Verificar novamente após um tempo maior (caso algum script atrase)
            setTimeout(function() {
                if (chart.legend) {
                    // Forçar exibição da legenda novamente
                    chart.legend.render();
                    chart.legend.display = true;
                    
                    // Aplicar visibilidade através do DOM
                    const chartContainer = document.getElementById(chartId);
                    if (chartContainer) {
                        const legendElements = chartContainer.querySelectorAll('.highcharts-legend');
                        legendElements.forEach(el => {
                            el.style.visibility = 'visible';
                            el.style.opacity = '1';
                            el.style.display = 'block';
                        });
                    }
                }
            }, 1000); // Verificar após 1 segundo
        }
    });
}


// Função simplificada para garantir visibilidade das legendas
function ensureLegendVisibility() {
    // Tornar todas as legendas visíveis
    document.querySelectorAll('.highcharts-legend, .highcharts-legend-box, .highcharts-legend-item')
        .forEach(el => {
            console.log(`el -=> ${el}`);
            el.style.visibility = 'visible';
            el.style.opacity = '1';
            el.style.display = 'block';
        });
}

// 2. Por último, adicionar os event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Executar funções básicas se já temos gráficos
    if (Highcharts && Highcharts.charts && Highcharts.charts.length > 0) {
        // standardizeChartElements();
        fixLabelOverlap();
        // setupChartLegends();
        setTimeout(ensureLegendVisibility, 300);
    }
    
    // // Configurar para o evento charts-loaded
    document.addEventListener('charts-loaded', function() {
        setTimeout(function() {
            standardizeChartElements();
    //         fixLabelOverlap();
    //         setupChartLegends();
            setTimeout(ensureLegendVisibility, 300);
        }, 100);
    });
});

// Inicializar quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', initChartStandardization);
