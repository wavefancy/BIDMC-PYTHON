var colors = {
    "protein coding"       : d3.rgb('#A00000'),
    "pseudogene"           : d3.rgb('#666666'),
    "processed transcript" : d3.rgb('#0033FF'),
    "ncRNA"                : d3.rgb('#8B668B'),
    "antisense"            : d3.rgb('#CBDD8B'),
};

var biotype_to_legend = {
    "protein_coding"       : "protein coding",
    "pseudogene"           : "pseudogene",
    "processed_pseudogene" : "pseudogene",
    "processed_transcript" : "processed transcript",
    "miRNA"                : "ncRNA",
    "lincRNA"              : "ncRNA",
    "misc_RNA"             : "ncRNA",
    "snoRNA"               : "ncRNA",
    "snRNA"                : "ncRNA",
    "rRNA"                 : "ncRNA",
    "antisense"            : "antisense",
    "sense_intronic"       : "antisense"
};

var render = function (div) {
    //load gene name from txt file
    var dgenes = []; //genes for display.
    d3.tsv("displayGenes.txt", function(data) {
      // alert(JSON.stringify(data[0]));
      data.forEach(function(d) {
          dgenes.push(d.name);
      })

      // alert(JSON.stringify(dgenes));

          // legend placeholder
          var legend_div = d3.select(div)
              .append("div")
              .attr("id", "mylegend")
              .attr("class", "tnt_legend_div");

          legend_div
              .append("text")
              .text("Gene legend:");

          // Gene track
          var gene_track = tnt.board.track()
              .height(330)
              .color("white")
              .display(tnt.board.track.feature.genome.gene()
                   .color("#550055")
              )
              .data(tnt.board.track.data.genome.gene());

          d3.selectAll("tnt_biotype")
              .data(gene_track.data().elements());

          // Get the default data updater...
          var gene_updater = gene_track.data().retriever();
          // ... and create a new updater that calls the orig one + populates the legend dynamically
          gene_track.data().retriever (function (obj) {
              return gene_updater.call(gene_track, obj)
                  .then (function (genes) {
                     //***********Do gene filter****************
                    //  alert(JSON.stringify(genes))
                    // $("#temptxt").text(JSON.stringify(genes));
                      // alert(genes[0].external_name);
                      var mygenes = [];
                      genes.forEach(function(d){
                          if(dgenes.indexOf(d.external_name) >= 0){
                              mygenes.push(d);
                          }
                      });

                      // alert(mygenes.length)
                      genes = mygenes;

                      //**********end gene filter*****************
                      genes.map(gene_color);

                      // And we setup/update the legend
                      var biotypes_array = genes.map(function(e){
                          return biotype_to_legend[e.biotype];
                      });
                      var biotypes_hash = {};
                      for (var i=0; i<biotypes_array.length; i++) {
                          biotypes_hash[biotypes_array[i]] = 1;
                      }
                      var biotypes = [];
                      for (var p in biotypes_hash) {
                          if (biotypes_hash.hasOwnProperty(p)) {
                              biotypes.push(p);
                          }
                      }
                      // alert(biotypes)
                      //remove undefined biotype.
                      // biotypes.splice(2,1);

                      var biotype_legend = legend_div.selectAll(".tnt_biotype_legend")
                          .data(biotypes, function(d){
                              return d;
                          });

                      var new_legend = biotype_legend
                          .enter()
                          .append("div")
                          .attr("class", "tnt_biotype_legend")
                          .style("display", "inline");

                      new_legend
                          .append("div")
                          .style("display", "inline-block")
                          .style("margin", "0px 2px 0px 15px")
                          .style("width", "10px")
                          .style("height", "10px")
                          .style("border", "1px solid #000")
                          .style("background", function(d){return colors[d];});
                      new_legend
                          .append("text")
                      .text(function(d){return d;});
                      biotype_legend
                          .exit()
                          .remove();

                      return genes;
                  });
          });

          var gene_color =  function (gene) {
              gene.color = colors[biotype_to_legend[gene.biotype]];
              return;
          };

          var rightEnd = 31324965 + 150000
          var leftEnd = 29527702 - 15000
          var genome = tnt.board.genome()
              .species("human")
              .chr(6).from(leftEnd).to(rightEnd)
              // .gene("ubd")
              .width(600)
              .min_coord (new Promise (function (res) {
              res(leftEnd);
              }))
              .max_coord (new Promise (function (res) {
              res(rightEnd);
              }))
          // .species("human").gene("brca2").width(950);

          genome.add_track(gene_track);
          genome(div);
          genome.start();

          //move legend to the end of this plot.
          var legend = $("#mydiv").find("div");
          legend.first().insertAfter(legend.last());
          // alert(legend)
          // alert($("#mydiv").html());

  }); //end of read data.
};
