$(document).ready(function() {

    var bench_names = ["startup", "compiler", "compress", "crypto", "derby", "mpegaudio", "scimark", "serial", "spec_sunflow", "xml"];

    var specjvm_bench = []

    //get all the benchmark values by their name
    for(i = 0; i < bench_names.length; i++){
        specjvm_bench.push($('#'+bench_names[i]).text());
    }

    var trace1 = {
      x: bench_names,
      y: specjvm_bench,
      name: 'Latest build',
      type: 'bar'
    };
    var trace2 = {
      x: bench_names,
      y: [1, 0.5, 3, 2, 5, 4, 7, 6, 8, 9],
      name: 'Previous good build',
      type: 'bar'
    };

    var data = [trace1, trace2];
    var layout = {
      title: 'SPECjvm benchmarks',
      xaxis: {
        title: 'SPECjvm benchmarks',
        titlefont: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
      yaxis: {
        title: 'Ops/m',
        titlefont: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
      barmode: 'group'
    };

    TESTER = document.getElementById('tester');
    Plotly.plot( TESTER, data, layout);

 });