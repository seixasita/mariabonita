document.addEventListener("DOMContentLoaded", function () {
  // Configuração do DataTables
  const config = {
    paging: false,
    searching: false,
    info: false,
    order: [[1, 'desc']],
    language: {
      decimal: ",",
      thousands: ".",
      emptyTable: "Nenhum dado disponível",
      infoEmpty: "Nenhum registro",
      loadingRecords: "Carregando...",
      processing: "Processando...",
      zeroRecords: "Nenhum registro encontrado",
      lengthMenu: "Mostrar _MENU_ registros",
      info: "Mostrando de _START_ até _END_ de _TOTAL_ registros",
      infoFiltered: "(filtrado de _MAX_ registros no total)",
      search: "Buscar:",
      paginate: {
        first: "Primeiro",
        last: "Último",
        next: "Próximo",
        previous: "Anterior"
      }
    }
  };

  const tabelaCategorias = document.querySelector('#tabela-categorias');
  const tabelaTipos = document.querySelector('#tabela-tipos');

  // Evita reinicializar DataTable verificando se a tabela já tem a classe 'dataTable'
  if (tabelaCategorias && !tabelaCategorias.classList.contains('dataTable')) {
    new DataTable(tabelaCategorias, config);
  }

  if (tabelaTipos && !tabelaTipos.classList.contains('dataTable')) {
    new DataTable(tabelaTipos, config);
  }

  // GRÁFICOS GERENCIAIS
  const dadosCategoriaEl = document.getElementById('dadosCategoria');
  const dadosTipoEl = document.getElementById('dadosTipo');

  if (dadosCategoriaEl && dadosTipoEl) {
    try {
      const categorias = JSON.parse(dadosCategoriaEl.textContent);
      const tipos = JSON.parse(dadosTipoEl.textContent);

      const graficoCategoria = document.getElementById('graficoCategoria');
      const graficoTipo = document.getElementById('graficoTipo');

      if (graficoCategoria) {
        new Chart(graficoCategoria, {
          type: 'pie',
          data: {
            labels: Object.keys(categorias),
            datasets: [{
              label: 'Custos por Categoria',
              data: Object.values(categorias),
              backgroundColor: [
                '#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8',
                '#6610f2', '#e83e8c', '#fd7e14', '#6c757d'
              ]
            }]
          },
          options: {
            plugins: {
              legend: {
                position: 'bottom'
              },
              title: {
                display: true,
                text: 'Distribuição dos Custos por Categoria',
                font: {
                  size: 18
                }
              }
            }
          }
        });
      }

      if (graficoTipo) {
        new Chart(graficoTipo, {
          type: 'bar',
          data: {
            labels: Object.keys(tipos),
            datasets: [{
              label: 'Custos por Tipo',
              data: Object.values(tipos),
              backgroundColor: '#6c757d'
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            },
            plugins: {
              legend: {
                display: false
              },
              title: {
                display: true,
                text: 'Totais por Tipo de Custo',
                font: {
                  size: 18
                }
              }
            }
          }
        });
      }
    } catch (error) {
      console.error("Erro ao carregar gráficos:", error);
    }
  }
});
