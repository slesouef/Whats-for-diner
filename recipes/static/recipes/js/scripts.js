/*!
* Start Bootstrap - Business Casual v6.0.0 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
document.getElementById("add_ingredient").addEventListener("click", function () {
    let click = document.getElementById("add_ingredient").value;
    if (click === '') {
        return false;
    } else {
    //    call create view , method PUT, arg ingredient
    }
});

document.getElementById("add_step").addEventListener("click", function () {
    let click = document.getElementById("add_step").value;
    if (click === '') {
        return false;
    } else {
    //    call create view , method PUT, arg step
    }
});

function add_new_entry() {
    let tempDiv = document.createElement("div");
    tempDiv.className = "form-group";
    tempDiv.innerHTML = "<label for=\"id_ingredient\" class=\"small\">Nom</label>\n" +
        "                    <input id=\"id_ingredient\" class=\"col-6\" type=\"text\" name=\"ingredient\" maxlength=\"255\">\n" +
        "                    <label for=\"id_quantity\" class=\"small mx-1\">Quantite</label>\n" +
        "                    <input id=\"id_quantity\" class=\"col-1\" type=\"text\" name=\"quantity\">";
    document.getElementById("ingredients_list").appendChild(tempDiv);
}