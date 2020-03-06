function populate_dropdown() {
    var e = document.getElementById("firstList");
    var version_chosen = e.options[e.selectedIndex].value;

    var second_dropdown = document.getElementById("parameter1_chooser");
    removeOptions(second_dropdown);

    console.log(version_chosen);

    if (version_chosen == "v1") {
        var options = ["5", "6", "7"];
    }
    else if (version_chosen == "v2"){
        var options = ["1", "2", "3"];
    }
    else if (version_chosen == "v3"){
        var options = ["10", "20", "30"];
    }
    else {
        var options = [];
    }

    console.log(options);

    for(var i = 0; i < options.length; i++) {
       var opt = options[i];
       var element = document.createElement("option");
       element.textContent = opt;
       element.value = opt;
       second_dropdown.appendChild(element);
    }
};


function removeOptions(selectElement) {
   var i, L = selectElement.options.length - 1;
   for(i = L; i >= 0; i--) {
      selectElement.remove(i);
   }
}


function load_home() {
    var e = document.getElementById("firstList");
    var version_chosen = e.options[e.selectedIndex].value;

    console.log(version_chosen);

    if (version_chosen == 1) {
        var result = "ok"
        var html_file = "{{ url_for('times_page_new_version_layout') }}";
         document.getElementById("content").innerHTML += '<object type="text/html" data="templates/times_page_new_version_layout.html"></object>'
         console.log('ouiiiiiiiii');
         console.log(document.getElementById("content").innerHTML);
    }
    else if (version_chosen == 2){


        var html_file = "{{ url_for('times_page_version_layout') }}";
    };



}






