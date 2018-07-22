$(document).ready(function() {
    //when the page loads, do the following...

    specjvm_data = gather_data(["startup", "compiler", "compress", "crypto", "derby", "mpegaudio", "scimark", "serial", "spec_sunflow", "xml"]);
    draw_specjvm(specjvm_data);

    dacapo_data = gather_data(["avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan"]);
    draw_dacapo(dacapo_data);

 });

function gather_data(bench_names){

    var num_bench = $('#no_bench').val();

    var data = [];

    for(b = 1; b <= num_bench; b++){

        var build_no = $('#build'+b).text();

        var specjvm_bench = [];

        for(i = 0; i < bench_names.length; i++){
            specjvm_bench.push($('#'+bench_names[i]+b).text());
        }

        var trace = {
              x: bench_names,
              y: specjvm_bench,
              name: 'Build '+build_no,
              type: 'bar'
        };

        data.push(trace);

    }

    return data;

}

 function draw_specjvm(data){

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

  function draw_dacapo(data){

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