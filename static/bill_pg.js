function searchFunction() {
    let input = document.getElementById("searchdish").value.toLowerCase();
    let items = document.getElementsByClassName("item");
        for (let i = 0; i < items.length; i++) {
            // Get the first <h4> inside .item (your item name)
            let title = items[i].getElementsByTagName("h4")[0].innerText.toLowerCase();

            // Show or hide item
            if (title.includes(input)) {
                items[i].style.display = "";
            } else {
                items[i].style.display = "none";
            }
        }
    }