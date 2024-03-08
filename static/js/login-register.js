function openForm(evt, formName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        console.log(tabcontent[i].className);
        console.log(tabcontent[i].classList);
        if (tabcontent[i].className == "tabcontent active") {
            tabcontent[i].style.display = "none";
        }
        tabcontent[i].classList.remove("active");
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(formName).style.display = "block";
    setTimeout(function () {
        document.getElementById(formName).classList.add("active");
    }, 0);
    evt.currentTarget.className += " active";
}