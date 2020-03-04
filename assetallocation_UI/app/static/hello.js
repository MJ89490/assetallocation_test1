

function getFoodItem(){

    var list1 = document.getElementById('firstList');
    var list1SelectedValue = list1.options[list1.selectedIndex].value;


    if (list1SelectedValue == 2)
    {
        alert("ouiiiii")
        {% include 'times_page_new_version_layout.html' %}


    }




}


