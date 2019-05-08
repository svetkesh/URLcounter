$(document).ready(function() {
  $('form').on('submit', function(event) {
   $.ajax({
      data : {
             address : $('#address').val(),
                 },
      type : 'POST',
      url : '/process'
      })
    .done(function(data) {
      // redraw message divs
      // $('#piechart').text('');
      $('#chart').text('');
      // $('#status').text('');
      $('#result').text('');
      $('#result').text('');
      $('#starttime').text('');
      $('#endtime').text('');
      $('#deftitle').text('');

      console.log(data.address);
      console.log(data.status);
      console.log(data.result);
      console.log(data['202']['Location']);
      var location = data['202']['Location'];
      console.log(data);

      function update_progress(location) {
        $('#done').text('In progress!').show();

        $.getJSON(location, function (data) {
          console.log(data);
          console.log(data['result']);
          console.log(data['status']);
          var st = data['status'];
          if (st === 'SUCCESS') {
            $('#done').text('Done!').show();
            $('#starttime').text('starttime: ' + data['result']['starttime']).show();
            $('#endtime').text('endtime: ' + data['result']['endtime']).show();

            // builds graph from dictionary
            var results = data['result']['result'];
            console.log("results:");
            console.log(results);

            var totalTags = 0;
            var currentTagsPerCent = 0;

            var dv_head = '<hr><dl><dt id="deftitle">Found tags:</dt>';
            var dv_tail = '</dl>';

            // count total divs for percentage graph
            for (var key in results) {
                if (results.hasOwnProperty(key)) {
                    console.log(key + " -> " + results[key]);
                    totalTags += results[key];
                }
            }

            // show warning against bad page
            if (totalTags !== 1){
              $('#chart').append(dv_head);
              $('#deftitle').text('Found tags: ' + totalTags);
              console.log("totalTags:" + totalTags);

              // building particular graphs
              for (var key in results) {
                  if (results.hasOwnProperty(key)) {
                      console.log(key + " -> " + results[key]);
                      currentTagsPerCent = 100 * (results[key] / totalTags);
                      console.log("currentTagsPerCent:" + currentTagsPerCent);
                      var new_dv = '<dd class="percentage percentage-'+ currentTagsPerCent + '"><span class="text">' + key + ': ' + results[key] + '</span><span style="display:block; background-color:#0275d8; width:' + currentTagsPerCent + '%;">' + results[key] + '</span></dd>';
                      $('#chart').append(new_dv);
                  }
              }
              $('#chart').append(dv_tail);
            }
            else {
              $('#chart').append('<dl><dt id="deftitle">Could not fetch given address</dt>');
              var new_dv = '<dd class="percentage percentage-'+ currentTagsPerCent + '"><span class="text">No tags here :(</span><span style="display:block; background-color:#f4eb0c; width:100%;">.</span></dd>';
              $('#chart').append(new_dv);
              $('#chart').append(dv_tail);
            }
          }
          else {
            setTimeout(function() {
              update_progress(location)
            }, 400);
          }
        });
      };
      update_progress(location);
    });
  event.preventDefault();
  });
});
