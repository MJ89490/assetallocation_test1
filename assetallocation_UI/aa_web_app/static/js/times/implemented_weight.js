const $tableID = $('#table');
const $BTN = $('#export-btn');

 // Export implemented weight

 jQuery.fn.pop = [].pop;
 jQuery.fn.shift = [].shift;

 $BTN.on('click', () => {

   console.log('hellooo');

   const $rows = $tableID.find('tr:not(:hidden)');
   const headers = [];
   const data = [];

   // Get the headers (add special header logic here)
   $($rows.shift()).find('th:not(:empty)').each(function () {

     headers.push($(this).text().toLowerCase());
   });

   // Turn all existing rows into a loopable array
   $rows.each(function () {
     const $td = $(this).find('td');
     const h = {};

     // Use the headers from earlier to name our hash keys
     headers.forEach((header, i) => {

       if (header == 'weight'){
            h[header] = $td.eq(i).text();
       }
     });
     data.push(h);
   });


   json_data = JSON.stringify(data);

    //   $.ajax({
    //    url: "receive_sidebar_data_times_form",
    //    data: {json_data: json_data},
    //    type: 'POST',
    //    success: function(response){
    //        console.log(response);
    //    },
    //    error: function(error){
    //        console.log(error);
    //    }
    //});

       // Output the result
       //$EXPORT.text();
 });