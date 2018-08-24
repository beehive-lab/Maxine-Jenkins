$(document).ready(function() {
    //when the page loads, do the following...

    //draw the graphs
    specjvm_data = gather_data(["startup", "compiler", "compress", "crypto", "derby", "mpegaudio", "scimark", "serial", "spec_sunflow", "xml"]);
    draw_specjvm(specjvm_data);

    dacapo_data = gather_data(["avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan"]);
    draw_dacapo(dacapo_data);

    //add-remove button handlers
    $(".add_build").click(function(){

        var MAX_BUILDS = 5;

        var new_no_builds = parseInt($('#modal_no_bld').val()) + 1

        if(new_no_builds <= MAX_BUILDS){
           var new_row = '<tr>'+
                                    '<td>Revision: </td>'+
                                    '<td><input type="text" name="build_rev" maxlength="40" required/></td>'+
                                    '<td>TAG: </td>'+
                                    '<td><input type="text" name="build_tag" value="default" required/></td>'+
                                    '<td><button type="button" class="btn delete_build">Delete</button></td>'+
                       '</tr>'
            $("#revision_input_table").append(new_row);
            $('#modal_no_bld').val(new_no_builds)
        }

    })

    $(document).on("click", ".delete_build", function(){

        var new_no_builds = parseInt($('#modal_no_bld').val()) - 1

        if(new_no_builds >= 2){
            $(this).parents("tr").remove();
            $('#modal_no_bld').val(new_no_builds)
        }

    })

 });

function gather_data(bench_names){

    var num_bench = $('#no_bench').val();

    var data = [];

    for(b = 1; b <= num_bench; b++){

        var build_no = $('#build'+b).text();

        var rev_short = $('#rev'+b).text().substring(0,7);

        var tag = $('#tag'+b).text();

        var specjvm_bench = [];

        for(i = 0; i < bench_names.length; i++){
            var bench_value = $('#'+bench_names[i]+b).text()

            //if there was something wrong with the benchmark, push "0"
            if (bench_value == "missing" || bench_value == "interpt/failed")
                specjvm_bench.push("0");
            else
                specjvm_bench.push(bench_value);
        }

        var trace = {
              x: bench_names,
              y: specjvm_bench,
              name: rev_short+"_"+tag,
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