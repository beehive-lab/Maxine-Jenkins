$(document).ready(function() {

    draw_specjvm();
    draw_dacapo();

 });

 function draw_specjvm(){

    var bench_names = ["startup", "compiler", "compress", "crypto", "derby", "mpegaudio", "scimark", "serial", "spec_sunflow", "xml"];

    var specjvm_bench = []
    var specjvm_bench1 = []

    var build_no1 = $('#build1').text()
    var build_no2 = $('#build2').text()

    //get all the benchmark values by their name
    for(i = 0; i < bench_names.length; i++){
        specjvm_bench.push($('#'+bench_names[i]).text());
        specjvm_bench1.push($('#'+bench_names[i]+'1').text());
    }

    var trace1 = {
      x: bench_names,
      y: specjvm_bench,
      name: 'Build '+build_no1,
      type: 'bar'
    };
    var trace2 = {
      x: bench_names,
      y: specjvm_bench1,
      name: 'Build '+build_no2,
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
 }

  function draw_dacapo(){

    var bench_names = ["avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan"];

    var dacapo_bench = []
    var dacapo_bench1 = []

    var build_no1 = $('#build1').text()
    var build_no2 = $('#build2').text()

    //get all the benchmark values by their name
    for(i = 0; i < bench_names.length; i++){
        dacapo_bench.push($('#'+bench_names[i]).text());
        dacapo_bench1.push($('#'+bench_names[i]+'1').text());
    }

    var trace1 = {
      x: bench_names,
      y: dacapo_bench,
      name: 'Build '+build_no1,
      type: 'bar'
    };
    var trace2 = {
      x: bench_names,
      y: dacapo_bench1,
      name: 'Build '+build_no2,
      type: 'bar'
    };

    var data = [trace1, trace2];
    var layout = {
      title: 'Dacapo benchmarks',
      xaxis: {
        title: 'Dacapo benchmarks',
        titlefont: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
      yaxis: {
        title: 'Milliseconds',
        titlefont: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
      barmode: 'group'
    };

    TESTER = document.getElementById('testerD');
    Plotly.plot( TESTER, data, layout);
 }